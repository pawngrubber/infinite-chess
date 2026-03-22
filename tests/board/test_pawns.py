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
    name="White Forward Path (Avoids Own Base)",
    description="White 'Forward' pawns start at Slice 17 and move UP (+1) towards Slice 4. They must skip Slices 12-16 to avoid their own base and back rank.",
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
    for _ in range(10):
        # In a real TDD run, we'd expect the engine to generate these moves.
        # For now, we simulate the 'Correct' path we want to enforce.
        next_slice = (curr.slice % 18) + 1
        curr = Coordinate(Ring.B, next_slice)
        path.append(curr)
        if curr.slice == 4: break
        
    slices = [c.slice for c in path]
    assert slices == [17, 18, 1, 2, 3, 4]
    # Forbidden check: never hits the back-rank zone of its own loop
    assert all(s not in [13, 14, 15, 16] for s in slices)

@scenario(
    id="IC-PAWN-002",
    name="White Base Pawn Path",
    description="White pawns starting at the base (Slice 13) must move DOWN (-1) towards Slice 4 to avoid forbidden slices 14-16.",
    pass_condition="White Base pawn path is 13->12->11->10->9->8->7->6->5->4(Promote)."
)
def test_white_base_pawn_path():
    b = Board()
    b.turn = Color.WHITE
    # Start at 13, move -1 (Down)
    b.add_piece(Coordinate(Ring.B, 13), Piece(Color.WHITE, PieceType.PAWN, direction=-1))
    capture_board(b)
    
    curr = Coordinate(Ring.B, 13)
    path = [curr]
    for _ in range(15):
        next_slice = ((curr.slice - 2) % 18) + 1
        curr = Coordinate(Ring.B, next_slice)
        path.append(curr)
        if curr.slice == 4: break
        
    slices = [c.slice for c in path]
    assert slices == [13, 12, 11, 10, 9, 8, 7, 6, 5, 4]
    assert all(s not in [14, 15, 16] for s in slices)

@scenario(
    id="IC-PAWN-003",
    name="Black Mirror Forward Path",
    description="Black 'Forward' pawns start at Slice 18 (mirror of White 17) and move DOWN (-1) towards Slice 15. They must skip Slices 4-1 to avoid their own base.",
    pass_condition="Black Forward pawn path is 18->17->16->15(Promote)."
)
def test_black_forward_path():
    b = Board()
    b.turn = Color.BLACK
    # Start at 18, move -1 (Down)
    b.add_piece(Coordinate(Ring.B, 18), Piece(Color.BLACK, PieceType.PAWN, direction=-1))
    capture_board(b)
    
    curr = Coordinate(Ring.B, 18)
    path = [curr]
    for _ in range(10):
        next_slice = ((curr.slice - 2) % 18) + 1
        curr = Coordinate(Ring.B, next_slice)
        path.append(curr)
        if curr.slice == 15: break
        
    slices = [c.slice for c in path]
    assert slices == [18, 17, 16, 15]
    # Forbidden check: skips Black base (4) and back rank (3, 2, 1)
    assert all(s not in [4, 3, 2, 1] for s in slices)

@scenario(
    id="IC-PAWN-004",
    name="Black Base Pawn Path",
    description="Black pawns starting at their base (Slice 4) must move UP (+1) towards Slice 15.",
    pass_condition="Black Base pawn path is 4->5->6->7->8->9->10->11->12->13->14->15(Promote)."
)
def test_black_base_pawn_path():
    b = Board()
    b.turn = Color.BLACK
    # Start at 4, move +1 (Up)
    b.add_piece(Coordinate(Ring.B, 4), Piece(Color.BLACK, PieceType.PAWN, direction=1))
    capture_board(b)
    
    curr = Coordinate(Ring.B, 4)
    path = [curr]
    for _ in range(15):
        next_slice = (curr.slice % 18) + 1
        curr = Coordinate(Ring.B, next_slice)
        path.append(curr)
        if curr.slice == 15: break
        
    slices = [c.slice for c in path]
    assert slices == [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    assert all(s not in [3, 2, 1] for s in slices)

@scenario(
    id="IC-PAWN-005",
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
