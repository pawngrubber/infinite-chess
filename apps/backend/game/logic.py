from enum import IntEnum
from typing import Set

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

    def __eq__(self, other):
        if not isinstance(other, Coordinate):
            return False
        return self.ring == other.ring and self.slice == other.slice

    def __hash__(self):
        return hash((self.ring, self.slice))

    def __repr__(self):
        return f"{self.ring.name}{self.slice}"

def get_rook_moves(coord: Coordinate) -> Set[Coordinate]:
    moves = set()
    # Move along the ring (all other slices)
    for s in range(1, 19):
        if s != coord.slice:
            moves.add(Coordinate(coord.ring, s))
    # Move along the slice (all other rings)
    for r in Ring:
        if r != coord.ring:
            moves.add(Coordinate(r, coord.slice))
    return moves

def get_bishop_moves(coord: Coordinate) -> Set[Coordinate]:
    moves = set()
    # Diagonals move through both ring and slice
    for d in range(1, 18):
        # r + d, s + d
        if coord.ring.value + d <= Ring.D.value:
            moves.add(Coordinate(Ring(coord.ring.value + d), coord.slice + d))
            moves.add(Coordinate(Ring(coord.ring.value + d), coord.slice - d))
        # r - d, s + d
        if coord.ring.value - d >= Ring.A.value:
            moves.add(Coordinate(Ring(coord.ring.value - d), coord.slice + d))
            moves.add(Coordinate(Ring(coord.ring.value - d), coord.slice - d))
    return moves

def get_knight_moves(coord: Coordinate) -> Set[Coordinate]:
    moves = set()
    offsets = [
        (1, 2), (1, -2), (-1, 2), (-1, -2),
        (2, 1), (2, -1), (-2, 1), (-2, -1)
    ]
    for dr, ds in offsets:
        nr = coord.ring.value + dr
        if Ring.A.value <= nr <= Ring.D.value:
            moves.add(Coordinate(Ring(nr), coord.slice + ds))
    return moves

def get_queen_moves(coord: Coordinate) -> Set[Coordinate]:
    return get_rook_moves(coord) | get_bishop_moves(coord)

def get_king_moves(coord: Coordinate) -> Set[Coordinate]:
    moves = set()
    for dr in [-1, 0, 1]:
        for ds in [-1, 0, 1]:
            if dr == 0 and ds == 0:
                continue
            nr = coord.ring.value + dr
            if Ring.A.value <= nr <= Ring.D.value:
                moves.add(Coordinate(Ring(nr), coord.slice + ds))
    
    # Crossing logic: if at slice 8-11, King can step across the intersection
    # Slices 9 and 18 are physically crossing paths in the center
    if coord.slice == 9:
        moves.add(Coordinate(coord.ring, 18))
    elif coord.slice == 18:
        moves.add(Coordinate(coord.ring, 9))
        
    return moves

def get_pawn_moves(coord: Coordinate, direction: int) -> Set[Coordinate]:
    """ direction is 1 (forward) or -1 (backward) """
    moves = set()
    moves.add(Coordinate(coord.ring, coord.slice + direction))
    return moves
