# /// script
# dependencies = [
#   "pytest",
# ]
# ///

import pytest
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from board.logic import Coordinate, Ring, get_rook_moves, get_bishop_moves, get_knight_moves, get_king_moves, get_pawn_moves

def test_coordinate_wrapping():
    c = Coordinate(Ring.A, 19)
    assert c.slice == 1
    c2 = Coordinate(Ring.B, 0)
    assert c2.slice == 18
    c3 = Coordinate(Ring.C, -1)
    assert c3.slice == 17

def test_coordinate_equality():
    assert Coordinate(Ring.A, 1) == Coordinate(Ring.A, 1)
    assert Coordinate(Ring.B, 18) == Coordinate(Ring.B, 0)
    assert Coordinate(Ring.C, 5) != Coordinate(Ring.D, 5)
    
def test_rook_moves():
    c = Coordinate(Ring.A, 1)
    moves = get_rook_moves(c)
    assert Coordinate(Ring.A, 2) in moves
    assert Coordinate(Ring.A, 18) in moves
    assert Coordinate(Ring.B, 1) in moves
    assert Coordinate(Ring.D, 1) in moves
    assert Coordinate(Ring.B, 2) not in moves
    # 17 slices in same ring + 3 rings in same slice = 20
    assert len(moves) == 20

def test_bishop_moves():
    c = Coordinate(Ring.B, 2)
    moves = get_bishop_moves(c)
    assert Coordinate(Ring.C, 3) in moves
    assert Coordinate(Ring.A, 1) in moves
    assert Coordinate(Ring.C, 1) in moves
    assert Coordinate(Ring.A, 3) in moves
    assert Coordinate(Ring.D, 4) in moves
    assert Coordinate(Ring.A, 2) not in moves

def test_knight_moves():
    c = Coordinate(Ring.B, 2)
    moves = get_knight_moves(c)
    assert Coordinate(Ring.C, 4) in moves
    assert Coordinate(Ring.A, 4) in moves
    assert Coordinate(Ring.D, 3) in moves
    assert Coordinate(Ring.C, 18) in moves  # B+1=C, 2-2=0->18
    assert Coordinate(Ring.A, 18) in moves  # B-1=A, 2-2=0->18
    # Test out of bounds rings
    assert Coordinate(Ring.A, 3) not in moves

def test_knight_wrapping_edge_case():
    c = Coordinate(Ring.A, 18)
    moves = get_knight_moves(c)
    # 18 + 2 = 20 -> 2
    assert Coordinate(Ring.B, 2) in moves
    # 18 + 1 = 19 -> 1
    assert Coordinate(Ring.C, 1) in moves

def test_king_moves():
    c = Coordinate(Ring.A, 9)
    moves = get_king_moves(c)
    # adjacent
    assert Coordinate(Ring.B, 9) in moves
    assert Coordinate(Ring.A, 8) in moves
    assert Coordinate(Ring.A, 10) in moves
    # crossing
    assert Coordinate(Ring.A, 18) in moves

def test_pawn_moves():
    c = Coordinate(Ring.A, 18)
    moves = get_pawn_moves(c, direction=1)
    assert Coordinate(Ring.A, 1) in moves
    
    c2 = Coordinate(Ring.A, 1)
    moves2 = get_pawn_moves(c2, direction=-1)
    assert Coordinate(Ring.A, 18) in moves2

def test_edge_case_ring_boundaries():
    # Rooks should not fall off the edge of rings A and D
    c = Coordinate(Ring.D, 5)
    moves = get_rook_moves(c)
    for m in moves:
        assert Ring.A.value <= m.ring.value <= Ring.D.value

    # Bishops should not exceed rings
    b_moves = get_bishop_moves(c)
    for m in b_moves:
        assert Ring.A.value <= m.ring.value <= Ring.D.value

def test_king_intersection_jump():
    # If king is at 18, it can jump to 9
    c = Coordinate(Ring.C, 18)
    moves = get_king_moves(c)
    assert Coordinate(Ring.C, 9) in moves
    assert Coordinate(Ring.C, 1) in moves
    assert Coordinate(Ring.C, 17) in moves

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
