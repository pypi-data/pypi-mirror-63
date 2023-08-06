#!/usr/bin/python

import sys
import random
import argparse
import libmsym as msym
import numpy as np
from numpy.linalg import norm


def set_basis(element, name="1s"):
    basis_function = msym.RealSphericalHarmonic(element=element, name=name)
    element.basis_functions = [basis_function]
    return basis_function


def atoms_dict_to_msym_elements(indata):
    """
    indata should be a dict, including elements & positions
    """
    msym_elements = []
    symbols = indata['symbols']
    positions = indata['positions']
    for i in range(0, len(symbols)):
        msym_elements.append(msym.Element(
            name=symbols[i], coordinates=positions[i]))
    return msym_elements


def msym_elements_to_atoms_dict(elements):
    symbols = [_.name for _ in elements]
    positions = [_.coordinates for _ in elements]
    atoms_dict = {
        'symbols': symbols,
        'positions': positions
    }
    return atoms_dict


def symmetry_operations_to_dict(symmetry_operations):
    """
    """
    if not isinstance(symmetry_operations, list):
        _symmetry_operations = [symmetry_operations]
    else:
        _symmetry_operations = symmetry_operations
    results = []
    for _ in _symmetry_operations:
        name = _._names[_.type]
        order = _.order
        power = _.power
        orientation = _.orientation
        vector = _._v[:]
        conjugacy_class = _.conjugacy_class
        if _.type == _.PROPER_ROTATION and _.order == 2:
            orientation = _._proper_rotation_type_names[_.orientation]
        elif _.type == _.REFLECTION:
            orientation = _._reflection_type_names[_.orientation]
            axis = " with normal vector " + repr(_.vector)

        if _.type in [_.PROPER_ROTATION, _.IMPROPER_ROTATION]:
            order = str(_.order)
            power = "^" + str(_.power)
            axis = " around " + repr(_.vector)

        results.append({
            'name': name,
            'order': order,
            'power': power,
            'orientation': orientation,
            'vector': vector,
            'conjugacy_class': conjugacy_class
        })
    if not isinstance(symmetry_operations, list):
        return results[0]
    return results


def basis_functions_to_dict(basis_functions, all_elements):
    _basis_functions = basis_functions
    if not isinstance(basis_functions, list):
        _basis_functions = [basis_functions]
    results = []
    for x in _basis_functions:
        element = x.element
        symbol = element.name
        for i, el in enumerate(all_elements):
            if norm(np.array(el._v[:]) - np.array(element._v[:])) < 0.01:
                element_id = i
                break
        results.append({
            'number': element_id,
            'symbol': symbol,
            'type': x._type,
            'name': x.name,
        })
    if not isinstance(basis_functions, list):
        return results[0]
    return results


def subrepresentation_spaces_to_dict(subrepresentation_spaces, all_elements):
    _subrepresentation_spaces = subrepresentation_spaces
    if not isinstance(subrepresentation_spaces, list):
        _subrepresentation_spaces = [subrepresentation_spaces]
    results = [
        {
            'symmetry_species': x.symmetry_species,
            'salcs': [
                {
                    'basis_functions': [basis_functions_to_dict(z, all_elements) for z in y.basis_functions],
                    'partner_functions': y.partner_functions.tolist()
                } for y in x.salcs],
        } for x in _subrepresentation_spaces
    ]
    if not isinstance(subrepresentation_spaces, list):
        return results[0]
    return results


def symmetry_species_to_dict(symmetry_species):
    _symmetry_species = symmetry_species
    if not isinstance(symmetry_species, list):
        _symmetry_species = [symmetry_species]
    results = []
    for x in symmetry_species:
        dim = x.dim
        reducible = x.reducible
        name = x.name
        results.append({
            'dim': dim,
            'reducible': reducible,
            'name': name
        })
    if not isinstance(symmetry_species, list):
        return results[0]
    return results


def get_symmetry_info_with_elements(elements, basis_functions=None, threshold=0.1):
    if basis_functions is None:
        basis_functions = [set_basis(e) for e in elements]
    assert isinstance(threshold, float)
    with msym.Context(elements=elements, basis_functions=basis_functions) as ctx:
        point_group = ctx.find_symmetry()
        symm_elements = ctx.symmetrize_elements()
        symm_atoms = msym_elements_to_atoms_dict(symm_elements)
        results = {
            'point_group': point_group,
            'symm_atoms': symm_atoms,
            'symmetry_operations': symmetry_operations_to_dict(ctx.symmetry_operations),  # symmetry operations
            'subrepresentation_spaces': subrepresentation_spaces_to_dict(ctx.subrepresentation_spaces, ctx.elements),  # subspace
            'table': ctx.character_table.table,  # table as numpy array
            'character_table_symmetry_operations': symmetry_operations_to_dict(ctx.character_table.symmetry_operations),  # representative symmetry operations
            'symmetry_species': symmetry_species_to_dict(ctx.character_table.symmetry_species),  # symmetry species
        }
    return results

#         print(results)
# 
#         somefunc = np.zeros((len(basis_functions)), dtype=np.float64)
#         for i in range(0, len(somefunc)):
#             somefunc[i] = i
#         species_components = ctx.symmetry_species_components(somefunc)
#         species = ctx.character_table.symmetry_species
# 
#         print('somefunc', somefunc)
#         for i, c in enumerate(species_components):
#             print('species_components', str(c),  species[i].name)
# 
#         # matrix version of the above, as well as wave function symmetrization
#         (matrix, species, partners) = ctx.salcs
#         (d, d) = matrix.shape
#         print('matrix', matrix)
#         print('species', species)
#         print('partners', [(p.index, p.dim) for p in partners])
#         indexes = [x for x in range(0, d)]
#         random.shuffle(indexes)
#         matrix = matrix[indexes, :]
#         matrix += 0.01
#         print('matrix', matrix)
#         (_same_matrix, species, partners) = ctx.symmetrize_wavefunctions(matrix)
#         print('matrix', matrix)
#         print('species', species)
#         print('partners', [(p.index, p.dim) for p in partners])
# 
#         write_xyz(args.outfile, symm_elements,
#                   " symmetrized by libmsym according to point group " + point_group)
# 
#         # generating elements
#         ctx.point_group = "D6h"
#         gen_elements = [msym.Element(name="C", coordinates=[1.443524, 0.0, 0.0]),
#                         msym.Element(name="H", coordinates=[
#                                      2.568381, 0.0, 0.0])
#                         ]
#         benzene = ctx.generate_elements(gen_elements)
#         maxcomp = max([max(e.coordinates) for e in benzene])
#         print(len(benzene), "\nbenzene")
#         for e in benzene:
#             vec = np.asarray(e.coordinates)
#             vec[vec < maxcomp*sys.float_info.epsilon] = 0
#             print(e.name, vec[0], vec[1], vec[2])
# 
#    with msym.Context(elements = elements, point_group = "T") as ctx:
#       point_group = ctx.point_group
#       symm_elements = ctx.symmetrize_elements()
#       write_xyz(args.outfile, symm_elements, comment + " symmetrized by libmsym according to point group " + point_group)



def get_symmetry_info(atoms_dict, basis_functions=None, threshold=0.1):
    elements = atoms_dict_to_msym_elements(atoms_dict)
    if basis_functions is None:
        basis_functions = [set_basis(e) for e in elements]
    results = get_symmetry_info_with_elements(elements, basis_functions, threshold)
    return results
