# /// script
# dependencies = [
#   "svgwrite",
# ]
# ///

import sys
import os
import math
from typing import List, Tuple, Dict
import svgwrite

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from board.board import Board, Color, PieceType, Move
from board.logic import Coordinate, Ring

def to_ifen(board: Board) -> str:
    """
    IFEN (Infinite FEN) format:
    [Slice1]/[Slice2]/.../[Slice18] [Turn: w/b] [EP: -/coord]
    Inside slice: 4 chars for Ring A, B, C, D. Empty as numbers (like '2P1').
    Pawn notation: P+ (White dir 1), P- (White dir -1), p+ (Black dir 1), p- (Black dir -1).
    Other pieces: K, Q, R, B, N, k, q, r, b, n.
    """
    ifen_slices = []
    piece_map = {
        PieceType.PAWN: 'P',
        PieceType.KNIGHT: 'N',
        PieceType.BISHOP: 'B',
        PieceType.ROOK: 'R',
        PieceType.QUEEN: 'Q',
        PieceType.KING: 'K'
    }

    for s in range(1, 19):
        slice_str = ""
        empty_count = 0
        for r in [Ring.A, Ring.B, Ring.C, Ring.D]:
            coord = Coordinate(r, s)
            piece = board.squares.get(coord)
            if piece:
                if empty_count > 0:
                    slice_str += str(empty_count)
                    empty_count = 0
                
                p_char = piece_map[piece.piece_type]
                if piece.color == Color.BLACK:
                    p_char = p_char.lower()
                
                if piece.piece_type == PieceType.PAWN:
                    # Direction matters
                    p_char += "+" if piece.direction == 1 else "-"
                
                slice_str += p_char
            else:
                empty_count += 1
        
        if empty_count > 0:
            slice_str += str(empty_count)
        ifen_slices.append(slice_str)
    
    turn = 'w' if board.turn == Color.WHITE else 'b'
    ep = str(board.en_passant_target) if board.en_passant_target else "-"
    return "/".join(ifen_slices) + f" {turn} {ep}"

def generate_svg(board: Board, filename: str, highlighted_moves: List[Move] = None):
    """
    Simple figure-eight SVG:
    Left loop: 12-18, Center: 9-10-11, Right loop: 1-7, Center: 18-1-2.
    """
    dwg = svgwrite.Drawing(filename, size=(800, 400))
    
    # Centers
    L_CENTER = (250, 200)
    R_CENTER = (550, 200)
    R_RADII = [40, 60, 80, 100]
    
    def get_coords(r: Ring, s: int):
        # Slices 1-7: Right loop
        # Slices 12-18: Left loop
        # Slices 8-11: Crossing
        
        angle_step = 360 / 18
        # Simple mapping for visualization:
        if 1 <= s <= 8 or s == 18:
            # Right loop
            # Offset angle so s=4 is on far right
            angle = (s - 4) * angle_step
            rad = R_RADII[r.value]
            x = R_CENTER[0] + rad * math.cos(math.radians(angle))
            y = R_CENTER[1] + rad * math.sin(math.radians(angle))
            return x, y
        else:
            # Left loop
            # Offset angle so s=13 is on far left
            angle = (s - 13) * angle_step
            rad = R_RADII[r.value]
            x = L_CENTER[0] + rad * math.cos(math.radians(angle))
            y = L_CENTER[1] + rad * math.sin(math.radians(angle))
            return x, y

    # Draw Tiles
    colors = ["#f88", "#8f8", "#ff8", "#88f"]
    for s in range(1, 19):
        for r in Ring:
            x, y = get_coords(r, s)
            color = colors[(r.value + s) % 4]
            dwg.add(dwg.circle(center=(x, y), r=15, fill=color, stroke='black'))
            dwg.add(dwg.text(f"{r.name}{s}", insert=(x-8, y+4), font_size=8, fill='black'))

    # Highlight moves
    if highlighted_moves:
        for move in highlighted_moves:
            x, y = get_coords(move.end.ring, move.end.slice)
            dwg.add(dwg.circle(center=(x, y), r=18, fill='none', stroke='cyan', stroke_width=3))

    # Draw pieces
    piece_chars = {
        PieceType.PAWN: 'P', PieceType.KNIGHT: 'N', PieceType.BISHOP: 'B',
        PieceType.ROOK: 'R', PieceType.QUEEN: 'Q', PieceType.KING: 'K'
    }
    for coord, piece in board.squares.items():
        x, y = get_coords(coord.ring, coord.slice)
        p_color = 'white' if piece.color == Color.WHITE else 'black'
        p_stroke = 'black' if piece.color == Color.WHITE else 'white'
        char = piece_chars[piece.piece_type]
        dwg.add(dwg.text(char, insert=(x-5, y+5), font_size=16, fill=p_color, stroke=p_stroke, stroke_width=0.5, font_weight='bold'))

    dwg.save()

def main():
    board = Board()
    board.reset()
    
    ifen = to_ifen(board)
    legal_moves = list(board.generate_legal_moves())
    
    # Sort for deterministic output
    legal_moves.sort(key=lambda m: (m.start.slice, m.start.ring.value, m.end.slice, m.end.ring.value))
    moves_str = ", ".join(str(m) for m in legal_moves)
    
    os.makedirs("infinite-chess/tests/visuals", exist_ok=True)
    generate_svg(board, "infinite-chess/tests/visuals/start_position.svg")
    generate_svg(board, "infinite-chess/tests/visuals/start_moves.svg", highlighted_moves=legal_moves)
    
    readme_content = f"""# Test Visualizations

This directory contains visual representations of board states and legal move generation to verify the engine's behavior.

## Standard Starting Position

**IFEN (Infinite FEN):** `{ifen}`

![Start Position](visuals/start_position.svg)

## Legal Moves from Start Position

The following image highlights all available legal moves for White (Turn: w) in the starting position.

![Legal Moves from Start](visuals/start_moves.svg)

### Legal Moves List ({len(legal_moves)} moves):
`{moves_str}`
"""
    with open("infinite-chess/tests/README.md", "w") as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
