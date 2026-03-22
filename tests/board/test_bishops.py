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
    name="Bishop Intersection Path",
    description="Bishops must be able to traverse the physical intersection between the two loops. Specifically, a Bishop at B17 should be able to reach C6 by following the diagonal topology.",
    pass_condition="Coordinate C6 is in the set of pseudo-legal moves for a Bishop at B17."
)
def test_bishop_b17_to_c6():
    b = Board()
    start = Coordinate(Ring.B, 17)
    target = Coordinate(Ring.C, 6)
    b.add_piece(start, Piece(Color.WHITE, PieceType.BISHOP))
    capture_board(b)
    
    moves = b.get_pseudo_legal_moves(start)
    ends = [m.end for m in moves]
    assert target in ends

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
