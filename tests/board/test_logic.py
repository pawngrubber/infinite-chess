# /// script
# dependencies = [
#   "pytest",
# ]
# ///

import pytest
import sys
import os

from board.logic import Coordinate, Ring, get_rook_moves, get_bishop_moves, get_knight_moves, get_king_moves, get_pawn_moves
from board.board import Board, Piece, PieceType, Color
from board.testing import scenario, capture_board

@scenario(
    
    name="Rook Movement Geometry",
    description="Test that Rooks move along rings and slices on an empty board.",
    pass_condition="Rook moves to adjacent rings and wraps around the same ring."
)
def test_rook_moves():
    b = Board()
    c = Coordinate(Ring.A, 1)
    b.add_piece(c, Piece(Color.WHITE, PieceType.ROOK))
    capture_board(b)
    moves = get_rook_moves(c)
    assert Coordinate(Ring.A, 2) in moves
    assert Coordinate(Ring.A, 18) in moves
    assert Coordinate(Ring.B, 1) in moves
    assert Coordinate(Ring.D, 1) in moves

@scenario(
    
    name="Bishop Diagonal Geometry",
    description="Test that Bishops move along diagonals, changing both ring and slice.",
    pass_condition="Bishop moves diagonally to adjacent rings and slices."
)
def test_bishop_moves():
    b = Board()
    c = Coordinate(Ring.B, 2)
    b.add_piece(c, Piece(Color.WHITE, PieceType.BISHOP))
    capture_board(b)
    moves = get_bishop_moves(c)
    assert Coordinate(Ring.C, 3) in moves
    assert Coordinate(Ring.A, 1) in moves
    assert Coordinate(Ring.C, 1) in moves

@scenario(
    
    name="Knight L-Shape Jumps",
    description="Test Knight movement on the curved manifold.",
    pass_condition="Knight performs valid L-shaped jumps, including wrapping."
)
def test_knight_moves():
    b = Board()
    c = Coordinate(Ring.B, 2)
    b.add_piece(c, Piece(Color.WHITE, PieceType.KNIGHT))
    capture_board(b)
    moves = get_knight_moves(c)
    assert Coordinate(Ring.C, 4) in moves
    assert Coordinate(Ring.A, 4) in moves
    assert Coordinate(Ring.C, 18) in moves

@scenario(
    
    name="King Intersect Jump",
    description="Test King movement across the physical intersection (Slice 9 to 18).",
    pass_condition="King can jump directly from Slice 9 to Slice 18."
)
def test_king_moves():
    b = Board()
    c = Coordinate(Ring.A, 9)
    b.add_piece(c, Piece(Color.WHITE, PieceType.KING))
    capture_board(b)
    moves = get_king_moves(c)
    assert Coordinate(Ring.A, 18) in moves

@scenario(
    
    name="Pawn Forward Step",
    description="Test Pawn movement following the loop direction.",
    pass_condition="Pawn moves one step forward and wraps correctly."
)
def test_pawn_moves():
    b = Board()
    c = Coordinate(Ring.A, 18)
    b.add_piece(c, Piece(Color.WHITE, PieceType.PAWN, direction=1))
    capture_board(b)
    moves = get_pawn_moves(c, direction=1)
    assert Coordinate(Ring.A, 1) in moves

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
