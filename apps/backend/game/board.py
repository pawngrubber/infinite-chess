from enum import Enum
from typing import Dict, List, Set, Optional, Tuple
from logic import Coordinate, Ring, get_knight_moves, get_king_moves

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

    def __repr__(self):
        return f"{self.color.name[0]}{self.piece_type.name[0]}"

class Move:
    def __init__(self, start: Coordinate, end: Coordinate, is_capture: bool = False, is_en_passant: bool = False, promotion: Optional[PieceType] = None):
        self.start = start
        self.end = end
        self.is_capture = is_capture
        self.is_en_passant = is_en_passant
        self.promotion = promotion

    def __repr__(self):
        return f"{self.start}->{self.end}"
    
    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        return self.start == other.start and self.end == other.end and self.promotion == other.promotion

    def __hash__(self):
        return hash((self.start, self.end, self.promotion))

class Board:
    def __init__(self):
        self.squares: Dict[Coordinate, Piece] = {}
        self.en_passant_target: Optional[Coordinate] = None
        self.turn = Color.WHITE

    def get_tile_color(self, coord: Coordinate) -> str:
        colors = ["RED", "GREEN", "YELLOW", "BLUE"]
        return colors[(coord.ring.value + coord.slice) % 4]

    def add_piece(self, coord: Coordinate, piece: Piece):
        self.squares[coord] = piece

    def remove_piece(self, coord: Coordinate):
        if coord in self.squares:
            del self.squares[coord]

    def get_piece(self, coord: Coordinate) -> Optional[Piece]:
        return self.squares.get(coord)

    def is_empty(self, coord: Coordinate) -> bool:
        return coord not in self.squares

    def _slide_moves(self, start: Coordinate, piece: Piece, directions: List[Tuple[int, int]]) -> Set[Move]:
        moves = set()
        for dr, ds in directions:
            r = start.ring.value
            s = start.slice
            visited = set()
            while True:
                r += dr
                s += ds
                
                if r < Ring.A.value or r > Ring.D.value:
                    break
                
                curr = Coordinate(Ring(r), s)
                if curr in visited:
                    break 
                visited.add(curr)

                target_piece = self.get_piece(curr)
                if target_piece:
                    if target_piece.color != piece.color:
                        moves.add(Move(start, curr, is_capture=True))
                    break 
                else:
                    moves.add(Move(start, curr))
        return moves

    def get_pseudo_legal_moves(self, coord: Coordinate) -> Set[Move]:
        piece = self.get_piece(coord)
        if not piece:
            return set()

        moves = set()

        if piece.piece_type == PieceType.ROOK:
            moves |= self._slide_moves(coord, piece, [(0, 1), (0, -1), (1, 0), (-1, 0)])

        elif piece.piece_type == PieceType.BISHOP:
            moves |= self._slide_moves(coord, piece, [(1, 1), (1, -1), (-1, 1), (-1, -1)])

        elif piece.piece_type == PieceType.QUEEN:
            moves |= self._slide_moves(coord, piece, [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)])

        elif piece.piece_type == PieceType.KNIGHT:
            for end_coord in get_knight_moves(coord):
                target_piece = self.get_piece(end_coord)
                if not target_piece or target_piece.color != piece.color:
                    moves.add(Move(coord, end_coord, is_capture=bool(target_piece)))

        elif piece.piece_type == PieceType.KING:
            for end_coord in get_king_moves(coord):
                target_piece = self.get_piece(end_coord)
                if not target_piece or target_piece.color != piece.color:
                    moves.add(Move(coord, end_coord, is_capture=bool(target_piece)))

        elif piece.piece_type == PieceType.PAWN:
            forward_coord = Coordinate(coord.ring, coord.slice + piece.direction)
            if self.is_empty(forward_coord):
                if piece.moves_made >= 9: # 10th move promotion
                    moves.add(Move(coord, forward_coord, promotion=PieceType.QUEEN))
                else:
                    moves.add(Move(coord, forward_coord))
                
                # Double push
                if piece.moves_made == 0:
                    double_forward = Coordinate(coord.ring, coord.slice + piece.direction * 2)
                    if self.is_empty(double_forward):
                        moves.add(Move(coord, double_forward))

            # Captures
            for dr in [-1, 1]:
                if Ring.A.value <= coord.ring.value + dr <= Ring.D.value:
                    cap_coord = Coordinate(Ring(coord.ring.value + dr), coord.slice + piece.direction)
                    target = self.get_piece(cap_coord)
                    is_promotion = piece.moves_made >= 9
                    
                    if target and target.color != piece.color:
                        moves.add(Move(coord, cap_coord, is_capture=True, promotion=PieceType.QUEEN if is_promotion else None))
                    elif cap_coord == self.en_passant_target:
                        moves.add(Move(coord, cap_coord, is_capture=True, is_en_passant=True))

        return moves

    def is_square_attacked(self, coord: Coordinate, by_color: Color) -> bool:
        for square, piece in self.squares.items():
            if piece.color == by_color:
                for move in self.get_pseudo_legal_moves(square):
                    if move.end == coord:
                        return True
        return False

    def find_king(self, color: Color) -> Optional[Coordinate]:
        for square, piece in self.squares.items():
            if piece.color == color and piece.piece_type == PieceType.KING:
                return square
        return None

    def is_in_check(self, color: Color) -> bool:
        king_pos = self.find_king(color)
        if not king_pos:
            return False
        enemy_color = Color.BLACK if color == Color.WHITE else Color.WHITE
        return self.is_square_attacked(king_pos, enemy_color)

    def get_legal_moves(self, coord: Coordinate) -> Set[Move]:
        piece = self.get_piece(coord)
        if not piece or piece.color != self.turn:
            return set()
            
        pseudo_moves = self.get_pseudo_legal_moves(coord)
        legal_moves = set()
        
        for move in pseudo_moves:
            next_board = self.make_move(move)
            if not next_board.is_in_check(piece.color):
                legal_moves.add(move)
                
        return legal_moves

    def get_all_legal_moves(self, color: Color) -> Set[Move]:
        moves = set()
        for sq, piece in self.squares.items():
            if piece.color == color:
                moves |= self.get_legal_moves(sq)
        return moves

    def is_checkmate(self, color: Color) -> bool:
        return self.is_in_check(color) and len(self.get_all_legal_moves(color)) == 0

    def is_stalemate(self, color: Color) -> bool:
        return not self.is_in_check(color) and len(self.get_all_legal_moves(color)) == 0

    def make_move(self, move: Move) -> 'Board':
        new_board = Board()
        for sq, pc in self.squares.items():
            new_pc = Piece(pc.color, pc.piece_type, pc.direction)
            new_pc.moves_made = pc.moves_made
            new_board.add_piece(sq, new_pc)
        
        piece = new_board.get_piece(move.start)
        new_board.remove_piece(move.start)
        
        if move.is_en_passant:
            cap_coord = Coordinate(move.end.ring, move.end.slice - piece.direction)
            new_board.remove_piece(cap_coord)
            
        if move.promotion:
            piece.piece_type = move.promotion
            
        piece.moves_made += 1
        new_board.add_piece(move.end, piece)
        new_board.turn = Color.BLACK if self.turn == Color.WHITE else Color.WHITE
        return new_board
