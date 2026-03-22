# /// script
# dependencies = [
#   "pytest",
# ]
# ///

import pytest
import sys
import os

from board.logic import Coordinate, Ring
from board.board import Board, Piece, PieceType, Color
from board.testing import scenario, capture_board

@scenario(
    id="IC-001",
    name="Around The World Check",
    description="Test that a sliding piece (Rook) can attack the King from 'behind' by wrapping around the empty loop.",
    pass_condition="The Black King is reported as being 'In Check'."
)
def test_around_the_world_check():
    b = Board()
    b.turn = Color.BLACK
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.BLACK, PieceType.KING))
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.WHITE, PieceType.ROOK))
    capture_board(b)
    assert b.is_in_check(Color.BLACK)

@scenario(
    id="IC-002",
    name="Self Intersection",
    description="Test that a sliding piece does not count its own square as a move after a full lap.",
    pass_condition="No move end coordinate matches the start coordinate."
)
def test_self_intersection():
    b = Board()
    coord = Coordinate(Ring.A, 1)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.ROOK))
    capture_board(b)
    moves = b.get_pseudo_legal_moves(coord)
    for m in moves:
        assert m.end != coord

@scenario(
    id="IC-003",
    name="Pin Slide",
    description="Test that a Rook pinned along a ring CAN move along that same ring, but CANNOT step off it.",
    pass_condition="All legal moves for the Rook stay on Ring A."
)
def test_pin_slide():
    b = Board()
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.KING))
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 5), Piece(Color.BLACK, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 18), Piece(Color.WHITE, PieceType.PAWN)) # Block around-the-world check
    capture_board(b)
    
    legal_moves = b.get_legal_moves(Coordinate(Ring.A, 3))
    assert len(legal_moves) > 0
    for m in legal_moves:
        assert m.end.ring == Ring.A

@scenario(
    id="IC-004",
    name="En Passant",
    description="Test en passant capture logic on a curved track.",
    pass_condition="A move exists with the 'is_en_passant' flag set to true."
)
def test_en_passant():
    b = Board()
    b.turn = Color.WHITE
    b.add_piece(Coordinate(Ring.A, 4), Piece(Color.WHITE, PieceType.PAWN, direction=1))
    b.add_piece(Coordinate(Ring.B, 4), Piece(Color.BLACK, PieceType.PAWN, direction=-1))
    b.en_passant_target = Coordinate(Ring.B, 5)
    b.add_piece(Coordinate(Ring.D, 18), Piece(Color.WHITE, PieceType.KING))
    capture_board(b)
    
    moves = b.get_legal_moves(Coordinate(Ring.A, 4))
    assert any(m.end == Coordinate(Ring.B, 5) and m.is_en_passant for m in moves)

@scenario(
    id="IC-005",
    name="King Teleportation Check",
    description="Test King intersection jump check legality at the crossing slices 9 and 18.",
    pass_condition="The King can capture an unprotected piece across the intersection."
)
def test_king_teleportation_check():
    b = Board()
    b.turn = Color.WHITE
    b.add_piece(Coordinate(Ring.A, 9), Piece(Color.WHITE, PieceType.KING))
    b.add_piece(Coordinate(Ring.A, 18), Piece(Color.BLACK, PieceType.ROOK))
    capture_board(b)
    
    legal_moves = b.get_legal_moves(Coordinate(Ring.A, 9))
    assert any(m.end == Coordinate(Ring.A, 18) for m in legal_moves)

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
