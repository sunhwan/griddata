"""This module provides a package that can read/write grid data format"""

from .autodock import AutoDockMap
from .opendx import OpenDX

def load(file, format):
    """Load grid-format data

    Args:
        file (:obj:`file`): File object to the file containing grid-format data.
        format (str): Grid-format data format.
    """

    if format == 'map':
        reader = AutoDockMap()
        grid = reader.load(file)
        
    return grid

def save(grid, file, format):
    """Writes grid data to a file

    Args:
        grid (:obj:`Grid`): Grid object.
        file (:obj:`file`): File object.
        format (str): Grid-format data format.
    """

    if format == 'map':
        AutoDockMap.write(grid, file)

    if format == 'dx':
        OpenDX.write(grid, file)