# /// script
# dependencies = [
#   "pytest",
# ]
# ///

import pytest
import sys
import os

from board.logic import Coordinate, Ring
from board.board import Board, Piece, PieceType, Color, Move
from board.testing import scenario, capture_board

@scenario(
    
    name="Absolute Pin Diagonal",
    description="A piece pinned to the King diagonally can only move along that diagonal.",
    pass_condition="Legal moves for the pinned Bishop are restricted to the diagonal."
)
def test_absolute_pin_diagonal():
    b = Board()
    b.turn = Color.WHITE
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.KING))
    b.add_piece(Coordinate(Ring.B, 2), Piece(Color.WHITE, PieceType.BISHOP))
    b.add_piece(Coordinate(Ring.D, 4), Piece(Color.BLACK, PieceType.BISHOP))
    capture_board(b)

    moves = b.get_legal_moves(Coordinate(Ring.B, 2))
    ends = [m.end for m in moves]
    assert Coordinate(Ring.C, 3) in ends
    assert Coordinate(Ring.D, 4) in ends
    assert all(m.end.ring.value - Ring.A.value == m.end.slice - 1 for m in moves)

@scenario(
    
    name="Double Check Evasion",
    description="When in double check, the only legal move is for the King to move.",
    pass_condition="Non-King pieces have zero legal moves during a double check."
)
def test_double_check_forces_king_move():
    b = Board()
    b.turn = Color.WHITE
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.KING))
    b.add_piece(Coordinate(Ring.C, 1), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.BLACK, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.B, 2), Piece(Color.BLACK, PieceType.BISHOP))
    capture_board(b)
    
    rook_moves = b.get_legal_moves(Coordinate(Ring.C, 1))
    assert len(rook_moves) == 0
    king_moves = b.get_legal_moves(Coordinate(Ring.A, 1))
    assert len(king_moves) > 0

@scenario(
    
    name="Pinned Piece Power",
    description="A pinned piece still projects threat and can deliver check.",
    pass_condition="The enemy King is in check even if the checking piece is pinned."
)
def test_pinned_piece_projects_check():
    b = Board()
    b.turn = Color.BLACK
    b.add_piece(Coordinate(Ring.C, 3), Piece(Color.BLACK, PieceType.KING))
    b.add_piece(Coordinate(Ring.C, 6), Piece(Color.WHITE, PieceType.QUEEN))
    b.add_piece(Coordinate(Ring.B, 5), Piece(Color.WHITE, PieceType.KING))
    b.add_piece(Coordinate(Ring.D, 7), Piece(Color.BLACK, PieceType.BISHOP))
    capture_board(b)

    assert b.is_in_check(Color.BLACK)

@scenario(
    
    name="Around The World Advanced",
    description="Blocking one path of a loop check doesn't necessarily block the other.",
    pass_condition="King remains in check if only one direction of the loop is blocked."
)
def test_around_the_world_check_advanced():
    b = Board()
    b.turn = Color.WHITE
    b.add_piece(Coordinate(Ring.A, 5), Piece(Color.WHITE, PieceType.KING))
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.BLACK, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 4), Piece(Color.WHITE, PieceType.PAWN)) # Blocks short path
    capture_board(b)
    
    assert b.is_in_check(Color.WHITE)

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
