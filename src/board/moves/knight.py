from typing import Iterator, TYPE_CHECKING
from ..logic import Coordinate, get_knight_moves

if TYPE_CHECKING:
    from ..board import Board, Piece, Move

def get_knight_piece_moves(board: 'Board', start: Coordinate, piece: 'Piece') -> Iterator['Move']:
    from ..board import Move
    for end_coord in get_knight_moves(start):
        target = board.squares.get(end_coord)
        if not target or target.color != piece.color:
            yield Move(start, end_coord, is_capture=bool(target))
