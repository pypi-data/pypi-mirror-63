from crystally.core.vectors import *
import copy
import crystally.core.constants as constants
from typing import Union


class Atom:
    """An entry within a crystal cell.

    The Atom has three propertiers. An element from the periodic table, fractional coordinates in form of a
    :class:`~crystal_creator.core.vectors.FractionalVector` and a sublattice identifier.

    :param element: string of element name
    :param position: fractional position of the atom
    :param sublattice: name of the sublattice the atom is in
    :return: Atom object
    """

    def __init__(self, element: str ="", position=(0, 0, 0), sublattice: str=""):
        self.element = str(element)
        self._position = FractionalVector(position)
        self.sublattice = str(sublattice)

    def __str__(self):
        string_representation = "Atom:"
        string_representation += f" {self.element:4s} "
        string_representation += f" [{', '.join([f'{coord:13.10f}' for coord in self.position.value])}] "
        string_representation += f" {self.sublattice:8s}"
        return string_representation

    def __repr__(self):
        rep = "Atom("
        rep += repr(self.element)    + ","
        rep += repr(self.position)   + ","
        rep += repr(self.sublattice) + ")"
        return rep

    def __eq__(self, other):
        return self.element == other.element        \
           and self.position == other.position      \
           and self.sublattice == other.sublattice

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = FractionalVector(new_position)


class Lattice:
    """A crystal lattice with atoms and crystal vectors

    :param atoms: string of element name
    :param vectors: fractional position of the atom
    :return: Lattice object
    """

    def __init__(self, vectors=np.identity(3), atoms=None):
        self._vectors = None
        self.atoms = list(atoms) if atoms is not None else None
        self.vectors = vectors

    def __iter__(self):
        return iter(self.atoms)

    def __str__(self):
        string_rep = "Lattice:\n" \
                     + " "*5 + "Vectors:\n"
        for vec in self.vectors:
            components = ["{:13.10f}".format(i) for i in vec]
            string_rep += "{:>23s} {} {}\n".format(*tuple(components))
        string_rep += " "*5 + "Positions:\n"
        for i in range(0, len(self.atoms)):
            string_rep += " "*10
            string_rep += "{: <5d}".format(i)
            string_rep += str(self.atoms[i])
            string_rep += "\n"
        return string_rep

    def __repr__(self):
        rep = "Lattice("
        rep += repr(self.vectors.tolist())  + ","
        rep += repr(self.atoms)             + ")"
        return rep

    def __getitem__(self, item):
        return self.atoms[item]

    def __setitem__(self, key, value):
        self.atoms[key] = value

    def __delitem__(self, key):
        del(self.atoms[key])

    @property
    def vectors(self):
        return self._vectors

    @vectors.setter
    def vectors(self, vec):
        self._vectors = np.array(vec)

    @property
    def size(self):
        if self.vectors.ndim == 1:
            return np.linalg.norm(self.vectors)
        elif self.vectors.ndim == 2:
            if len(self.vectors) == 1:
                return np.linalg.norm(self.vectors[0])
            elif len(self.vectors) == 2:
                return self.vectors[0].dot(self.vectors[1])
            elif len(self.vectors) == 3:
                return np.cross(self.vectors[0], self.vectors[1]).dot(self.vectors[2])
        else:
            raise NotImplemented("Size property is not compatible with lattice vectors!")

    def sort(self, key=None, tolerance=None):
        """ Sort the lattice with a given key.

        :param key: sorting argument. Either "element", "position", "position_from_origin", "sublattice" for sorting
                    according to the corresponding :class:`.Atom` attribute or a function expression.
        :param tolerance: tolerance parameter which will be used when sorting this lattice with another lattice
                            (is not used when sorting with the keyword positions)
        :return: the sorted Lattice
        """
        if key is None:
            self.atoms.sort(key=lambda atom: (atom.element, atom.sublattice, atom.position))
        elif key == "element":
            self.atoms.sort(key=lambda atom: atom.element)
        elif key == "position":
            self.atoms.sort(key=lambda atom: self.distance(atom, [0.0, 0.0, 0.0]))
        elif key == "sublattice":
            self.atoms.sort(key=lambda atom: atom.sublattice)
        elif isinstance(key, Lattice):
            self._sort_with_other_lattice(key, tolerance)
        else:
            self.atoms.sort(key=key)
        return None

    def find(self, element=None, sublattice=None, position=None, tolerance=None, first=False):
        """ Get the atoms of the lattice with the specified element and/or sublattice

        :param element: element name of the atoms to get - ignored if not specified or None
        :param sublattice: sublattice name of the atoms to get - ignored if not specified or None
        :param position: position of the atoms to get (range comparison is done with constants.FRAC_VEC_COMP_TOL)
                        - ignored if not specified or None
        :return: list of :class:`Atoms <.Atom>`
        """
        def element_cond(atom):
            return True if element is None else atom.element == element

        def sublattice_cond(atom):
            return True if sublattice is None else atom.sublattice == sublattice

        def position_cond(atom, tol=tolerance):
            tol = constants.ABS_VEC_COMP_TOL if not tol else tol
            return True if position is None else self.distance(atom, position) < tol

        found_atoms = (atom for atom in self.atoms
                       if element_cond(atom)
                       and sublattice_cond(atom)
                       and position_cond(atom))

        if first is True:
            try:
                return next(found_atoms)
            except StopIteration:
                return None
        else:
            return list(found_atoms)

    def remove(self, atom: Atom):
        index = self.index(atom.position, tolerance=1e-10)
        del(self[index])
        return None

    def to_cartesian(self, position):
        position = getattr(position, "position", position)
        return self.vectors.dot(np.array(position))

    def to_fractional(self, position, periodic=True):
        frac_position = np.linalg.inv(self.vectors) @ position
        if periodic:
            return FractionalVector(frac_position).value
        else:
            return frac_position

    def get_in_radius(self, center: Union[np.array, list, Atom], max_radius, min_radius=0.0):
        """ Fetch a :class:`.Atom` from the stom list at the provided position

        :param min_radius: minimal radius, that is searched
        :param max_radius: maximal radius, that is seached
        :param center: Position of the searched :class:`.Atom`
        :return: :class:`.Atom` object
        """

        def condition(atom):
            return min_radius <= self.distance(atom, center) <= max_radius
        atom_list = [atom for atom in self.atoms if condition(atom)]
        atom_list.sort(key=lambda atom: self.distance(atom, center))
        return atom_list

    def index(self, position, tolerance=1e-3):
        """ Get the index of the :class:`.Atom` at the provided position

        :param position: Position or Atom whose index is searched for
        :param tolerance: Tolerance of fractional coordinates
        :return: int, index of :class:`.Atom`
        """
        position = getattr(position, "position", position)
        position = np.array(getattr(position, "value", position))
        for i in range(0, len(self.atoms)):
            if self.distance(self.atoms[i].position, position) < tolerance:
                return i
        return None

    def get_element_names(self):
        """ Get all occuring :attr:`Atom.element` names

        :return: List of strings
        """
        element_names = set()
        [element_names.add(x.element) for x in self.atoms]
        return list(element_names)

    def get_sublattice_names(self):
        """ Get all occuring :attr:`Atom.sublattice` names

        :return: List of strings
        """
        sublattice_names = set()
        [sublattice_names.add(x.sublattice) for x in self.atoms]
        return list(sublattice_names)

    def get_element_number_list(self):
        """Get a two dimensional list with the sort order of the elements within the lattice.

        The first column specifies the element name and the second column the number of adjacent atoms with this
        element. This information can be used for VASP Input files.
        For instance if the sort order of the atoms is as follows:

        X, X, Y, Y, Y, X, X

        (where X and Y are the elements of the atoms)
        the function would return the following table:

        =============  =============================
        Element Name   Number of repeating elements
        =============  =============================
        X              2
        Y              4
        X              2
        =============  =============================

        :return: two dimensional list - the first column is an int, the second a string

        Examples
        --------
        >>> #lattice = generate_from_crystal(ceria(),2,2,2).sort("position")
        >>> #print(lattice.get_element_number_list())
        [['Ce', 1], ['O', 1], ['Ce', 3], ['O', 7]]
        """
        element_number_list = []
        for atom in self.atoms:
            if not element_number_list:
                element_number_list.append([atom.element, 1])
            elif element_number_list[-1][0] == atom.element:
                element_number_list[-1][1] += 1
            else:
                element_number_list.append([atom.element, 1])
        return element_number_list

    def distance(self, position1, position2, periodic=True):
        """ Get the distance between two points

        :param position1: fractional coordinate as vector shaped container
        :param position2: fractional coordinate as vector shaped container
        :param periodic: bool, flag that indicates if the distance should be calculated under consideration of
                                periodic boundaries
        :return: float, distance in Angstrom
        """

        position1 = getattr(position1, "position", position1)
        position2 = getattr(position2, "position", position2)

        if periodic:
            position1 = FractionalVector(position1)
            position2 = FractionalVector(position2)
            diff_vector = position2.diff(position1)
        else:
            position1 = np.array(getattr(position1, "value", position1))
            position2 = np.array(getattr(position2, "value", position2))
            diff_vector = position2 - position1

        diff_vector_cartesian = diff_vector.dot(self.vectors)
        return np.sqrt(diff_vector_cartesian.dot(diff_vector_cartesian))

    def increase_distance_rel(self, center, position, rel_increase):

        # First check if atoms were passed to the function
        center = getattr(center, "position", center)
        position = getattr(position, "position", position)

        # Now convert the vectors to ensure periodicity
        center = FractionalVector(center)
        position = FractionalVector(position)

        # calculate the distance in fractional coordinates from center to position
        diff_vector = center.diff(position)

        # convert everything to cartesian coordinates
        center = self.vectors.dot(center.value)
        diff_vector = self.vectors.dot(diff_vector)

        # calculate the new position in cartesian coordinates
        new_position = center + diff_vector * (1+rel_increase)

        # convert the new position to fractional coordinates
        return FractionalVector(np.linalg.inv(self.vectors).dot(new_position))

    def increase_distance_abs(self, center, position, abs_increase):
        distance = self.distance(center, position)
        rel_distance = abs_increase/distance
        return self.increase_distance_rel(center, position, rel_distance)

    def diff(self, other, tolerance=None):
        """Compares the Atoms in this and the other lattice"""

        if not tolerance:
            tolerance = const.ABS_VEC_COMP_TOL

        self_not_found = []
        other_not_found = list(other.atoms)

        for atom1 in self:
            for atom2_id, atom2 in enumerate(other_not_found):
                if self._compare_atoms(atom1, atom2, tolerance):
                        del(other_not_found[atom2_id])
                        break
            else:
                self_not_found.append(atom1)

        return self_not_found, other_not_found

    def grid_atoms(self, grid_step):

        def to_grid(self, position, round_func):
            position = self.vectors @ position
            return tuple(int(x) for x in round_func(np.round(position / grid_step, 10)))

        grid_size = to_grid(self, np.array([1, 1, 1]), np.ceil)
        print(grid_size)
        print(np.round(self.vectors @ np.array([1, 1, 1]) / grid_step, 10))

        grid = [[[[] for _ in range(grid_size[2])]
                     for _ in range(grid_size[1])]
                     for _ in range(grid_size[0])]

        for atom in self:
            x, y, z = to_grid(self, atom.position, np.floor)
            grid[x][y][z].append(atom)
        return grid

    def _sort_with_other_lattice(self, other, tolerance=None):
        if not tolerance:
            tolerance = const.ABS_VEC_COMP_TOL

        old_order = list(self.atoms)
        new_order = []
        for atom1 in other:
            for atom2_id, atom2 in enumerate(old_order):
                if self._compare_atoms(atom1, atom2, tolerance):
                    new_order.append(atom2)
                    del(old_order[atom2_id])
        new_order += old_order
        self.atoms = new_order

    def _compare_atoms(self, atom1, atom2, dist_tolerance):
        if atom1.element != atom2.element:
            return False
        if atom1.sublattice != atom2.sublattice:
            return False
        if self.distance(atom1, atom2) > dist_tolerance:
            return False
        return True

    @staticmethod
    def from_lattice(lattice, size_x=1, size_y=1, size_z=1):
        new_lattice =  expand_lattice(lattice, size_x, size_y, size_z)
        new_lattice.sort("element")
        return new_lattice


def concat_lattices(lattice1: Lattice, lattice2: Lattice, direction: int):
    for i in range(lattice1.vectors.shape[0]):
        if i == direction:
            continue
        if not np.allclose(lattice1.vectors[i], lattice2.vectors[i], atol=1e-10):
            raise ValueError("shape of lattices does not match: "
                             "lattice1: {} lattice2: {}".format(str(lattice1.vectors[i]), lattice2.vectors[i]))
    new_lattice = Lattice(vectors=lattice1.vectors, atoms=[])
    new_lattice.vectors[direction] = lattice1.vectors[direction] + lattice2.vectors[direction]
    for atom in lattice1.atoms:
        new_atom = copy.copy(atom)
        new_atom.position = FractionalVector(atom.position.value.dot(lattice1.vectors).dot(np.linalg.inv(new_lattice.vectors)))
        new_lattice.atoms.append(new_atom)

    for atom in lattice2.atoms:
        new_atom = copy.copy(atom)
        shift = new_atom.position.value * 0
        shift[direction] = 1
        shift_cart = shift.dot(lattice1.vectors)
        new_position = new_atom.position.value.dot(lattice2.vectors) + shift_cart
        new_position = new_position.dot(np.linalg.inv(new_lattice.vectors))
        new_atom.position = FractionalVector(new_position)
        new_lattice.atoms.append(new_atom)

    return new_lattice


def expand_lattice(lattice, size_x, size_y, size_z):
    supercell_size = np.array([size_x, size_y, size_z])
    supercell_positions = []

    def reorientate_position(pos, x, y, z): return FractionalVector((pos + np.array([x, y, z])) / supercell_size)

    lattice_expansion = ((x, y, z) for x in range(size_x) for y in range(size_y) for z in range(size_z))
    supercell_positions += [Atom(element=atom.element,
                                 sublattice=atom.sublattice,
                                 position=reorientate_position(atom.position.value, *coord))
                            for coord in lattice_expansion for atom in lattice.atoms]

    lattice_vectors = lattice.vectors * supercell_size
    return Lattice(lattice_vectors, supercell_positions)
