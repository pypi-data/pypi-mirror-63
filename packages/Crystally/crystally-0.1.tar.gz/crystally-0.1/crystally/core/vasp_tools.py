import crystally as cr


def interpolate_lattices(lattice1: cr.Lattice, lattice2: cr.Lattice, weighting=0.5):
    if len(lattice1.atoms) != len(lattice2.atoms):
        raise ValueError("lattices must have the same number of atoms!")

    new_lattice = cr.Lattice(vectors=lattice1.vectors, atoms=[])
    for atom1, atom2 in zip(lattice1, lattice2):
        new_position = atom1.position + atom1.position.diff(atom2.position)*weighting
        new_atom = cr.Atom(element=atom1.element, position=new_position, sublattice=atom1.sublattice)
        new_lattice.atoms.append(new_atom)
    return new_lattice

