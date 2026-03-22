import sys
import os
import pytest

from board.logic import Coordinate, Ring
from board.board import Board, Piece, PieceType, Color
from board.testing import scenario, capture_board

@scenario(
    
    name="Bishop Color Constraint",
    description="Bishops must strictly alternate between two specific colors of the 4-color tiling.",
    pass_condition="All moves for a Bishop land on its allowed color complex."
)
def test_bishop_color_constraint():
    b = Board()
    coord = Coordinate(Ring.C, 5)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.BISHOP))
    capture_board(b)
    moves = b.get_pseudo_legal_moves(coord)
    assert len(moves) > 0
    for m in moves:
        assert b.get_tile_color(m.end) in ["GREEN", "BLUE"]

@scenario(
    
    name="Pawn Promotion (10 Steps)",
    description="Pawns must travel exactly 10 spaces on the figure-eight track to promote.",
    pass_condition="Promotion is only available when moves_made is 9 or more."
)
def test_pawn_10_space_promotion():
    b = Board()
    b.turn = Color.WHITE
    start_coord = Coordinate(Ring.A, 1)
    pawn = Piece(Color.WHITE, PieceType.PAWN, direction=1)
    pawn.moves_made = 9
    b.add_piece(start_coord, pawn)
    capture_board(b)
    
    moves = b.get_legal_moves(start_coord)
    assert any(m.promotion == PieceType.QUEEN for m in moves)

@scenario(
    
    name="Knight Wormhole Jump",
    description="Knights can jump across the physical intersection between Slice 9 and 18.",
    pass_condition="Knight at A9 has a legal jump to C18 across the intersection."
)
def test_knight_true_lemniscate_jump():
    b = Board()
    coord = Coordinate(Ring.A, 9)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.KNIGHT))
    capture_board(b)
    moves = b.get_pseudo_legal_moves(coord)
    ends = [m.end for m in moves]
    assert Coordinate(Ring.C, 18) in ends

@scenario(
    
    name="Checkmate Recognition",
    description="The engine must correctly identify when the King is trapped in check.",
    pass_condition="is_checkmate returns True when no legal escape exists."
)
def test_is_checkmate():
    b = Board()
    b.turn = Color.BLACK
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.BLACK, PieceType.KING))
    b.add_piece(Coordinate(Ring.B, 1), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 2), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 18), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.C, 1), Piece(Color.WHITE, PieceType.ROOK))
    capture_board(b)
    
    assert b.is_checkmate(Color.BLACK)

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
