from typing import List, Tuple, Iterator, TYPE_CHECKING
from ..logic import Coordinate, Ring, get_next_coord

if TYPE_CHECKING:
    from ..board import Board, Piece, Move

def get_slide_moves(board: 'Board', start: Coordinate, piece: 'Piece', directions: List[Tuple[int, int]]) -> Iterator['Move']:
    from ..board import Move
    for dr, ds in directions:
        curr = start
        visited = {start}
        while True:
            try:
                nr, ns = get_next_coord(curr, dr, ds)
            except (ValueError, IndexError):
                break
            
            if nr < Ring.A.value or nr > Ring.D.value:
                break
            
            next_coord = Coordinate(nr, ns)
            if next_coord in visited:
                break
            visited.add(next_coord)
            
            target = board.squares.get(next_coord)
            if target:
                if target.color != piece.color:
                    yield Move(start, next_coord, is_capture=True)
                break
            yield Move(start, next_coord)
            curr = next_coord
