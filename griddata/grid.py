"""
Initialize grid format data and allow conversion between formats and
resampling of data
"""

from __future__ import division
import numpy as np
from scipy import interpolate
from scipy import ndimage

class Grid(object):
    """Grid data class that reads/converts grid-format data. Internally
    the elements are kept in C order.

    Args:
        file (:obj:`file`): File object to the file containing grid-format data.
        format (str): Grid-format data format.
    """

    ndim = None
    n_elements = None
    _shape = ()
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
            raise NotImplementedError

        n_elements = self.n_elements
        return self._elements.reshape(self.shape).ravel(order=order)

    @elements.setter
    def elements(self, elements):
<<<<<<< HEAD
        assert len(elements) == self.n_elements, '%d != %d' % (len(elements), self.n_elements)
=======
        if self.n_elements is not None:
            assert len(elements) == self.n_elements, f'{len(elements)} != {len(self.n_elements)}'
>>>>>>> c0fcf569fca1943180ef46d756a6269fe818dd98
        self.set_elements(elements)

    def set_elements(self, elements, order='C'):
        if order not in ('C', 'F'):
            raise NotImplementedError
        n_elements = len(elements)
        self._elements = np.array(elements).reshape(self.shape, order=order).ravel()

    @property
    def ndelements(self, order='C'):
        """Reshape the elements array into ndarray"""
        if order not in ('C', 'F'):
            raise NotImplementedError
        ndelements = self._elements.reshape(self.shape)
        if order == 'C':
            return ndelements
        return ndelements.ravel(order=order).reshape(self.shape, order=order)

    @property
    def center(self):
        if self._center is not None:
            return self._center
        try:
            ndim = self.ndim
            center = [None for _ in range(self.ndim)]
            for i in range(self.ndim):
                center[i] = self._origin[i] + int(float(self.shape[i])/2) * self.spacing[i]
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

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape):
        self._shape = shape
        self.ndim = len(shape)
        self.n_elements = np.cumprod(shape)[-1]

    def points(self, order='C'):
        if order not in ('C', 'F'):
            raise NotImplementedError
        origin = self.origin
        shape = self.shape
        spacing = self.spacing
        ix, iy, iz = [np.array([origin[i]+_*spacing[i] for _ in range(shape[i])]) for i in range(self.ndim)]
        Z = np.meshgrid(ix, iy, iz, indexing='ij')
        points = np.empty((self.n_elements, self.ndim), dtype=np.float)
        for i in range(self.ndim):
            points[:,i] = Z[i].reshape(1, self.n_elements, order=order)
        return points

    def reorient(self, shape, center, u, spacing=None, bounds_error=False, fill_value=0):
        if not spacing:
            spacing = self.spacing

        grid = Grid()
        grid.n_elements = np.cumprod(shape)[-1]
        grid.spacing = spacing
        grid.shape = shape
        grid.center = center

        # prepare for large array for storing the rotated map
        big_shape = np.max([self.shape, shape], axis=0)
        ndelements = np.zeros(big_shape)
        offset = [int((big_shape[0] - self.shape[0]) / 2.0),
                  int((big_shape[1] - self.shape[1]) / 2.0),
                  int((big_shape[2] - self.shape[2]) / 2.0)]
        ndelements[offset[0]:offset[0] + self.shape[0],
                   offset[1]:offset[1] + self.shape[1],
                   offset[2]:offset[2] + self.shape[2]] = self.ndelements

        # good introduction on affine transform
        # https://stackoverflow.com/a/20161742/532799
        c_in = 0.5 * np.array(ndelements.shape)
        c_out = 0.5 * np.array(ndelements.shape)
        offset = c_in - c_out.dot(u['rot'])

        new = ndimage.affine_transform(ndelements, u['rot'].T, offset=offset, order=3)
        offset = [int((big_shape[0] - shape[0]) / 2.0),
                  int((big_shape[1] - shape[1]) / 2.0),
                  int((big_shape[2] - shape[2]) / 2.0)]
        grid.elements = new[offset[0]:offset[0] + shape[0],
                            offset[1]:offset[1] + shape[1],
                            offset[2]:offset[2] + shape[2]].flatten()
        return grid

    def resample(self, shape, center, spacing=None, bounds_error=False, fill_value=0):
        if not spacing:
            spacing = self.spacing

        grid = Grid()
        grid.n_elements = np.cumprod(shape)[-1]
        grid.spacing = spacing
        grid.shape = shape
        grid.center = center
        points = [np.arange(self.origin[i], self.origin[i]+self.spacing[i]*self.shape[i], self.spacing[i]) for i in range(self.ndim)]
        g = interpolate.RegularGridInterpolator(points, self.ndelements, bounds_error=bounds_error, fill_value=fill_value)

        origin = grid.origin
        points = [np.arange(origin[i], origin[i]+shape[i]*spacing[i], spacing[i]) for i in range(self.ndim)]
        ndpoints = np.meshgrid(*points, indexing='ij')
        points = np.array([ndpoints[i].reshape(grid.n_elements) for i in range(self.ndim)]).T
        grid.elements = g(points)
        return grid

    def gaussian_filter(self, sigma=1.):
        grid = Grid()
        grid.n_elements = np.cumprod(self.shape)[-1]
        grid.spacing = self.spacing
        grid.shape = self.shape
        grid.center = self.center
        ndelements = ndimage.gaussian_filter(self.ndelements, sigma=sigma)
        grid.elements = ndelements.flatten()
        return grid

    def _gridcheck(self, h):
        """Validate grid h is same shape as the current grid"""
        if not isinstance(h, Grid):
            raise TypeError
        assert h.n_elements == self.n_elements
        assert h.spacing == self.spacing
        assert h.shape == self.shape

    def copy(self):
        grid = Grid()
        grid.n_elements = self.n_elements
        grid.spacing = self.spacing
        grid.shape = self.shape
        grid.origin = self.origin
        return grid

    def log(self):
        idx = ~(self.elements == 0)
        self.elements[idx] = np.log(self.elements[idx])
        return self

    def exp(self):
        self.elements = np.exp(self.elements)
        return self

    def __sub__(self, h):
        self._gridcheck(h)
        grid = self.copy()
        grid.elements = self.elements - h.elements
        return grid

    def __add__(self, h):
        self._gridcheck(h)
        grid = self.copy()
        grid.elements = self.elements + h.elements
        return grid

    def __mul__(self, factor):
        self.elements = self.elements * factor
        return self

    __rmul__ = __mul__

    def __truediv__(self, factor):
        self.elements = self.elements / factor
        return self

