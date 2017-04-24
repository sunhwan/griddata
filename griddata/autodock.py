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

        self.paramfile = ''
        self.molecule = ''
        self.datafile = ''
        self.spacing = spacing
        self.npts = n_points
        self.center = center

        elements = []
        for _ in range(n_elements):
            elements.append(float(file.readline()))

        grid = Grid()
        grid.n_elements = n_elements
        grid.center = center
        grid.shape = shape
        grid.spacing = (spacing, spacing, spacing)
        grid.elements = elements
        return grid

    def meta(self):
        return _MAP_HEADER_TMPL.format(**self.__dict__)

    def save(self, file):
        """Writes to a file.

        Args:
            grid (:obj:`Grid`): Grid object.
            file (:obj:`file`): File object.
        """

        file.write(self.meta())
        for value in grid.elements:
            file.write("%.3f\n" % value)

    @staticmethod
    def write(grid, file):
        file.write(grid.meta())
        for value in grid.elements:
            file.write("%.3f\n" % value)
