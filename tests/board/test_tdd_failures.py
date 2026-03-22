import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from board.logic import Coordinate, Ring
from board.board import Board, Piece, PieceType, Color

def test_bishop_color_constraint():
    """
    In Infinite Chess, the board is tiled with Red, Yellow, Blue, and Green.
    A Bishop must strictly alternate between Green and Blue (or Red and Yellow)
    and can never step on the wrong color complex.
    """
    b = Board()
    coord = Coordinate(Ring.C, 5)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.BISHOP))
    moves = b.get_pseudo_legal_moves(coord)
    assert len(moves) > 0
    
    # This will fail because get_tile_color() doesn't exist yet
    for m in moves:
        assert b.get_tile_color(m.end) in ["GREEN", "BLUE"]

def test_pawn_10_space_promotion():
    """
    A pawn must travel 10 spaces on the elongated lemniscate loops to promote.
    """
    b = Board()
    b.turn = Color.WHITE
    start_coord = Coordinate(Ring.A, 1)
    b.add_piece(start_coord, Piece(Color.WHITE, PieceType.PAWN, direction=1))
    
    # Fast-forward the pawn's life: pretend it has moved 9 times
    # This attribute doesn't exist yet!
    b.squares[start_coord].moves_made = 9 
    
    moves = b.get_legal_moves(start_coord)
    promotion_moves = [m for m in moves if m.promotion is not None]
    
    # Should generate promotion moves (to Queen, Rook, etc.)
    assert len(promotion_moves) > 0
    assert promotion_moves[0].promotion == PieceType.QUEEN

def test_pawn_double_push():
    """
    A pawn that hasn't moved yet can move forward two spaces.
    """
    b = Board()
    b.turn = Color.WHITE
    start_coord = Coordinate(Ring.A, 1)
    b.add_piece(start_coord, Piece(Color.WHITE, PieceType.PAWN, direction=1))
    
    # It has 0 moves made, so it can double push to A3
    moves = b.get_legal_moves(start_coord)
    assert any(m.end == Coordinate(Ring.A, 3) for m in moves)

def test_is_checkmate():
    """
    The board must recognize Checkmate when the King is in check and has no legal moves.
    """
    b = Board()
    b.turn = Color.BLACK
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.BLACK, PieceType.KING))
    
    # Surround with White Rooks to create an inescapable check
    b.add_piece(Coordinate(Ring.B, 1), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 2), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 18), Piece(Color.WHITE, PieceType.ROOK))
    
    # Protect the B1 Rook so the King cannot capture it
    b.add_piece(Coordinate(Ring.C, 1), Piece(Color.WHITE, PieceType.ROOK))
    
    assert b.is_in_check(Color.BLACK)
    # This method doesn't exist yet! (Wait, I implemented it, so it should be true now)
    assert b.is_checkmate(Color.BLACK)

def test_is_stalemate():
    """
    The board must recognize Stalemate when the King is NOT in check but has no legal moves.
    """
    b = Board()
    b.turn = Color.BLACK
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.BLACK, PieceType.KING))
    
    # Control all surrounding squares without checking the King
    b.add_piece(Coordinate(Ring.C, 2), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.C, 18), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.B, 3), Piece(Color.WHITE, PieceType.ROOK))
    
    assert not b.is_in_check(Color.BLACK)
    # This method doesn't exist yet!
    assert b.is_stalemate(Color.BLACK)

def test_knight_true_lemniscate_jump():
    """
    Because Slice 9 crosses Slice 18 physically, a Knight's L-shape should be able
    to bridge the gap between these opposing tracks at the intersection.
    """
    b = Board()
    coord = Coordinate(Ring.A, 9)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.KNIGHT))
    moves = b.get_pseudo_legal_moves(coord)
    
    # C18 is physically an L-shape away from A9 across the intersection void
    # Currently, our math just adds/subtracts 2, so it won't find this wormhole jump.
    ends = [m.end for m in moves]
    assert Coordinate(Ring.C, 18) in ends
