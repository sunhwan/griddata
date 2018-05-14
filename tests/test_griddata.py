import pytest
import gzip
import os
import numpy as np

import griddata
from griddata.grid import Grid

@pytest.fixture
def autodockmap_file():
    fixture_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    return gzip.open(os.path.join(fixture_dir, '3ptb.map.gz'))

@pytest.fixture
def opendx_file():
    fixture_dir = os.path.join(os.path.dirname(__file__), 'fixtures')
    return gzip.open(os.path.join(fixture_dir, '3ptb.dx.gz'))

def test_griddata_map():
    file = autodockmap_file()
    grid = griddata.load(file, format='map')
    assert isinstance(grid, Grid)
    assert 0.375 == grid.spacing[0]
    origin = (-13.18, 2.82, 4.974)
    assert all([origin[i] == pytest.approx(grid.origin[i]) for i,_ in enumerate(grid.shape)])

def test_griddata_dx():
    file = opendx_file()
    grid = griddata.load(file, format='dx')
    assert isinstance(grid, Grid)
    assert 0.375 == grid.spacing[0]
    origin = (-13.555, 2.445, 4.599)
    assert all([origin[i] == pytest.approx(grid.origin[i]) for i,_ in enumerate(grid.shape)])
    center = ( -24.805, -8.805, -6.651 )
    assert all([center[i] == pytest.approx(grid.center[i]) for i,_ in enumerate(grid.shape)])

def test_griddata_sub():
    file = autodockmap_file()
    g = griddata.load(file, format='map')
    file.seek(0)
    h = griddata.load(file, format='map')
    gg = g - h
    assert all([0 == e for e in gg.elements])

    file = opendx_file()
    h = griddata.load(file, format='dx')
    gg = g - h
    assert sum([abs(d) > abs( h.elements[i] * 0.001 ) for i,d in enumerate(gg.elements)]) == 0

def test_griddata_points():
    file = autodockmap_file()
    grid = griddata.load(file, format='map')
    origin = np.array((-13.18, 2.82, 4.974))
    points = grid.points(order='F')
    np.testing.assert_array_almost_equal(points[0], origin)

    vec = np.array([grid.spacing[0], 0, 0])
    np.testing.assert_array_almost_equal(points[1], origin + vec)

    vec = np.array([0, grid.spacing[0], 0])
    np.testing.assert_array_almost_equal(points[grid.shape[0]], origin + vec)

    vec = np.array([0, 0, grid.spacing[0]])
    np.testing.assert_array_almost_equal(points[grid.shape[0]*grid.shape[1]], origin + vec)

def test_resample():
    file = autodockmap_file()
    g = griddata.load(file, format='map')
    h = g.resample(center=g.center, shape=g.shape)
    gg = g - h
    assert all([0 == e for e in gg.elements])

    shape = [_-2 for _ in g.shape]
    h = g.resample(center=g.center, shape=shape)
    gg = g.ndelements[1:-1, 1:-1, 1:-1] - h.ndelements
    assert 0 == np.sum(gg)

def test_gaussian_filter():
    file = autodockmap_file()
    g = griddata.load(file, format='map')
    h = g.gaussian_filter(sigma=0)
    gg = g - h
    assert all([0 == e for e in gg.elements])

    h = g.gaussian_filter(sigma=0.1)
    gg = g - h
    elements = [gg.elements[i]/e*100 for i,e in enumerate(g.elements) if e > 0]
    # catching changes bigger than 1%
    assert all([1.0 > np.abs(e) for e in elements])
