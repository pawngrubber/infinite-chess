from typing import Iterator, TYPE_CHECKING
from .common import get_slide_moves
from ..logic import Coordinate

if TYPE_CHECKING:
    from ..board import Board, Piece, Move

def get_rook_moves(board: 'Board', start: Coordinate, piece: 'Piece') -> Iterator['Move']:
    return get_slide_moves(board, start, piece, [(0, 1), (0, -1), (1, 0), (-1, 0)])
