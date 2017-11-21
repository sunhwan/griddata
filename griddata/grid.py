
"""Initialize grid format data and allow conversion between formats and resampling of data"""

import numpy as np

class Grid(object):
    """Grid data class that reads/converts grid-format data. Internally
    the elements are kept in C order.

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
    _center = None
    _elements = None

    def __init__(self):
        pass

    @property
    def elements(self):
        return self.get_elements()

    def get_elements(self, order='C'):
        """Return the elements in 1D array. The array is ordered in C-order."""
        if order not in ('C', 'F'):
            raise NotImplemented
        if order == 'F':
            return np.array(self._elements).reshape(self._shape).reshape(self.n_elements, order='F')
        return self._elements

    @elements.setter
    def elements(self, elements):
        self.set_elements(elements)

    def set_elements(self, elements, order='C'):
        if order not in ('C', 'F'):
            raise NotImplemented
        if order == 'F':
            n_elements = len(elements)
            shape = self.shape
            self._elements = np.array(elements).reshape(shape, order='F').reshape(n_elements)
        else:
            self._elements = np.array(elements)

    def ndelements(self, order='C'):
        """Reshape the elements array into ndarray"""
        if order not in ('C', 'F'):
            raise NotImplemented
        return self._elements.reshape(self.shape, order=order)

    @property
    def center(self):
        if self._center:
            return self._center

        try:
            ndim = self.ndim
            center = [None for _ in range(self.ndim)]
            for i in range(self.ndim):
                center[i] = self._origin[i] - int(float(self.shape[i])/2) * self.spacing[i]
            self._center = center
            return self._center
        except:
            raise ValueError

    @center.setter
    def center(self, center):
        self._center = center
        self.ndim = len(center)

    @property
    def origin(self):
        if self._origin:
            return self._origin

        try:
            ndim = self.ndim
            _origin = [None for _ in range(self.ndim)]
            for i in range(self.ndim):
                _origin[i] = self._center[i] - int(float(self.shape[i])/2) * self.spacing[i]
            self._origin = _origin
            return self._origin
        except:
            raise ValueError

    @origin.setter
    def origin(self, origin):
        self._origin = origin
        self.ndim = len(origin)

    def points(self, order='C'):
        if order not in ('C', 'F'):
            raise NotImplemented
        origin = self.origin
        shape = self.shape
        spacing = self.spacing
        ix, iy, iz = [np.array([origin[i]+_*spacing[i] for _ in range(shape[i])]) for i in range(self.ndim)]
        Z = np.meshgrid(ix, iy, iz, indexing='ij')
        points = np.empty((self.n_elements, self.ndim), dtype=np.float)
        for i in range(self.ndim):
            points[:,i] = Z[i].reshape(1, self.n_elements, order=order)
        return points

    def _gridcheck(self, h):
        """Validate grid h is same shape as the current grid"""
        if not isinstance(h, Grid):
            raise TypeError

        assert h.n_elements == self.n_elements
        assert h.spacing == self.spacing
        assert h.shape == self.shape

    def __sub__(self, h):
        self._gridcheck(h)
        grid = Grid()
        grid.n_elements = self.n_elements
        grid.spacing = self.spacing
        grid.elements = self.elements - h.elements
        grid.shape = self.shape
        grid.origin = self.origin
        return grid

    def __add__(self, h):
        self._gridcheck(h)
        grid = Grid()
        grid.n_elements = self.n_elements
        grid.spacing = self.spacing
        grid.elements = self.elements + h.elements
        grid.shape = self.shape
        grid.origin = self.origin
        return grid

    def __truediv__(self, n):
        self._gridcheck(h)
        grid = Grid()
        grid.n_elements = self.n_elements
        grid.spacing = self.spacing
        grid.elements = self.elements / n
        grid.shape = self.shape
        grid.origin = self.origin
        return grid
