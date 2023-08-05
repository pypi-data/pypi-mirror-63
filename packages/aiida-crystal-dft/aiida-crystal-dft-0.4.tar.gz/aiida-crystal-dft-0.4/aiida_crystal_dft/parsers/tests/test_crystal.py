#   Copyright (c)  Andrey Sobolev, 2019. Distributed under MIT license, see LICENSE file.

# noinspection PyUnresolvedReferences
from aiida_crystal_dft.tests.fixtures import *


def test_crystal_parser(crystal_calc_node):
    from aiida.plugins import DataFactory
    from aiida_crystal_dft.parsers.cry_pycrystal import CrystalParser
    calcnode = crystal_calc_node()
    parser = CrystalParser(calcnode)

    parser.parse()
    nodes = parser.outputs
    # wavefunction tests
    assert parser._linkname_wavefunction in nodes
    assert isinstance(nodes[parser._linkname_wavefunction], DataFactory("singlefile"))
    # output parameter tests
    assert parser._linkname_parameters in nodes
    assert isinstance(nodes[parser._linkname_parameters], DataFactory("dict"))
    assert nodes[parser._linkname_parameters].dict.energy == -7473.995626235668
    # output structure tests
    assert parser._linkname_structure in nodes
    assert isinstance(nodes[parser._linkname_structure], DataFactory("structure"))
    ase_struct = nodes[parser._linkname_structure].get_ase()
    assert 8 in ase_struct.get_atomic_numbers()
    # output trajectory tests
    assert parser._linkname_trajectory in nodes
    assert isinstance(nodes[parser._linkname_trajectory], DataFactory("array.trajectory"))
    assert nodes[parser._linkname_trajectory].numsteps == 13


def test_crystal_raman_parser(crystal_calc_node):
    from aiida.plugins import DataFactory
    from aiida_crystal_dft.parsers.cry_pycrystal import CrystalParser
    calcnode = crystal_calc_node(files={'crystal.out': 'mgo_sto3g/raman'})
    parser = CrystalParser(calcnode)

    parser.parse()
    nodes = parser.outputs
    # output parameter tests
    assert parser._linkname_parameters in nodes
    assert isinstance(nodes[parser._linkname_parameters], DataFactory("dict"))
    assert nodes[parser._linkname_parameters].dict.energy == -7473.993352557831
    assert nodes[parser._linkname_parameters].dict.phonons['zero_point_energy'] == 0.09020363263183974
    assert nodes[parser._linkname_parameters].dict.phonons['thermodynamics']['temperature'][0] == 298.15


def test_crystal_elastic_parser(crystal_calc_node):
    from aiida.plugins import DataFactory
    from aiida_crystal_dft.parsers.cry_pycrystal import CrystalParser
    calcnode = crystal_calc_node(files={'crystal.out': 'mgo_sto3g/elastic'})
    parser = CrystalParser(calcnode)

    parser.parse(retrieved_temporary_folder=calcnode.outputs.retrieved)
    nodes = parser.outputs
    # output parameter tests
    assert parser._linkname_parameters in nodes
    assert isinstance(nodes[parser._linkname_parameters], DataFactory("dict"))
    assert nodes[parser._linkname_parameters].dict.elastic['bulk_modulus'] == 470.57
