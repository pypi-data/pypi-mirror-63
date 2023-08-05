#!/usr/bin/env python

# Copyright 2020 Informatics Matters Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import print_function
import sys, gzip, json, uuid
from rdkit import Chem
from rdkit.Chem import AllChem
from .sanifix import fix_mol
from .MolFromTypedColumnReader import MolFromTypedColumnReader

from pipelines_utils import utils
from pipelines_utils.StreamJsonListLoader import StreamJsonListLoader


def default_open_input_output(inputDef, inputFormat, outputDef, defaultOutput,
                              outputFormat, thinOutput=False, valueClassMappings=None,
                              datasetMetaProps=None, fieldMetaProps=None):
    """Default approach to handling the inputs and outputs"""
    input, suppl = default_open_input(inputDef, inputFormat)
    output,writer,outputBase =\
        default_open_output(outputDef, defaultOutput, outputFormat,
                            thinOutput=thinOutput,
                            valueClassMappings=valueClassMappings,
                            datasetMetaProps=datasetMetaProps,
                            fieldMetaProps=fieldMetaProps)
    return input,output,suppl,writer,outputBase


def default_open_input(inputDef, inputFormat):
    if not inputDef and not inputFormat:
        raise ValueError('Must specify either an input file name or an input format (or both)')
    elif inputFormat == 'sdf' or (inputDef and (inputDef.lower().endswith('.sdf') or inputDef.lower().endswith('.sdf.gz'))):
        input, suppl = default_open_input_sdf(inputDef)
    elif inputFormat == 'json' or (inputDef and (inputDef.lower().endswith('.data') or inputDef.lower().endswith('.data.gz'))):
        input, suppl = default_open_input_json(inputDef)
    elif inputFormat == 'smiles':
        input, suppl = default_open_input_typed_smiles(inputDef)
    else:
        raise ValueError('Unsupported input format')

    return input, suppl


def default_open_input_sdf(inputDef):
    """Open the input as a SD file (possibly gzipped if ending with .gz) according to RDKit's ForwardSDMolSupplier

    :param inputDef: The name of the file. If None then STDIN is used (and assumed not to be gzipped)
    """
    if inputDef:
        input = utils.open_file(inputDef)
    else:
        # We need to use the (Python 3) stdin.buffer
        # (a binary representation of the input stream)
        # for RDKit in Python 3.
        if sys.version_info[0] >= 3:
            input = sys.stdin.buffer
        else:
            input = sys.stdin
    suppl = Chem.ForwardSDMolSupplier(input)
    return input, suppl


def default_open_input_smiles(inputDef, delimiter='\t', smilesColumn=0,
                              nameColumn=1, titleLine=False):
    """Open the input as a file of smiles (possibly gzipped if ending with .gz)
    according to RDKit's SmilesMolSupplier

    :param inputDef: The name of the file. If None then STDIN is used
                     (and assumed not to be gzipped)
    """
    if inputDef:
        input = utils.open_file(inputDef, as_text=True)
    else:
        input = sys.stdin
    # SmilesMolSupplier is a bit strange as it can't accept a file like object!
    txt = input.read()
    input.close()
    suppl = Chem.SmilesMolSupplier()
    suppl.SetData(txt, delimiter=delimiter, smilesColumn=smilesColumn,
                  nameColumn=nameColumn, titleLine=titleLine)
    return suppl


def default_open_input_typed_smiles(inputDef):
    """Open the input as a file of typed column text containing SMILES
    (possibly gzipped if ending with .gz).

    The user will need to initialise() this object once it's been created
    to provide an optional header and other parameters.

    :param inputDef: The name of the file, or None if to use STDIN.
                     If filename ends with .gz will be gunzipped
    """
    if inputDef:
        input = utils.open_file(inputDef, as_text=True)
    else:
        input = sys.stdin
    suppl = MolFromTypedColumnReader(input)
    return input, suppl


def open_smarts(filename):
    """Very simple smarts parser that expects smarts expression
    (and nothing else) on each line (no header)"""
    f = open(filename)
    count = 0
    for line in f:
        count += 1
        mol = Chem.MolFromSmarts(line)
        if mol:
            mol.SetIntProp("idx", count)
        yield mol


def default_open_input_json(inputDef, lazy=True):
    """Open the given input as JSON array of Squonk MoleculeObjects.

    :param inputDef: The name of the input file, or None if to use STDIN.
                     If filename ends with .gz will be gunzipped
    :param lazy: Use lazy loading of the JSON. If True will allow handling of
                 large datasets without being loaded into memory,
                 but may be less robust and will be slower.
    """
    if inputDef:
        if inputDef.lower().endswith('.gz'):
            input = gzip.open(inputDef, 'rt')
        else:
            input = open(inputDef, 'r')
    else:
        input = sys.stdin
    if lazy:
        suppl = generate_mols_from_json(StreamJsonListLoader(input))
    else:
        suppl = generate_mols_from_json(json.load(input))
    return input, suppl


def default_open_output(outputDef, defaultOutput, outputFormat, compress=True,
                        thinOutput=False, valueClassMappings=None,
                        datasetMetaProps=None, fieldMetaProps=None):

    outputFormat = utils.determine_output_format(outputFormat)

    if not outputDef:
        outputBase = defaultOutput
    else:
        outputBase = outputDef

    if outputFormat == 'sdf':
        output,writer = default_open_output_sdf(outputDef, outputBase, thinOutput, compress)
    elif outputFormat == 'json':
        output,writer = default_open_output_json(outputDef, outputBase, thinOutput, compress,
                                                 valueClassMappings, datasetMetaProps, fieldMetaProps)
    else:
        raise ValueError('Unsupported output format')
    return output,writer,outputBase


def default_open_output_sdf(outputDef, outputBase, thinOutput, compress):

    output = utils.open_output(outputDef, 'sdf', compress)

    if thinOutput:
        writer = ThinSDWriter(output)
    else:
        writer = ThickSDWriter(output)
    return output, writer


def default_open_output_json(outputDef, outputBase, thinOutput,
                             compress, valueClassMappings, datasetMetaProps,
                             fieldMetaProps):

    # this writes the metadata that Squonk needs
    utils.write_squonk_datasetmetadata(outputBase, thinOutput, valueClassMappings,
                                       datasetMetaProps, fieldMetaProps)

    output = utils.open_output(outputDef, 'data', compress)

    if thinOutput:
        writer = ThinJsonWriter(output)
    else:
        writer = ThickJsonWriter(output)
    return output,writer


def read_single_molecule(filename, index=1, format=None):
    """Read a single molecule as a RDKit Mol object. This can come from a file in molfile or SDF format.
    If SDF then you can also specify an index of the molecule that is read (default is the first)
    """
    mol = None
    if format == 'mol' or filename.lower().endswith('.mol') or filename.lower().endswith('.mol.gz'):
        file = utils.open_file(filename)
        mol = Chem.MolFromMolBlock(file.read())
        file.close()
    elif format == 'sdf' or filename.lower().endswith('.sdf') or filename.lower().endswith('.sdf.gz'):
        file = utils.open_file(filename)
        supplier = Chem.ForwardSDMolSupplier(file)
        for i in range(0,index):
            if supplier.atEnd():
                break
            mol = next(supplier)
        file.close()
    elif format == 'json' or filename.lower().endswith('.data') or filename.lower().endswith('.data.gz'):
        input, suppl = default_open_input_json(filename)
        for i in range(0,index):
            try:
                mol = next(suppl)
            except StopIteration:
                break
        input.close()

    if not mol:
        raise ValueError("Unable to read molecule")

    return mol


def parse_mol_simple(my_type, txt):
    """Function to parse individual mols given a type.

    :param my_type: A type definition (i.e. "mol" or "smiles")
    :param txt: The textual definition of the molecule (i.e. a SMILES string)
    :return: A mol instance or None if the molecule could not be compiled
    """
    # Ignore unexpected parameter values...
    if my_type is None or not my_type or txt is None or not txt:
        return None

    if my_type == "mol":
        # Try this way
        mol = Chem.MolFromMolBlock(txt.strip())
        if mol is None:
            mol = Chem.MolFromMolBlock(txt)
        if mol is None:
            mol = Chem.MolFromMolBlock("\n".join(txt.split("\n")[1:]))
        # Now try to do sanifix
        if mol is None:
            mol = fix_mol(Chem.MolFromMolBlock(txt, False))
        # And again
        if mol is None:
            mol = fix_mol(Chem.MolFromMolBlock(txt.strip(), False))
    elif my_type == "smiles":
        # Assumes that smiles is the first column -> and splits on chemaxon
        mol = Chem.MolFromSmiles(txt.split()[0].split(":")[0])
    if mol is None:
        utils.log('Failed to parse mol "%s" for my_type %s' % (txt, my_type))
    return mol


def create_mol_from_props(molobj):
    """Function to get the RDKit mol from MoleculeObject JSON

    :param molobj: Python dictionary containing the molecule's properties
    """

    if "source" not in molobj or "format" not in molobj:
        return None

    molstr = str(molobj["source"])
    # Get the format and use this as a starting point to work out
    molformat = molobj["format"]
    # Now parse it with RDKit
    mol = parse_mol_simple(molformat, molstr)
    if mol:
        if "values" in molobj:
            values = molobj["values"]
            for key in values:
                mol.SetProp(str(key), str(values[key]))
        uuid = str(molobj["uuid"])
        if uuid:
            mol.SetProp("uuid", uuid)
            mol.SetProp("_Name", uuid)
    return mol


def clear_mol_props(mol, exceptFor):
    for p in mol.GetPropNames():
        if p not in exceptFor:
            mol.ClearProp(p)


def generate_mols_from_json(input):
    """Create a supplier of RDKit Mol objects from the json

    :param input: file like object containing the json representation of the molecules
    """
    j=0
    for item in input:
        j+=1
        mol = create_mol_from_props(item)
        if not mol:
            # TODO - get a count of the errors and report
            utils.log("Failed to create molecule - skipping. Data was ", item)
            continue
        yield mol


def generate_2d_coords(mol):
    AllChem.Compute2DCoords(mol)

class ThickJsonWriter:

    def __init__(self, file):
        self.file = file
        self.file.write('[')
        self.count = 0

    def write(self, mol, props=None, includeStereo=True, confId=-1,
              kekulize=True, forceV3000=False, format='mol'):
        d = {}
        if format == 'mol':
            d['source'] = Chem.MolToMolBlock(mol, includeStereo=includeStereo, confId=confId, kekulize=kekulize, forceV3000=forceV3000)
            d['format'] = 'mol'
        elif format == 'smiles':
            if kekulize:
                Chem.Kekulize(mol)
            d['source'] = Chem.MolToSmiles(mol, isomericSmiles=includeStereo, kekuleSmiles=kekulize)
            d['format'] = 'smiles'
        else:
            raise ValueError("Unexpected format: " + format)
        allProps = mol.GetPropsAsDict()
        if props:
            allProps.update(props)

        if 'uuid' in allProps:
            d['uuid'] = allProps['uuid']
            del allProps['uuid']
        else:
            d['uuid'] = str(uuid.uuid4())
        if allProps:
            d['values'] = allProps
        #utils.log("Mol:",d)
        json_str = json.dumps(d)
        if self.count > 0:
            self.file.write(',')
        self.file.write(json_str)
        self.count += 1

    def close(self):
        self.file.write(']')
        self.file.close()

    def flush(self):
        self.file.flush()

class ThinJsonWriter:

    def __init__(self, file):
        self.file = file
        self.file.write('[')
        self.count = 0

    def write(self, mol, props=None, includeStereo=True, confId=-1, kekulize=True, forceV3000=False):
        d = {}
        allProps = mol.GetPropsAsDict()
        if props:
            allProps.update(props)

        if 'uuid' in allProps:
            d['uuid'] = allProps['uuid']
            del allProps['uuid']
        else:
            d['uuid'] = str(uuid.uuid4())
        if allProps:
            d['values'] = allProps
        json_str = json.dumps(d)
        if self.count > 0:
            self.file.write(',')
        self.file.write(json_str)
        self.count += 1

    def close(self):
        self.file.write(']')
        self.file.close()

    def flush(self):
        self.file.flush()

class ThinSDWriter:
    def __init__(self, output):
        self.count = 0
        self.writer = Chem.SDWriter(output)

    def write(self, mol, confId=-1, props=None):
        emptyMol = Chem.Mol()
        allProps = mol.GetPropsAsDict()
        for key in allProps:
            emptyMol.SetProp(key, str(allProps[key]))
        self.writer.write(emptyMol)
        self.count += 1

    def close(self):
        self.writer.close()

    def flush(self):
        self.writer.flush()


class ThickSDWriter:
    def __init__(self, output):
        self.count = 0
        self.writer = Chem.SDWriter(output)

    def write(self, mol, confId=-1, props=None):
        self.writer.write(mol)
        self.count += 1

    def close(self):
        self.writer.close()

    def flush(self):
        self.writer.flush()

# class TabWriter:
#
#     def __init__(self, file, propertiesToWrite=None, includeStereo=True, kekulize=False):
#         self.file = file
#         self.count = 0
#         self.includeStereo = includeStereo
#         self.kekulize = kekulize
#         self.propertiesToWrite = propertiesToWrite
#         if propertiesToWrite is None:
#             utils.log("WARNING: propertiesToWrite not defined. Output may be misformatted if the same properties are not present for each record")
#
#     def writeHeader(self):
#         if self.propertiesToWrite is None:
#             raise ValueError("Cannot write header if propertiesToWrite is not set")
#         line = "SMILES"
#         for prop in self.propertiesToWrite:
#             line += "\t" + prop
#         self.file.write(line + "\n")
#
#
#     def write(self, mol, props=None, confId=-1):
#         if self.kekulize:
#             Chem.Kekulize(mol)
#         line = Chem.MolToSmiles(mol, isomericSmiles=self.includeStereo, kekuleSmiles=self.kekulize)
#         allProps = mol.GetPropsAsDict()
#         if props:
#             allProps.update(props)
#
#         if self.propertiesToWrite is None:
#             propsToUse = allProps
#         else:
#             propsToUse = self.propertiesToWrite
#
#         for prop in propsToUse:
#             line += line + "\t"
#             val = allProps[prop]
#             if val is not None:
#                 line += str(val)
#
#         self.file.write(line + "\n")
#         self.count += 1
#
#     def close(self):
#         self.file.close()
#
#     def flush(self):
#         self.file.flush()