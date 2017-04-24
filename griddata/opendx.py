"""OpenDX formatter"""

_DX_HEADER_TMPL = """object 1 class gridpositions counts {shape[0]} {shape[1]} {shape[2]}
origin {origin[0]:12.5e} {origin[1]:12.5e} {origin[2]:12.5e}
delta {spacing[0]:12.5e} 0 0
delta 0 {spacing[1]:12.5e} 0
delta 0 0 {spacing[2]:12.5e}
object 2 class gridconnections counts {shape[0]} {shape[1]} {shape[2]}
object 3 class array type double rank 0 items {n_elements} data follows
"""

_DX_FOOTER_TMPL = """attribute "dep" string "positions"
object "regular positions regular connections" class field
component "positions" value 1
component "connections" value 2
component "data" value 3
"""

class OpenDX(object):
    """OpenDX formatter"""

    @staticmethod
    def save(grid, file):
        """Writes to a file.

        Args:
            grid (:obj:`Grid`): Grid object.
            file (:obj:`file`): File object.
        """

        file.write(_DX_HEADER_TMPL.format( \
            shape=grid.shape, \
            origin=grid.origin, \
            spacing=grid.spacing, \
            n_elements=grid.n_elements \
        ))
        for i in range(grid.shape[0]):
            col = 0
            for j in range(grid.shape[1]):
                for k in range(grid.shape[2]):
                    idx = k*grid.shape[0]*grid.shape[1] + j*grid.shape[0] + i
                    file.write(" %12.5E" % grid.elements[idx])
                    col += 1
                    if col == 3:
                        file.write("\n")
                        col = 0
        if col != 0:
            file.write("\n")
        file.write(_DX_FOOTER_TMPL)
        file.close()
