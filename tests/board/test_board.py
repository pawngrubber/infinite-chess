# /// script
# dependencies = [
#   "pytest",
# ]
# ///

import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from board.logic import Coordinate, Ring
from board.board import Board, Piece, PieceType, Color

def test_around_the_world_check():
    """
    Test that a sliding piece (Rook) can attack the King from 'behind'
    by wrapping around the empty loop.
    """
    b = Board()
    b.turn = Color.BLACK # Black's turn to see if king is in check
    # King on A1
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.BLACK, PieceType.KING))
    # Enemy Rook on A3
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.WHITE, PieceType.ROOK))
    
    # Is black king attacked? Yes, from A3 -> A2 -> A1 and also around the long way.
    # Actually wait, the Rook is attacking from 3 to 1 via 2, and also via 4, 5... 18, 1.
    assert b.is_in_check(Color.BLACK)

def test_self_intersection():
    """
    Test that a sliding piece does not count its own square as a move after a full lap.
    """
    b = Board()
    coord = Coordinate(Ring.A, 1)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.ROOK))
    
    moves = b.get_pseudo_legal_moves(coord)
    # The rook should not be able to capture itself or move to its own starting square
    for m in moves:
        assert m.end != coord

def test_pin_slide():
    """
    Test that a Rook pinned along a ring CAN move along that same ring,
    but CANNOT step off the ring.
    """
    b = Board()
    # White King at A1
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.KING))
    # White Rook at A3
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.WHITE, PieceType.ROOK))
    # Black Rook at A5 (Pinning the White Rook)
    b.add_piece(Coordinate(Ring.A, 5), Piece(Color.BLACK, PieceType.ROOK))
    
    # It's White's turn
    legal_moves = b.get_legal_moves(Coordinate(Ring.A, 3))
    
    # White Rook can move to A2, A4, or capture on A5.
    valid_ends = {Coordinate(Ring.A, 2), Coordinate(Ring.A, 4), Coordinate(Ring.A, 5)}
    for m in legal_moves:
        assert m.end in valid_ends
        
    # It should not be able to step to Ring B (e.g., B3) because that exposes the King
    for m in legal_moves:
        assert m.end.ring == Ring.A

def test_en_passant():
    """
    Test en passant capture logic.
    """
    b = Board()
    b.turn = Color.WHITE
    # White pawn on A4
    b.add_piece(Coordinate(Ring.A, 4), Piece(Color.WHITE, PieceType.PAWN, direction=1))
    # Black pawn on B4 (just double moved from B6, skipped B5)
    b.add_piece(Coordinate(Ring.B, 4), Piece(Color.BLACK, PieceType.PAWN, direction=-1))
    # The skipped square is the target
    b.en_passant_target = Coordinate(Ring.B, 5)
    
    # Add White King so we can test legality
    b.add_piece(Coordinate(Ring.D, 18), Piece(Color.WHITE, PieceType.KING))
    
    moves = b.get_legal_moves(Coordinate(Ring.A, 4))
    
    # Should have a move to B5
    found_ep = False
    for m in moves:
        if m.end == Coordinate(Ring.B, 5) and m.is_en_passant:
            found_ep = True
    assert found_ep

def test_king_teleportation_check():
    """
    Test King intersection jump check legality.
    """
    b = Board()
    b.turn = Color.WHITE
    # White King on A9
    b.add_piece(Coordinate(Ring.A, 9), Piece(Color.WHITE, PieceType.KING))
    # Black Rook on A18
    b.add_piece(Coordinate(Ring.A, 18), Piece(Color.BLACK, PieceType.ROOK))
    
    # The King on A9 has pseudo-legal move to A18.
    # However, A18 is occupied by the Black Rook.
    # The King can capture the Rook, IF the Rook is not protected.
    
    legal_moves = b.get_legal_moves(Coordinate(Ring.A, 9))
    found_capture = False
    for m in legal_moves:
        if m.end == Coordinate(Ring.A, 18):
            found_capture = True
    assert found_capture

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
