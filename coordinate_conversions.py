def grid_coord_to_num_coord(coord: str):
    """
    Converts a grid co-ordinate into a numeric co-ordinate used to control movement
    """
    coord = coord.upper()

    column = ord(coord[0]) - 64
    row = int(coord[1])

    return (row * 10) + column

def grid_coord_to_index(coord: str):
    """
    Returns a tuple `(row, column)` for a given coordinate in the board matrix
    """
    row_index = [8 ,7, 6, 5, 4, 3, 2, 1]
    coord = coord.upper()

    row = row_index[int(coord[1]) - 1]
    column = ord(coord[0]) - 64

    return (row, column)

def num_coord_to_index(num_coord: int):
    
    row_index = [8 ,7, 6, 5, 4, 3, 2, 1]

    row = row_index[(num_coord // 10) - 1]
    column = num_coord % 10

    return (row, column)

def index_to_num_coord(row: int, column: int):
    pass