"""AutoDock Grid Map read and write"""
from __future__ import print_function

from .grid import Grid

_MAP_HEADER_TMPL = """GRID_PARAMETER_FILE {paramfile}
GRID_DATA_FILE {datafile}
MACROMOLECULE {molecule}
SPACING {spacing:4.3f}
NELEMENTS {npts[0]} {npts[1]} {npts[2]}
CENTER {center[0]:5.3f} {center[1]:5.3f} {center[2]:5.3f}
"""

class AutoDockMap(object):
    """Class for handling AutoDock Map files"""

    def load(self, file):
        """Load grid format file

        Args:
            file (:obj:`file`): File object.
        """

        header = []
        for _ in range(6):
            line = file.readline()
            header.append(line.strip())

        paramfile = header[0]
        datafile = header[1]
        molecule = header[2]
        spacing = float(header[3].split()[1])
        n_points = [int(_) for _ in header[4].split()[1:]]
        center = [float(_) for _ in header[5].split()[1:]]
        shape = [n_points[i]+1 for i in range(3)]
        n_elements = shape[0] * shape[1] * shape[2]

        elements = []
        for _ in range(n_elements):
            elements.append(float(file.readline()))

        grid = Grid()
        grid.n_elements = n_elements
        grid.spacing = (spacing, spacing, spacing)
        grid.elements = elements

        origin = []
        for i in range(3):
            origin[i] = center[i] - (float(n_points[i])/2 + 1) * spacing
        grid.origin = origin
        return grid

    def meta(self):
        return _MAP_HEADER_TMPL.format(**self.__dict__)

    @staticmethod
    def save(grid, file):
        """Writes to a file.

        Args:
            grid (:obj:`Grid`): Grid object.
            file (:obj:`file`): File object.
        """

        file.write(grid.meta())
        for value in grid.values:
            if abs(value) < grid.precision:
                file.write("0.\n")
            else:
                file.write("%.3f\n" % value)