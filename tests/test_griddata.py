import pytest
import gzip
import os

import griddata
from griddata import Grid

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
    format = 'map'
    grid = griddata.load(file, format='map')
    assert isinstance(grid, Grid)
    assert 0.375 == grid.spacing[0]
    origin = (-13.555, 2.445, 4.599)
    assert all([origin[i] == pytest.approx(grid.origin[i]) for i,_ in enumerate(grid.shape)])

def test_griddata_write_dx():
    file = autodockmap_file()
    format = 'map'
    grid = griddata.load(file, format='map')
    assert isinstance(grid, Grid)
    assert 0.375 == grid.spacing[0]
    origin = (-13.555, 2.445, 4.599)
    assert all([origin[i] == pytest.approx(grid.origin[i]) for i,_ in enumerate(grid.shape)])
    