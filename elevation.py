"""Assignment 2 functions."""
from typing import List
import math

THREE_BY_THREE = [[1, 2, 1],
                  [4, 6, 5],
                  [7, 8, 9]]

FOUR_BY_FOUR = [[1, 2, 6, 5],
                [4, 5, 3, 2],
                [7, 9, 8, 1],
                [1, 2, 1, 4]]

UNIQUE_3X3 = [[1, 2, 3],
              [9, 8, 7],
              [4, 5, 6]]

UNIQUE_4X4 = [[10, 2, 3, 30],
              [9, 8, 7, 11],
              [4, 5, 6, 12],
              [13, 14, 15, 16]]


def compare_elevations_within_row(elevation_map: List[List[int]], map_row: int,
                                  level: int) -> List[int]:
    """Return a new list containing the three counts: the number of
    elevations from row number map_row of elevation map elevation_map
    that are less than, equal to, and greater than elevation level.

    Precondition: elevation_map is a valid elevation map.
                  0 <= map_row < len(elevation_map).

    >>> compare_elevations_within_row(THREE_BY_THREE, 1, 5)
    [1, 1, 1]
    >>> compare_elevations_within_row(FOUR_BY_FOUR, 1, 2)
    [0, 1, 3]

    """
    three_items = [0, 0, 0]
    for num in elevation_map[map_row]:
        if num < level:
            three_items[0] += 1
        elif num == level:
            three_items[1] += 1
        elif num > level:
            three_items[2] += 1
    return three_items


def update_elevation(elevation_map: List[List[int]], start: List[int],
                     stop: List[int], delta: int) -> None:
    """Modify elevation map elevation_map so that the elevation of each
    cell between cells start and stop, inclusive, changes by amount
    delta.

    Precondition: elevation_map is a valid elevation map.
                  start and stop are valid cells in elevation_map.
                  start and stop are in the same row or column or both.
                  If start and stop are in the same row,
                      start's column <=  stop's column.
                  If start and stop are in the same column,
                      start's row <=  stop's row.
                  elevation_map[i, j] + delta >= 1
                      for each cell [i, j] that will change.

    >>> THREE_BY_THREE_COPY = [[1, 2, 1],
    ...                        [4, 6, 5],
    ...                        [7, 8, 9]]
    >>> update_elevation(THREE_BY_THREE_COPY, [1, 0], [1, 1], -2)
    >>> THREE_BY_THREE_COPY
    [[1, 2, 1], [2, 4, 5], [7, 8, 9]]
    >>> FOUR_BY_FOUR_COPY = [[1, 2, 6, 5],
    ...                      [4, 5, 3, 2],
    ...                      [7, 9, 8, 1],
    ...                      [1, 2, 1, 4]]
    >>> update_elevation(FOUR_BY_FOUR_COPY, [1, 2], [3, 2], 1)
    >>> FOUR_BY_FOUR_COPY
    [[1, 2, 6, 5], [4, 5, 4, 2], [7, 9, 9, 1], [1, 2, 2, 4]]

    """
    start_row = start[0]
    start_col = start[1]
    stop_row = stop[0]
    stop_col = stop[1]
    
    for i in range(start_row, stop_row + 1):
        for j in range(start_col, stop_col + 1):
            elevation_map[i][j] += delta
            
            
def get_average_elevation(elevation_map: List[List[int]]) -> float:
    """Return the average elevation across all cells in the elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.

    >>> get_average_elevation(UNIQUE_3X3)
    5.0
    >>> get_average_elevation(FOUR_BY_FOUR)
    3.8125
    """
    count = 0
    total = 0
    for i in elevation_map:
        for j in i:
            count += 1
            total += j
    return total / count


def find_peak(elevation_map: List[List[int]]) -> List[int]:
    """Return the cell that is the highest point in the elevation map
    elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  Every elevation value in elevation_map is unique.

    >>> find_peak(UNIQUE_3X3)
    [1, 0]
    >>> find_peak(UNIQUE_4X4)
    [0, 3]
    """
    row = 0
    col = 0
    for i in range(len(elevation_map)):
        for j in range(len(elevation_map[i])):
            if elevation_map[i][j] > elevation_map[row][col]:
                row = i
                col = j
    return [row, col]


def is_valid_cell(elevation_map: List[List[int]], cell: List[int])-> bool:
    """Return True if and only if cell exists in the elevation map
    
    Precondition: elevation_map is a valid elevation map.
                  cell is a 2-element list.
                  
    >>> is_valid_cell(THREE_BY_THREE, [0, 0])
    True
    >>> is_valid_cell(FOUR_BY_FOUR, [2, 7])
    False
    """
    row = cell[0]
    col = cell[1]
    length = len(elevation_map)
    return 0 <= row < length and 0 <= col < length


def is_sink(elevation_map: List[List[int]], cell: List[int]) -> bool:
    """Return True if and only if cell exists in the elevation map
    elevation_map and cell is a sink.

    Precondition: elevation_map is a valid elevation map.
                  cell is a 2-element list.

    >>> is_sink(THREE_BY_THREE, [0, 5])
    False
    >>> is_sink(THREE_BY_THREE, [0, 2])
    True
    >>> is_sink(THREE_BY_THREE, [1, 1])
    False
    >>> is_sink(FOUR_BY_FOUR, [2, 3])
    True
    >>> is_sink(FOUR_BY_FOUR, [3, 2])
    True
    >>> is_sink(FOUR_BY_FOUR, [1, 3])
    False
    """
    row = cell[0]
    col = cell[1]
    if not is_valid_cell(elevation_map, cell):
        return False
    for i in range(-1, 2):
        for j in range(-1, 2):
            if is_valid_cell(elevation_map, [row + i, col + j]) and \
               elevation_map[row][col] > elevation_map[row + i][col + j]:
                return False
    return True
    

def find_local_sink(elevation_map: List[List[int]],
                    cell: List[int]) -> List[int]:
    """Return the local sink of cell cell in elevation map elevation_map.

    Precondition: elevation_map is a valid elevation map.
                  elevation_map contains no duplicate elevation values.
                  cell is a valid cell in elevation_map.

    >>> find_local_sink(UNIQUE_3X3, [1, 1])
    [0, 0]
    >>> find_local_sink(UNIQUE_3X3, [2, 0])
    [2, 0]
    >>> find_local_sink(UNIQUE_4X4, [1, 3])
    [0, 2]
    >>> find_local_sink(UNIQUE_4X4, [2, 2])
    [2, 1]
    """
    row = cell[0]
    col = cell[1]
    lowest = [row, col]
    for i in range(-1, 2):
        for j in range(-1, 2):
            new_cell = [row + i, col + j]
            if is_valid_cell(elevation_map, new_cell) and \
               cell != new_cell and \
               elevation_map[lowest[0]][lowest[1]] >= \
               elevation_map[row + i][col + j]:
                lowest = new_cell
    return lowest


def can_hike_to(elevation_map: List[List[int]], start: List[int],
    dest: List[int], supplies: int) -> bool:
    """Return True if and only if a hiker can go from start to dest in
    elevation_map without running out of supplies.

    Precondition: elevation_map is a valid elevation map.
                  start and dest are valid cells in elevation_map.
                  dest is North-West of cur.
                  supplies >= 0

    >>> map = [[1, 6, 5, 6],
    ...        [2, 5, 6, 8],
    ...        [7, 2, 8, 1],
    ...        [4, 4, 7, 3]]
    >>> can_hike_to(map, [3, 3], [2, 2], 10)
    True
    >>> can_hike_to(map, [3, 3], [2, 2], 8)
    False
    >>> can_hike_to(map, [3, 3], [3, 0], 7)
    True
    >>> can_hike_to(map, [3, 3], [3, 0], 6)
    False
    >>> can_hike_to(map, [3, 3], [0, 0], 18)
    True
    >>> can_hike_to(map, [3, 3], [0, 0], 17)
    False

    """
    cur_row = start[0]
    cur_col = start[1]
    dest_row = dest[0]
    dest_col = dest[1]
    while  cur_row > dest_row and cur_col > dest_col and supplies > 0:
        north_supplies = elevation_map[cur_row - 1][cur_col]
        west_supplies = elevation_map[cur_row][cur_col - 1]
        diff_north = abs(elevation_map[cur_row][cur_col] - north_supplies)
        diff_west = abs(elevation_map[cur_row][cur_col] - west_supplies)
        if diff_west < diff_north:
            supplies -= diff_west
            cur_col -= 1
        elif diff_west >= diff_north:
            supplies -= diff_north
            cur_row -= 1
    if cur_col == dest_col and supplies > 0:
        while cur_row > dest_row:
            north_supplies = elevation_map[cur_row - 1][cur_col]
            diff_north = abs(elevation_map[cur_row][cur_col] - north_supplies)
            supplies -= diff_north
            cur_row -= 1
    elif cur_row == dest_row and supplies > 0:
        while cur_col > dest_col and supplies >= 0:
            west_supplies = elevation_map[cur_row][cur_col - 1]
            diff_west = abs(elevation_map[cur_row][cur_col] - west_supplies)
            supplies -= diff_west
            cur_col -= 1
    return cur_col == dest_col and cur_row == dest_row and supplies >= 0 
    

def get_lower_resolution(elevation_map: List[List[int]]) -> List[List[int]]:
    """Return a new elevation map, which is constructed from the values
    of elevation_map by decreasing the number of elevation points
    within it.

    Precondition: elevation_map is a valid elevation map.
    
    >>> get_lower_resolution(
    ...     [[1, 6, 5, 6],
    ...      [2, 5, 6, 8],
    ...      [7, 2, 8, 1],
    ...      [4, 4, 7, 3]])
    [[3, 6], [4, 4]]
    >>> get_lower_resolution(
    ...     [[7, 9, 1],
    ...      [4, 2, 1],
    ...      [3, 2, 3]])
    [[5, 1], [2, 3]]

    """
    acc = []
    inner = []
    length = len(elevation_map)
    if length == 1 or length == 0:
        return elevation_map
    elif length == 2:
        acc.append([math.floor(get_average_elevation(elevation_map))])
        return acc
    for i in range(0, length, 2):
        for j in range(0, length, 2):
            temp = [elevation_map[i][j]]
            if i + 1 < length and j + 1 < length:
                temp.extend([elevation_map[i][j + 1], elevation_map[i + 1][j], \
                             elevation_map[i + 1][j + 1]])
            elif j + 1 < length:
                temp.extend([elevation_map[i][j + 1]])
            elif i + 1 < length:
                temp.extend([elevation_map[i + 1][j]])
            acc.append(sum(temp) // len(temp))
        inner.append(acc)
        acc = []
    return inner