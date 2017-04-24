import pytest
import gzip
import os

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
    format = 'map'
    grid = griddata.load(file, format='map')
    assert isinstance(grid, Grid)
    assert 0.375 == grid.spacing[0]
    origin = (-13.3675, 2.6325, 4.7865)
    print(grid.origin)
    assert all([origin[i] == pytest.approx(grid.origin[i]) for i,_ in enumerate(grid.shape)])

def test_griddata_sub():
    file = autodockmap_file()
    format = 'map'
    g = griddata.load(file, format='map')
    file.seek(0)
    h = griddata.load(file, format='map')
    gg = g - h
    assert all([0 == e for e in gg.elements])
