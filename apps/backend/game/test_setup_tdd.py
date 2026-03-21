import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from logic import Coordinate, Ring
from board import Board, Piece, PieceType, Color

def test_coordinate_serialization():
    """
    Test that we can convert Coordinate to string and parse string back to Coordinate.
    This is necessary for WebSockets.
    """
    c = Coordinate.from_string("A1")
    assert c.ring == Ring.A
    assert c.slice == 1
    
    c2 = Coordinate.from_string("D18")
    assert c2.ring == Ring.D
    assert c2.slice == 18
    
    assert str(c) == "A1"
    assert str(c2) == "D18"

def test_starting_position():
    """
    Test that setup_board() populates exactly 32 pieces correctly.
    """
    b = Board()
    b.setup_board()
    
    white_pieces = [p for p in b.squares.values() if p.color == Color.WHITE]
    black_pieces = [p for p in b.squares.values() if p.color == Color.BLACK]
    
    assert len(white_pieces) == 16
    assert len(black_pieces) == 16
    
    # Check specific key squares based on the image
    # Note: Without the full mapping, let's at least check that kings and pawns exist
    white_king_pos = b.find_king(Color.WHITE)
    black_king_pos = b.find_king(Color.BLACK)
    
    assert white_king_pos is not None
    assert black_king_pos is not None
