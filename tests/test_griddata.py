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
    return gzip.open(os.path.join(fixture_dir, '3ptbdx.gz'))

def test_griddata_map():
    file = autodockmap_file()
    grid = griddata.load(file, format='map')
    assert isinstance(grid, Grid)
    assert 0.375 == grid.spacing[0]
    origin = (-13.3675, 2.6325, 4.7865)
    assert all([origin[i] == pytest.approx(grid.origin[i]) for i,_ in enumerate(grid.shape)])

def test_griddata_sub():
    file = autodockmap_file()
    g = griddata.load(file, format='map')
    file.seek(0)
    h = griddata.load(file, format='map')
    gg = g - h
    assert all([0 == e for e in gg.elements])

def test_griddata_points():
    file = autodockmap_file()
    grid = griddata.load(file, format='map')
    origin = np.array((-13.3675, 2.6325, 4.7865))
    points = grid.points()
    np.testing.assert_array_almost_equal(points[0], origin)

    vec = np.array([grid.spacing[0], 0, 0])
    np.testing.assert_array_almost_equal(points[1], origin + vec)

    vec = np.array([0, grid.spacing[0], 0])
    np.testing.assert_array_almost_equal(points[grid.shape[0]], origin + vec)

    vec = np.array([0, 0, grid.spacing[0]])
    np.testing.assert_array_almost_equal(points[grid.shape[0]*grid.shape[1]], origin + vec)
