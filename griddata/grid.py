"""Initialize grid format data and allow conversion between formats and resampling of data"""

class Grid(object):
    """Grid data class that reads/converts grid-format data.

    Args:
        file (:obj:`file`): File object to the file containing grid-format data.
        format (str): Grid-format data format.
    """

    n_elements = 0
    shape = ()
    origin = ()
    spacing = ()
    elements = []
