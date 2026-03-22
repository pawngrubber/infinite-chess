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
    id="IC-PAWN-001",
    name="Pawn Direction Towards Center",
    description="Pawns must move towards the center crossing (Slices 9/18). White pawns from 9-12 move -1, while those from 14-17 move +1.",
    pass_condition="Pawns only generate moves in their assigned direction towards the crossing."
)
def test_pawn_direction_towards_center():
    b = Board()
    # White pawn in the 14-17 bracket (should move +1 towards 18)
    p1 = Piece(Color.WHITE, PieceType.PAWN, direction=1)
    b.add_piece(Coordinate(Ring.B, 14), p1)
    
    # White pawn in the 9-12 bracket (should move -1 towards 9)
    p2 = Piece(Color.WHITE, PieceType.PAWN, direction=-1)
    b.add_piece(Coordinate(Ring.B, 12), p2)
    
    capture_board(b)
    
    moves1 = b.get_pseudo_legal_moves(Coordinate(Ring.B, 14))
    assert all(m.end.slice == 15 for m in moves1)
    
    moves2 = b.get_pseudo_legal_moves(Coordinate(Ring.B, 12))
    assert all(m.end.slice == 11 for m in moves2)

@scenario(
    id="IC-PAWN-002",
    name="Valid En Passant (Towards Center)",
    description="A White pawn moving -1 towards Slice 9 captures a Black pawn that double-pushed +1 towards Slice 9.",
    pass_condition="En Passant is possible when both pawns are moving towards their meeting point."
)
def test_en_passant_valid_direction():
    b = Board()
    b.turn = Color.WHITE
    
    # White pawn at A9, moving -1 (towards 8)
    # Wait, if it's at A9 and moves -1, it goes to A8.
    b.add_piece(Coordinate(Ring.A, 9), Piece(Color.WHITE, PieceType.PAWN, direction=-1))
    
    # Black pawn at B7, moving +1 (towards 8, 9)
    # It double pushes 7 -> 8 -> 9. Skipped 8.
    b.add_piece(Coordinate(Ring.B, 9), Piece(Color.BLACK, PieceType.PAWN, direction=1))
    b.en_passant_target = Coordinate(Ring.B, 8)
    
    # Add a King to satisfy legality checks if any
    b.add_piece(Coordinate(Ring.D, 13), Piece(Color.WHITE, PieceType.KING))
    
    capture_board(b)
    
    moves = b.get_legal_moves(Coordinate(Ring.A, 9))
    assert any(m.end == Coordinate(Ring.B, 8) and m.is_en_passant for m in moves)

@scenario(
    id="IC-PAWN-003",
    name="Head-On Pawn Collision",
    description="Two pawns from different loops meeting head-on at the intersection must block each other.",
    pass_condition="Neither pawn can move forward into the occupied square."
)
def test_pawn_head_on_collision():
    b = Board()
    # White pawn moving +1 towards 18
    b.add_piece(Coordinate(Ring.B, 17), Piece(Color.WHITE, PieceType.PAWN, direction=1))
    # Black pawn moving -1 towards 18 (from 18-3 bracket)
    b.add_piece(Coordinate(Ring.B, 18), Piece(Color.BLACK, PieceType.PAWN, direction=-1))
    
    capture_board(b)
    
    w_moves = b.get_pseudo_legal_moves(Coordinate(Ring.B, 17))
    assert len(w_moves) == 0 # Blocked
    
    b.turn = Color.BLACK
    b_moves = b.get_pseudo_legal_moves(Coordinate(Ring.B, 18))
    assert len(b_moves) == 0 # Blocked

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
