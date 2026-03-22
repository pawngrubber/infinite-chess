import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from infinite_chess.logic import Coordinate, Ring
from infinite_chess.board import Board, Piece, PieceType, Color, Move

# -------------------------------------------------------------------
# 1. CORE PIECE MOVEMENT (No Board Blockers)
# -------------------------------------------------------------------

def test_rook_empty_board():
    b = Board()
    coord = Coordinate(Ring.C, 5)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.ROOK))
    moves = b.get_pseudo_legal_moves(coord)
    # A rook on an empty ring should be able to move to 17 other slices on the same ring
    # and 3 other rings on the same slice. Total 20 moves.
    assert len(moves) == 20
    # Make sure we don't return the starting square
    for m in moves:
        assert m.end != coord

def test_bishop_empty_board():
    b = Board()
    coord = Coordinate(Ring.C, 5)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.BISHOP))
    moves = b.get_pseudo_legal_moves(coord)
    # Bishop moves along diagonals
    assert Move(coord, Coordinate(Ring.D, 6)) in moves
    assert Move(coord, Coordinate(Ring.B, 4)) in moves

def test_queen_empty_board():
    b = Board()
    coord = Coordinate(Ring.B, 10)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.QUEEN))
    moves = b.get_pseudo_legal_moves(coord)
    # Queen should have Rook + Bishop moves combined
    assert Move(coord, Coordinate(Ring.B, 11)) in moves # Rook move
    assert Move(coord, Coordinate(Ring.C, 11)) in moves # Bishop move

def test_knight_empty_board():
    b = Board()
    coord = Coordinate(Ring.A, 1)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.KNIGHT))
    moves = b.get_pseudo_legal_moves(coord)
    # Knight on A1 can jump to B3, C2. It cannot jump to Ring < A.
    valid_ends = [m.end for m in moves]
    assert Coordinate(Ring.B, 3) in valid_ends
    assert Coordinate(Ring.C, 2) in valid_ends

def test_king_empty_board():
    b = Board()
    coord = Coordinate(Ring.D, 9)
    b.add_piece(coord, Piece(Color.WHITE, PieceType.KING))
    moves = b.get_pseudo_legal_moves(coord)
    valid_ends = [m.end for m in moves]
    # Standard adjacencies
    assert Coordinate(Ring.C, 9) in valid_ends
    assert Coordinate(Ring.D, 10) in valid_ends
    assert Coordinate(Ring.C, 8) in valid_ends
    # Intersection adjacency (slice 9 crosses to 18)
    assert Coordinate(Ring.D, 18) in valid_ends

# -------------------------------------------------------------------
# 2. BLOCKING & CAPTURING (Collision Detection)
# -------------------------------------------------------------------

def test_rook_blocked_by_friendly():
    b = Board()
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.WHITE, PieceType.PAWN))
    b.add_piece(Coordinate(Ring.A, 18), Piece(Color.WHITE, PieceType.PAWN)) # Block backwards path too
    moves = b.get_pseudo_legal_moves(Coordinate(Ring.A, 1))
    ends = [m.end for m in moves]
    assert Coordinate(Ring.A, 2) in ends
    assert Coordinate(Ring.A, 3) not in ends # Blocked by friendly
    assert Coordinate(Ring.A, 4) not in ends # Blocked by friendly AND backwards path is blocked

def test_rook_capture_enemy():
    b = Board()
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.BLACK, PieceType.PAWN))
    b.add_piece(Coordinate(Ring.A, 18), Piece(Color.WHITE, PieceType.PAWN)) # Block backwards path
    moves = b.get_pseudo_legal_moves(Coordinate(Ring.A, 1))
    capture_move = next((m for m in moves if m.end == Coordinate(Ring.A, 3)), None)
    assert capture_move is not None
    assert capture_move.is_capture
    # Cannot go through the enemy
    assert Coordinate(Ring.A, 4) not in [m.end for m in moves]

def test_bishop_capture_enemy():
    b = Board()
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.BISHOP))
    b.add_piece(Coordinate(Ring.B, 2), Piece(Color.BLACK, PieceType.KNIGHT))
    moves = b.get_pseudo_legal_moves(Coordinate(Ring.A, 1))
    capture_move = next((m for m in moves if m.end == Coordinate(Ring.B, 2)), None)
    assert capture_move is not None
    assert capture_move.is_capture
    assert Coordinate(Ring.C, 3) not in [m.end for m in moves]

# -------------------------------------------------------------------
# 3. INTERSECTION MADNESS (Slices 8-11)
# -------------------------------------------------------------------

def test_pawn_head_on_collision():
    b = Board()
    b.add_piece(Coordinate(Ring.A, 8), Piece(Color.WHITE, PieceType.PAWN, direction=1))
    b.add_piece(Coordinate(Ring.A, 9), Piece(Color.BLACK, PieceType.PAWN, direction=-1))
    
    w_moves = b.get_pseudo_legal_moves(Coordinate(Ring.A, 8))
    # White pawn is blocked by black pawn at 9
    assert Coordinate(Ring.A, 9) not in [m.end for m in w_moves]

def test_king_teleportation_crossing():
    b = Board()
    # King at the crossing
    b.add_piece(Coordinate(Ring.B, 18), Piece(Color.WHITE, PieceType.KING))
    # Enemy at the other side of crossing
    b.add_piece(Coordinate(Ring.B, 9), Piece(Color.BLACK, PieceType.PAWN))
    
    moves = b.get_pseudo_legal_moves(Coordinate(Ring.B, 18))
    capture_move = next((m for m in moves if m.end == Coordinate(Ring.B, 9)), None)
    assert capture_move is not None
    assert capture_move.is_capture

# -------------------------------------------------------------------
# 4. INFINITE LOOP TOPOLOGY
# -------------------------------------------------------------------

def test_loop_wrap_around_rook():
    b = Board()
    b.add_piece(Coordinate(Ring.A, 18), Piece(Color.WHITE, PieceType.ROOK))
    moves = b.get_pseudo_legal_moves(Coordinate(Ring.A, 18))
    # Wrapping forward 18 -> 1
    assert Coordinate(Ring.A, 1) in [m.end for m in moves]
    # Wrapping backward 18 -> 17
    assert Coordinate(Ring.A, 17) in [m.end for m in moves]

def test_loop_wrap_around_bishop():
    b = Board()
    b.add_piece(Coordinate(Ring.C, 18), Piece(Color.WHITE, PieceType.BISHOP))
    moves = b.get_pseudo_legal_moves(Coordinate(Ring.C, 18))
    # C18 + (1,1) -> D1
    assert Coordinate(Ring.D, 1) in [m.end for m in moves]
    # C18 + (-1, 1) -> B1
    assert Coordinate(Ring.B, 1) in [m.end for m in moves]

# -------------------------------------------------------------------
# 5. PINS AND GHOST THREATS
# -------------------------------------------------------------------

def test_absolute_pin_horizontal():
    b = Board()
    b.turn = Color.WHITE
    b.add_piece(Coordinate(Ring.B, 5), Piece(Color.WHITE, PieceType.KING))
    b.add_piece(Coordinate(Ring.B, 6), Piece(Color.WHITE, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.B, 10), Piece(Color.BLACK, PieceType.ROOK)) # Pinning along the ring
    # Block the backwards 'around the world' check path so the King is not currently in check
    b.add_piece(Coordinate(Ring.B, 4), Piece(Color.WHITE, PieceType.PAWN))

    moves = b.get_legal_moves(Coordinate(Ring.B, 6))
    ends = [m.end for m in moves]
    # The rook can slide along the ring to B7, B8, B9, or capture B10
    assert Coordinate(Ring.B, 7) in ends
    assert Coordinate(Ring.B, 10) in ends
    # The rook cannot slide to ring C
    assert Coordinate(Ring.C, 6) not in ends

def test_absolute_pin_diagonal():
    b = Board()
    b.turn = Color.WHITE
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.KING))
    b.add_piece(Coordinate(Ring.B, 2), Piece(Color.WHITE, PieceType.BISHOP))
    b.add_piece(Coordinate(Ring.D, 4), Piece(Color.BLACK, PieceType.BISHOP)) # Pinning diagonally

    moves = b.get_legal_moves(Coordinate(Ring.B, 2))
    ends = [m.end for m in moves]
    # Bishop can move along the pin to C3 or D4
    assert Coordinate(Ring.C, 3) in ends
    assert Coordinate(Ring.D, 4) in ends
    # Bishop cannot move off the pin to A3
    assert Coordinate(Ring.A, 3) not in ends

def test_pinned_piece_projects_check():
    b = Board()
    b.turn = Color.BLACK
    # Black King
    b.add_piece(Coordinate(Ring.C, 3), Piece(Color.BLACK, PieceType.KING))
    # White Queen (pinned diagonally to white king)
    b.add_piece(Coordinate(Ring.C, 6), Piece(Color.WHITE, PieceType.QUEEN))
    b.add_piece(Coordinate(Ring.B, 5), Piece(Color.WHITE, PieceType.KING))
    # Black Bishop pinning the white queen diagonally
    b.add_piece(Coordinate(Ring.D, 7), Piece(Color.BLACK, PieceType.BISHOP))

    # The White Queen is legally pinned to the White King, but it STILL attacks C3 where the Black King is.
    # We expect is_in_check(BLACK) to be True!
    assert b.is_in_check(Color.BLACK)

# -------------------------------------------------------------------
# 6. CHECK EVASION PRECEDENCE
# -------------------------------------------------------------------

def test_double_check_forces_king_move():
    b = Board()
    b.turn = Color.WHITE
    # White King
    b.add_piece(Coordinate(Ring.A, 1), Piece(Color.WHITE, PieceType.KING))
    # White Rook
    b.add_piece(Coordinate(Ring.C, 1), Piece(Color.WHITE, PieceType.ROOK))
    
    # Black pieces giving double check
    b.add_piece(Coordinate(Ring.A, 3), Piece(Color.BLACK, PieceType.ROOK))
    b.add_piece(Coordinate(Ring.B, 2), Piece(Color.BLACK, PieceType.BISHOP))
    
    assert b.is_in_check(Color.WHITE)
    
    # White Rook should have NO legal moves because it's a double check
    rook_moves = b.get_legal_moves(Coordinate(Ring.C, 1))
    assert len(rook_moves) == 0
    
    # White King must move
    king_moves = b.get_legal_moves(Coordinate(Ring.A, 1))
    assert len(king_moves) > 0

# -------------------------------------------------------------------
# 7. AROUND THE WORLD (Edge Case)
# -------------------------------------------------------------------

def test_around_the_world_check_advanced():
    b = Board()
    b.turn = Color.WHITE
    # White King
    b.add_piece(Coordinate(Ring.A, 5), Piece(Color.WHITE, PieceType.KING))
    # Black Rook on the other side of the loop
    b.add_piece(Coordinate(Ring.A, 4), Piece(Color.BLACK, PieceType.ROOK))
    # Black Rook attacks A5 directly (distance 1) AND around the loop (distance 17)
    
    assert b.is_in_check(Color.WHITE)
    
    # If White blocks the short path
    b.add_piece(Coordinate(Ring.A, 6), Piece(Color.WHITE, PieceType.KNIGHT))
    # But wait, White Knight blocks the LONG path. The SHORT path is A4->A5. 
    # Let's say Rook is at A3. King is at A5.
    
    b2 = Board()
    b2.turn = Color.WHITE
    b2.add_piece(Coordinate(Ring.A, 5), Piece(Color.WHITE, PieceType.KING))
    b2.add_piece(Coordinate(Ring.A, 3), Piece(Color.BLACK, PieceType.ROOK))
    
    # Block the short path A3 -> A4 -> A5
    b2.add_piece(Coordinate(Ring.A, 4), Piece(Color.WHITE, PieceType.PAWN))
    
    # Is it STILL in check? Yes, because A3 -> A2 -> A1 -> A18 ... -> A5
    assert b2.is_in_check(Color.WHITE)

if __name__ == "__main__":
    sys.exit(pytest.main(["-v", __file__]))
