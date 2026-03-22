from enum import Enum
from typing import Dict, List, Set, Optional, Tuple, Iterator, Iterable
from .logic import Coordinate, Ring, get_knight_moves, get_king_moves, get_next_coord
from .moves.pawn import get_pawn_moves
from .moves.knight import get_knight_piece_moves
from .moves.bishop import get_bishop_moves
from .moves.rook import get_rook_moves
from .moves.queen import get_queen_moves
from .moves.king import get_king_piece_moves

class Color(Enum):
    WHITE = 1
    BLACK = 2

class PieceType(Enum):
    PAWN = 1
    KNIGHT = 2
    BISHOP = 3
    ROOK = 4
    QUEEN = 5
    KING = 6

class Piece:
    def __init__(self, color: Color, piece_type: PieceType, direction: int = 1):
        self.color = color
        self.piece_type = piece_type
        self.direction = direction # For pawns: +1 or -1 along the slice
        self.moves_made = 0

    def to_dict(self):
        return {
            "color": self.color.name,
            "type": self.piece_type.name,
            "direction": self.direction,
            "moves_made": self.moves_made
        }

    def __repr__(self):
        return f"{self.color.name[0]}{self.piece_type.name[0]}"

class Move:
    def __init__(self, start: Coordinate, end: Coordinate, is_capture: bool = False, is_en_passant: bool = False, promotion: Optional[PieceType] = None):
        self.start = start
        self.end = end
        self.is_capture = is_capture
        self.is_en_passant = is_en_passant
        self.promotion = promotion

    def to_dict(self):
        return {
            "start": self.start.to_dict(),
            "end": self.end.to_dict(),
            "is_capture": self.is_capture,
            "is_en_passant": self.is_en_passant,
            "promotion": self.promotion.name if self.promotion else None
        }

    def __repr__(self):
        return f"{self.start}->{self.end}"
    
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.start == other.start and self.end == other.end and self.promotion == other.promotion

    def __hash__(self):
        return hash((self.start, self.end, self.promotion))

class LegalMoveGenerator:
    def __init__(self, board: 'Board'):
        self.board = board

    def __bool__(self) -> bool:
        return any(self.board.generate_legal_moves())

    def count(self) -> int:
        return len(list(self))

    def __iter__(self) -> Iterator[Move]:
        return self.board.generate_legal_moves()

    def __contains__(self, move: Move) -> bool:
        return self.board.is_legal(move)

class PseudoLegalMoveGenerator:
    def __init__(self, board: 'Board'):
        self.board = board

    def __iter__(self) -> Iterator[Move]:
        return self.board.generate_pseudo_legal_moves()

class Board:
    def __init__(self):
        self.squares: Dict[Coordinate, Piece] = {}
        self.en_passant_target: Optional[Coordinate] = None
        self.turn = Color.WHITE
        self.move_stack: List[Move] = []
        self._state_stack: List[Tuple[Optional[Coordinate], Color, int]] = [] # (ep_target, turn, prev_moves_made)

    @property
    def legal_moves(self) -> LegalMoveGenerator:
        return LegalMoveGenerator(self)

    @property
    def pseudo_legal_moves(self) -> PseudoLegalMoveGenerator:
        return PseudoLegalMoveGenerator(self)

    def piece_at(self, coord: Coordinate) -> Optional[Piece]:
        return self.squares.get(coord)

    def to_dict(self):
        return {
            "squares": {str(sq): pc.to_dict() for sq, pc in self.squares.items()},
            "turn": self.turn.name,
            "en_passant_target": self.en_passant_target.to_dict() if self.en_passant_target else None
        }

    def reset(self):
        self.squares.clear()
        self.move_stack.clear()
        self._state_stack.clear()
        self.turn = Color.WHITE
        self.en_passant_target = None
        
        # WHITE PIECES (Bottom Loop, Center is Slice 13)
        self.add_piece(Coordinate(Ring.D, 13), Piece(Color.WHITE, PieceType.KING))
        self.add_piece(Coordinate(Ring.C, 13), Piece(Color.WHITE, PieceType.QUEEN))
        self.add_piece(Coordinate(Ring.B, 13), Piece(Color.WHITE, PieceType.BISHOP))
        self.add_piece(Coordinate(Ring.A, 13), Piece(Color.WHITE, PieceType.BISHOP))
        self.add_piece(Coordinate(Ring.D, 15), Piece(Color.WHITE, PieceType.ROOK))
        self.add_piece(Coordinate(Ring.C, 15), Piece(Color.WHITE, PieceType.KNIGHT))
        self.add_piece(Coordinate(Ring.D, 11), Piece(Color.WHITE, PieceType.ROOK))
        self.add_piece(Coordinate(Ring.C, 11), Piece(Color.WHITE, PieceType.KNIGHT))
        
        # Slices from 14-17 and 9-12 for 8 pawns
        for s in [14, 15, 16, 17]:
            self.add_piece(Coordinate(Ring.B, s), Piece(Color.WHITE, PieceType.PAWN, direction=1))
        for s in [12, 11, 10, 9]:
            self.add_piece(Coordinate(Ring.B, s), Piece(Color.WHITE, PieceType.PAWN, direction=-1))

        # BLACK PIECES (Top Loop, Center is Slice 4)
        self.add_piece(Coordinate(Ring.D, 4), Piece(Color.BLACK, PieceType.KING))
        self.add_piece(Coordinate(Ring.C, 4), Piece(Color.BLACK, PieceType.QUEEN))
        self.add_piece(Coordinate(Ring.B, 4), Piece(Color.BLACK, PieceType.BISHOP))
        self.add_piece(Coordinate(Ring.A, 4), Piece(Color.BLACK, PieceType.BISHOP))
        self.add_piece(Coordinate(Ring.D, 2), Piece(Color.BLACK, PieceType.ROOK))
        self.add_piece(Coordinate(Ring.C, 2), Piece(Color.BLACK, PieceType.KNIGHT))
        self.add_piece(Coordinate(Ring.D, 6), Piece(Color.BLACK, PieceType.ROOK))
        self.add_piece(Coordinate(Ring.C, 6), Piece(Color.BLACK, PieceType.KNIGHT))
        for s in [5, 6, 7, 8]:
            self.add_piece(Coordinate(Ring.B, s), Piece(Color.BLACK, PieceType.PAWN, direction=1))
        for s in [3, 2, 1, 18]:
            self.add_piece(Coordinate(Ring.B, s), Piece(Color.BLACK, PieceType.PAWN, direction=-1))

    def get_tile_color(self, coord: Coordinate) -> str:
        colors = ["RED", "GREEN", "YELLOW", "BLUE"]
        return colors[(coord.ring.value + coord.slice) % 4]

    def setup_board(self):
        """ Alias for reset() to maintain compatibility with existing tests/consumers """
        self.reset()

    def add_piece(self, coord: Coordinate, piece: Piece):
        self.squares[coord] = piece

    def remove_piece(self, coord: Coordinate) -> Optional[Piece]:
        return self.squares.pop(coord, None)

    def is_check(self) -> bool:
        return self.is_check_for_color(self.turn)

    def is_in_check(self, color: Color) -> bool:
        """ Compatibility alias for tests """
        return self.is_check_for_color(color)

    def is_checkmate(self, color: Optional[Color] = None) -> bool:
        c = color if color is not None else self.turn
        if not self.is_check_for_color(c):
            return False
        # Collect all legal moves for this color
        original_turn = self.turn
        self.turn = c
        has_legal = any(self.generate_legal_moves())
        self.turn = original_turn
        return not has_legal

    def is_stalemate(self, color: Optional[Color] = None) -> bool:
        c = color if color is not None else self.turn
        if self.is_check_for_color(c):
            return False
        original_turn = self.turn
        self.turn = c
        has_legal = any(self.generate_legal_moves())
        self.turn = original_turn
        return not has_legal

    def generate_pseudo_legal_moves(self) -> Iterator[Move]:
        # Collect coords first to avoid mutation issues
        coords = [c for c, p in self.squares.items() if p.color == self.turn]
        for coord in coords:
            yield from self._get_pseudo_legal_moves_for_piece(coord)

    def get_pseudo_legal_moves(self, coord: Coordinate) -> Set[Move]:
        """ Compatibility alias for tests """
        return set(self._get_pseudo_legal_moves_for_piece(coord))

    def generate_legal_moves(self) -> Iterator[Move]:
        pseudo = list(self.generate_pseudo_legal_moves())
        for move in pseudo:
            if self.is_legal(move):
                yield move

    def is_legal(self, move: Move) -> bool:
        piece = self.piece_at(move.start)
        if not piece or piece.color != self.turn:
            return False
        
        self.push(move)
        was_legal = not self.is_check_for_color(piece.color)
        self.pop()
        return was_legal

    def is_check_for_color(self, color: Color) -> bool:
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        return self.is_square_attacked(king_pos, enemy_color)

    def push(self, move: Move):
        piece = self.squares.get(move.start)
        if not piece:
            return

        captured_piece = self.squares.get(move.end)
        captured_coord = move.end
        
        if move.is_en_passant:
            try:
                cap_r, cap_s = get_next_coord(move.end, 0, -piece.direction)
                captured_coord = Coordinate(cap_r, cap_s)
                captured_piece = self.squares.get(captured_coord)
            except (ValueError, IndexError):
                pass

        undo_info = (move, captured_piece, captured_coord, self.en_passant_target, self.turn, piece.moves_made)
        self._state_stack.append(undo_info)

        # Execute move
        del self.squares[move.start]
        if captured_coord in self.squares:
            del self.squares[captured_coord]
            
        if move.promotion:
            piece.piece_type = move.promotion
            
        piece.moves_made += 1
        self.squares[move.end] = piece
        
        # En Passant target logic
        self.en_passant_target = None
        if piece.piece_type == PieceType.PAWN:
            try:
                r1, s1 = get_next_coord(move.start, 0, piece.direction)
                r2, s2 = get_next_coord(Coordinate(r1, s1), 0, piece.direction)
                if move.end == Coordinate(r2, s2):
                    self.en_passant_target = Coordinate(r1, s1)
            except (ValueError, IndexError):
                pass

        self.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        self.move_stack.append(move)

    def pop(self) -> Move:
        if not self._state_stack:
            raise IndexError("pop from empty stack")
        
        move, captured_piece, captured_coord, prev_ep_target, prev_turn, prev_moves_made = self._state_stack.pop()
        self.move_stack.pop()

        piece = self.squares.pop(move.end)
        if move.promotion:
            piece.piece_type = PieceType.PAWN
        piece.moves_made = prev_moves_made
        self.squares[move.start] = piece

        if captured_piece:
            self.squares[captured_coord] = captured_piece

        self.en_passant_target = prev_ep_target
        self.turn = prev_turn
        
        return move

    def find_king(self, color: Color) -> Optional[Coordinate]:
        for square, piece in self.squares.items():
            if piece.color == color and piece.piece_type == PieceType.KING:
                return square
        return None

    def is_square_attacked(self, coord: Coordinate, by_color: Color) -> bool:
        original_turn = self.turn
        self.turn = by_color
        is_attacked = any(move.end == coord for move in self.generate_pseudo_legal_moves())
        self.turn = original_turn
        return is_attacked

    def _get_pseudo_legal_moves_for_piece(self, coord: Coordinate) -> Iterator[Move]:
        piece = self.squares[coord]
        if piece.piece_type == PieceType.PAWN:
            return get_pawn_moves(self, coord, piece)
        elif piece.piece_type == PieceType.KNIGHT:
            return get_knight_piece_moves(self, coord, piece)
        elif piece.piece_type == PieceType.BISHOP:
            return get_bishop_moves(self, coord, piece)
        elif piece.piece_type == PieceType.ROOK:
            return get_rook_moves(self, coord, piece)
        elif piece.piece_type == PieceType.QUEEN:
            return get_queen_moves(self, coord, piece)
        elif piece.piece_type == PieceType.KING:
            return get_king_piece_moves(self, coord, piece)
        return iter([])

    def get_legal_moves(self, coord: Coordinate) -> Set[Move]:
        """ Compatibility method for pieces """
        return {m for m in self.generate_legal_moves() if m.start == coord}
