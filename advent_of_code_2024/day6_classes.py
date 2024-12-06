from typing import NamedTuple
from enum import Enum
from dataclasses import dataclass, field


class Point(NamedTuple):
    x: int
    y: int
    char: str

class Obstacle(Point):
    ...

class MapEdge(Point):
    ...

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

@dataclass
class MapRow():
    point_list: list[Point]

    def get_point(self, x: int) -> Point:
        return self.point_list[x]

    @property
    def width(self):
        return len(self.point_list)

@dataclass
class Map():
    row_list: list[MapRow]

    @property
    def height(self):
        return len(self.row_list)

    @property
    def width(self):
        return self.row_list[0].width

    def get_row(self, y: int) -> MapRow:
        return self.row_list[y]

    def get_point(self, x: int, y: int) -> Point:
        row = self.row_list[y]
        return row.get_point(x)

    

@dataclass
class Guard():
    x: int
    y: int
    map: Map = field(repr=False)
    direction: Direction = field(repr=False)
    total_positions: int = field(default=1, repr=False)

    def rotate(self) -> None:
        new_value = (self.direction.value + 1) % 4
        self.direction = Direction(new_value)
        
    def find_next_point(self) -> Point:
        ''' Determine the next point based on current direction.  If next point is an obstacle, rotate and try again.'''
        current_x = self.x
        current_y = self.y
        match self.direction:
            case Direction.UP:
                next_point = self.map.get_point(current_x, current_y + 1)
            case Direction.RIGHT:
                next_point = self.map.get_point(current_x + 1, current_y)
            case Direction.DOWN:
                next_point = self.map.get_point(current_x, current_y - 1)
            case Direction.LEFT:
                next_point = self.map.get_point(current_x - 1, current_y)
                
        if isinstance(next_point, Obstacle):
            self.rotate()
            return self.find_next_point()
        else:
            return next_point

    def patrol(self) -> int:
        ''' If current position is an edge of the map, we're done, so return the total moves. 
        Otherwise, increment `total_positions`, move to the next position, and try again.'''
        if isinstance(self.position, MapEdge):
            return self.total_positions
        else:
            self.position = self.find_next_point()
            self.total_positions += 1
            return self.patrol()



if __name__ == '__main__':
    pass