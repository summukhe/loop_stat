import numpy as np
from enum import Enum
from typing import Union
from .basis_vector import BasisVector3D, BasisVector2D


class BravaisLatticeType(Enum):
    C2 = 'Monoclinic 2d'
    C2C = 'Monoclinic 2d centered'
    D2 = 'Orthorhombic'
    D2C = 'Orthorhombic centered'
    D4 = 'Tetragonal'
    D6 = 'Hexagonal'
    Ci = 'Triclinic'
    C2h = 'Monoclinic 3d'
    C2hS = 'Monoclinic 3d base centered'
    D2h = 'Orthorhombic'
    D2hS = 'Orthorhombic base centered'
    D2hI = 'Orthorhombic body centered'
    D2hF = 'Orthorhombic face centered'
    D4h = 'Tetragonal'
    D4hI = 'Tetragonal body centered'
    D3d = 'Rhombohedral'
    D6h = 'Hexagonal 3D'
    Oh = 'Cubic'
    OhI = 'Cubic body centered'
    OhF = 'Cubic Face centered'


def to_bravais_lattice_type(lattice_type: Union[str, BravaisLatticeType]):
    if isinstance(lattice_type, BravaisLatticeType):
        return lattice_type
    lattice_ = lattice_type.lower()
    for l_type in BravaisLatticeType:
        if l_type.name.lower() == lattice_:
            return l_type
    raise ValueError(f"Error: unknown lattice type {lattice_type}!")


def generic_2d_basis_system(a_x: float,
                            a_y: float,
                            theta: float):
    lattice_basis = (BasisVector2D([a_x, 0.]),
                     BasisVector2D([a_y * np.cos(theta), a_y * np.sin(theta)]))
    return lattice_basis


def generic_3d_basis_system(a_x: float,
                            a_y: float,
                            a_z: float,
                            alpha: float,
                            beta: float,
                            gamma: float,
                            ):
    cg, sg = np.cos(gamma), np.sin(gamma)
    ca, cb = np.cos(alpha), np.cos(beta)

    lattice_basis = (BasisVector3D([a_x, 0, 0]),
                     BasisVector3D([a_y * cg,
                                    a_y * sg,
                                    0]),
                     BasisVector3D([a_z * cb,
                                    a_z * (ca - cb * cg) / sg,
                                    a_z * np.sqrt(sg ** 2 - ca ** 2 - cb ** 2 + 2 * ca * cb * cg) / sg]))
    return lattice_basis


def get_basis_pair(lattice_type: Union[BravaisLatticeType, str],
                   a_x: float = 1.,
                   a_y: float = 1.,
                   a_z: float = 1.,
                   theta: float = np.pi / 2,
                   alpha: float = np.pi / 2,
                   beta: float = np.pi / 2,
                   gamma: float = np.pi / 2,
                   **kwargs):
    lattice_type = to_bravais_lattice_type(lattice_type)
    lattice_params = dict()
    if lattice_type == BravaisLatticeType.C2:
        lattice_basis = generic_2d_basis_system(a_x, a_y, theta)
    elif lattice_type == BravaisLatticeType.D2:
        lattice_basis = generic_2d_basis_system(a_x, a_y, np.pi/2)
    elif lattice_type == BravaisLatticeType.D2C:
        lattice_basis = generic_2d_basis_system(a_x, a_y, np.pi/2)
        lattice_params['xy_face_centered'] = True
    elif lattice_type == BravaisLatticeType.D4:
        lattice_basis = generic_2d_basis_system(a_x, a_x, np.pi / 2)
    elif lattice_type == BravaisLatticeType.D6:
        lattice_basis = generic_2d_basis_system(a_x, a_x, 2 * np.pi / 3)
    elif lattice_type == BravaisLatticeType.Ci:
        lattice_basis = generic_3d_basis_system(a_x, a_y, a_z, alpha, beta, gamma)
    elif lattice_type == BravaisLatticeType.C2h:
        lattice_basis = generic_3d_basis_system(a_x, a_y, a_z, np.pi/2, beta, np.pi/2)
    elif lattice_type == BravaisLatticeType.C2hS:
        lattice_basis = generic_3d_basis_system(a_x, a_y, a_z, np.pi / 2, beta, np.pi / 2)
        lattice_params['xy_face_centered'] = True
    elif lattice_type == BravaisLatticeType.D2h:
        lattice_basis = generic_3d_basis_system(a_x, a_y, a_z, np.pi/2, np.pi/2, np.pi / 2)
    elif lattice_type == BravaisLatticeType.D2hS:
        lattice_basis = generic_3d_basis_system(a_x, a_y, a_z, np.pi / 2, np.pi / 2, np.pi / 2)
        lattice_params['xy_face_centered'] = True
    elif lattice_type == BravaisLatticeType.D2hI:
        lattice_basis = generic_3d_basis_system(a_x, a_y, a_z, np.pi / 2, np.pi / 2, np.pi / 2)
        lattice_params['body_centered'] = True
    elif lattice_type == BravaisLatticeType.D2hF:
        lattice_basis = generic_3d_basis_system(a_x, a_y, a_z, np.pi / 2, np.pi / 2, np.pi / 2)
        lattice_params['xy_face_centered'] = True
        lattice_params['yz_face_centered'] = True
        lattice_params['xz_face_centered'] = True
    elif lattice_type == BravaisLatticeType.D4h:
        lattice_basis = generic_3d_basis_system(a_x, a_x, a_z, np.pi / 2, np.pi / 2, np.pi / 2)
    elif lattice_type == BravaisLatticeType.D4hI:
        lattice_basis = generic_3d_basis_system(a_x, a_x, a_z, np.pi / 2, np.pi / 2, np.pi / 2)
        lattice_params['body_centered'] = True
    elif lattice_type == BravaisLatticeType.D3d:
        lattice_basis = generic_3d_basis_system(a_x, a_x, a_x, alpha, alpha, alpha)
    elif lattice_type == BravaisLatticeType.D6h:
        lattice_basis = generic_3d_basis_system(a_x, a_x, a_z, np.pi / 2, np.pi / 2, 2 * np.pi / 3)
    elif lattice_type == BravaisLatticeType.Oh:
        lattice_basis = generic_3d_basis_system(a_x, a_x, a_x, np.pi / 2, np.pi / 2, np.pi / 2)
    elif lattice_type == BravaisLatticeType.OhI:
        lattice_basis = generic_3d_basis_system(a_x, a_x, a_x, np.pi / 2, np.pi / 2, np.pi / 2)
        lattice_params['body_centered'] = True
    elif lattice_type == BravaisLatticeType.OhF:
        lattice_basis = generic_3d_basis_system(a_x, a_x, a_x, np.pi / 2, np.pi / 2, np.pi / 2)
        lattice_params['xy_face_centered'] = True
        lattice_params['yz_face_centered'] = True
        lattice_params['xz_face_centered'] = True
    else:
        raise ValueError(f"Error: unknown lattice_type [{lattice_type}]")

    return lattice_basis, lattice_params


