from typing import Iterator, TYPE_CHECKING
from ..logic import Coordinate, Ring, get_next_coord

if TYPE_CHECKING:
    from ..board import Board, Piece, Move

def get_pawn_moves(board: 'Board', start: Coordinate, piece: 'Piece') -> Iterator['Move']:
    from ..board import Move, PieceType
    
    # Forward
    try:
        nr, ns = get_next_coord(start, 0, piece.direction)
        forward = Coordinate(nr, ns)
        if forward not in board.squares:
            yield Move(start, forward, promotion=PieceType.QUEEN if piece.moves_made >= 9 else None)
            if piece.moves_made == 0:
                try:
                    nr2, ns2 = get_next_coord(forward, 0, piece.direction)
                    double = Coordinate(nr2, ns2)
                    if double not in board.squares:
                        yield Move(start, double)
                except (ValueError, IndexError):
                    pass
    except (ValueError, IndexError):
        pass
        
    # Captures
    for dr in [-1, 1]:
        if Ring.A.value <= start.ring.value + dr <= Ring.D.value:
            try:
                nr, ns = get_next_coord(start, dr, piece.direction)
                cap_coord = Coordinate(nr, ns)
                target = board.squares.get(cap_coord)
                if target and target.color != piece.color:
                    yield Move(start, cap_coord, is_capture=True, promotion=PieceType.QUEEN if piece.moves_made >= 9 else None)
                elif cap_coord == board.en_passant_target:
                    yield Move(start, cap_coord, is_capture=True, is_en_passant=True)
            except (ValueError, IndexError):
                pass
