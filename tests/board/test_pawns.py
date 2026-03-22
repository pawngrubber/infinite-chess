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
    name="White Forward Path Logic",
    description="White 'Forward' pawns start at Slice 17 and move UP (+1) towards Slice 4. They should never hit Slices 13-16 or 12.",
    pass_condition="White Forward pawn path is 17->18->1->2->3->4(Promote)."
)
def test_white_forward_path():
    b = Board()
    b.turn = Color.WHITE
    # Start at 17, move +1 (Up)
    b.add_piece(Coordinate(Ring.B, 17), Piece(Color.WHITE, PieceType.PAWN, direction=1))
    capture_board(b)
    
    # Simulate full path
    curr = Coordinate(Ring.B, 17)
    path = [curr]
    for _ in range(5):
        moves = b.get_pseudo_legal_moves(curr)
        next_move = next(m for m in moves if m.promotion is not None or m.end.slice == (curr.slice % 18) + 1)
        b.push(next_move)
        curr = next_move.end
        path.append(curr)
        if next_move.promotion: break
        
    slices = [c.slice for c in path]
    assert slices == [17, 18, 1, 2, 3, 4]
    # Forbidden check
    assert 13 not in slices
    assert 12 not in slices
    assert 14 not in slices

@scenario(
    id="IC-PAWN-002",
    name="Black Backward Path Logic (Mirror)",
    description="Black 'Backward' pawns start at Slice 3 and move DOWN (-1) towards Slice 13. They mirror the White Forward path but continue past the White base.",
    pass_condition="Black Backward pawn path is 3->2->1->18->17->16->15->14->13(Promote)."
)
def test_black_backward_path():
    b = Board()
    b.turn = Color.BLACK
    # Start at 3, move -1 (Down)
    b.add_piece(Coordinate(Ring.B, 3), Piece(Color.BLACK, PieceType.PAWN, direction=-1))
    capture_board(b)
    
    curr = Coordinate(Ring.B, 3)
    path = [curr]
    for _ in range(10):
        moves = b.get_pseudo_legal_moves(curr)
        # Find move that goes down in slice
        next_move = next(m for m in moves if m.promotion is not None or m.end.slice == (curr.slice - 2) % 18 + 1)
        b.push(next_move)
        curr = next_move.end
        path.append(curr)
        if next_move.promotion: break
        
    slices = [c.slice for c in path]
    assert slices == [3, 2, 1, 18, 17, 16, 15, 14, 13]
    # Forbidden check
    assert 4 not in slices

@scenario(
    id="IC-PAWN-003",
    name="White Pawn Forbidden Zone",
    description="White pawns are strictly forbidden from entering Slices 14, 15, and 16, as these are behind their movement vector.",
    pass_condition="No White pawn can generate a move that lands on Slice 14, 15, or 16."
)
def test_white_pawn_forbidden_zone():
    b = Board()
    # Test a 'Backward' White pawn starting at 12 moving -1
    b.add_piece(Coordinate(Ring.B, 12), Piece(Color.WHITE, PieceType.PAWN, direction=-1))
    capture_board(b)
    
    curr = Coordinate(Ring.B, 12)
    path_slices = []
    for _ in range(10):
        moves = b.get_pseudo_legal_moves(curr)
        if not moves: break
        next_move = next((m for m in moves), None)
        if not next_move: break
        b.push(next_move)
        curr = next_move.end
        path_slices.append(curr.slice)
        if next_move.promotion: break
        
    assert all(s not in [14, 15, 16] for s in path_slices)

@scenario(
    id="IC-PAWN-004",
    name="Black Pawn Forbidden Zone (Mirror)",
    description="Black pawns are strictly forbidden from entering Slices 1, 2, and 3.",
    pass_condition="No Black pawn can generate a move that lands on Slice 1, 2, or 3."
)
def test_black_pawn_forbidden_zone():
    b = Board()
    b.turn = Color.BLACK
    # Test a 'Forward' Black pawn starting at 5 moving +1
    b.add_piece(Coordinate(Ring.B, 5), Piece(Color.BLACK, PieceType.PAWN, direction=1))
    capture_board(b)
    
    curr = Coordinate(Ring.B, 5)
    path_slices = []
    for _ in range(10):
        moves = b.get_pseudo_legal_moves(curr)
        if not moves: break
        next_move = next((m for m in moves), None)
        if not next_move: break
        b.push(next_move)
        curr = next_move.end
        path_slices.append(curr.slice)
        if next_move.promotion: break
        
    assert all(s not in [1, 2, 3] for s in path_slices)

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
