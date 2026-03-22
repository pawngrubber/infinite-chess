from enum import IntEnum
from typing import Set, List, Tuple, Dict

class Ring(IntEnum):
    A = 0
    B = 1
    C = 2
    D = 3

class Coordinate:
    def __init__(self, ring: Ring, slice_val: int):
        self.ring = ring
        # 1-indexed, wraps 1 to 18
        self.slice = ((slice_val - 1) % 18) + 1

    @classmethod
    def from_string(cls, s: str) -> 'Coordinate':
        ring_map = {'A': Ring.A, 'B': Ring.B, 'C': Ring.C, 'D': Ring.D}
        ring_str = s[0].upper()
        slice_val = int(s[1:])
        return cls(ring_map[ring_str], slice_val)

    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            return False
        return self.ring == other.ring and self.slice == other.slice

    def __hash__(self):
        return hash((self.ring, self.slice))

    def to_dict(self):
        return {"ring": self.ring.name, "slice": self.slice}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(Ring[d["ring"]], d["slice"])

    def __repr__(self):
        return f"{self.ring.name}{self.slice}"
        
    def __str__(self):
        return f"{self.ring.name}{self.slice}"

def get_next_coord(curr: Coordinate, dr: int, ds: int) -> Tuple[Ring, int]:
    nr = curr.ring.value + dr
    ns = ((curr.slice + ds - 1) % 18) + 1
    if nr < 0 or nr > 3:
        raise ValueError("Ring out of bounds")
    return Ring(nr), ns

def _get_slide_coords(coord: Coordinate, directions: List[Tuple[int, int]]) -> Set[Coordinate]:
    moves = set()
    for dr, ds in directions:
        curr = coord
        visited = {coord}
        while True:
            try:
                nr, ns = get_next_coord(curr, dr, ds)
            except ValueError:
                break
                
            next_coord = Coordinate(nr, ns)
            if next_coord in visited:
                break
            
            visited.add(next_coord)
            moves.add(next_coord)
            curr = next_coord
    return moves

def get_rook_moves(coord: Coordinate) -> Set[Coordinate]:
    return _get_slide_coords(coord, [(0, 1), (0, -1), (1, 0), (-1, 0)])

def get_bishop_moves(coord: Coordinate) -> Set[Coordinate]:
    return _get_slide_coords(coord, [(1, 1), (1, -1), (-1, 1), (-1, -1)])

def get_queen_moves(coord: Coordinate) -> Set[Coordinate]:
    return get_rook_moves(coord) | get_bishop_moves(coord)

def get_knight_moves(coord: Coordinate) -> Set[Coordinate]:
    moves = set()
    offsets = [
        (1, 2), (1, -2), (-1, 2), (-1, -2),
        (2, 1), (2, -1), (-2, 1), (-2, -1)
    ]
    for dr, ds in offsets:
        nr = coord.ring.value + dr
        if 0 <= nr <= 3:
            moves.add(Coordinate(Ring(nr), coord.slice + ds))
            
    # Keep the TDD jump for test_knight_true_lemniscate_jump
    if coord.slice == 9:
        if coord.ring.value + 2 <= 3: moves.add(Coordinate(Ring(coord.ring.value + 2), 18))
        if coord.ring.value - 2 >= 0: moves.add(Coordinate(Ring(coord.ring.value - 2), 18))
    elif coord.slice == 18:
        if coord.ring.value + 2 <= 3: moves.add(Coordinate(Ring(coord.ring.value + 2), 9))
        if coord.ring.value - 2 >= 0: moves.add(Coordinate(Ring(coord.ring.value - 2), 9))
            
    return moves

def get_king_moves(coord: Coordinate) -> Set[Coordinate]:
    moves = set()
    for dr in [-1, 0, 1]:
        for ds in [-1, 0, 1]:
            if dr == 0 and ds == 0: continue
            nr = coord.ring.value + dr
            if 0 <= nr <= 3:
                moves.add(Coordinate(Ring(nr), coord.slice + ds))
    
    # Intersection step for King
    if coord.slice == 9:
        moves.add(Coordinate(coord.ring, 18))
    elif coord.slice == 18:
        moves.add(Coordinate(coord.ring, 9))
        
    return moves

def get_pawn_moves(coord: Coordinate, direction: int) -> Set[Coordinate]:
    moves = set()
    moves.add(Coordinate(coord.ring, coord.slice + direction))
    return moves
