"""Initialize grid format data and allow conversion between formats and resampling of data"""

import numpy as np

class Grid(object):
    """Grid data class that reads/converts grid-format data.

    Args:
        file (:obj:`file`): File object to the file containing grid-format data.
        format (str): Grid-format data format.
    """

    ndim = None
    n_elements = 0
    shape = ()
    spacing = ()
    _origin = None
    _center = None
    _elements = None

    def __init__(self):
        pass

    @property
    def elements(self):
        return self._elements

    @elements.setter
    def elements(self, elements):
        self._elements = np.array(elements)

    @property
    def center(self):
        if self._center:
            return self._center

    @center.setter
    def center(self, center):
        self._center = center
        self.ndim = len(center)

    @property
    def origin(self):
        if self._origin:
            return self._origin

        ndim = self.ndim
        origin = [None for _ in range(self.ndim)]
        for i in range(self.ndim):
            origin[i] = self._center[i] - int(float(self.shape[i])/2) * self.spacing[i] - self.spacing[i] / 2
        self._origin = origin
        return self._origin

    @origin.setter
    def origin(self, origin):
        self._origin = origin

    def __sub__(self, h):
        if not isinstance(h, Grid):
            raise TypeError

        assert h.n_elements == self.n_elements
        assert h.spacing == self.spacing
        assert h.shape == self.shape

        grid = Grid()
        grid.n_elements = self.n_elements
        grid.spacing = self.spacing
        grid.elements = self.elements - h.elements
        grid.shape = self.shape
        grid.origin = self.origin
        return grid
