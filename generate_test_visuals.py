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

def polar_to_cart(cx, cy, r, deg):
    rad = math.radians(deg)
    return cx + r * math.cos(rad), cy - r * math.sin(rad)

def get_arc_path(cx, cy, r_in, r_out, a_start, a_end):
    p1 = polar_to_cart(cx, cy, r_out, a_start)
    p2 = polar_to_cart(cx, cy, r_out, a_end)
    p3 = polar_to_cart(cx, cy, r_in, a_end)
    p4 = polar_to_cart(cx, cy, r_in, a_start)
    
    # In SVG (Y down), an arc from lower math angle to higher math angle goes visual CCW.
    # sweep-flag 0 usually means "negative angle direction" in SVG coordinate space.
    # Since our math Y is flipped (cy - ...), a sweep of 0 correctly bulges outward.
    d = f"M {p1[0]:.2f} {p1[1]:.2f} "
    d += f"A {r_out} {r_out} 0 0 0 {p2[0]:.2f} {p2[1]:.2f} "
    d += f"L {p3[0]:.2f} {p3[1]:.2f} "
    d += f"A {r_in} {r_in} 0 0 1 {p4[0]:.2f} {p4[1]:.2f} "
    d += "Z"
    return d

def generate_svg(board: Board, filename: str, highlighted_moves: List[Move] = None):
    dwg = svgwrite.Drawing(filename, size=(1000, 600))
    
    # Background
    dwg.add(dwg.rect(insert=(0,0), size=('100%', '100%'), fill='#1a1a1a'))
    
    C_L = (350, 300)
    C_R = (650, 300)
    
    # Thick tracks
    ring_radii = {
        Ring.A: (60, 100),
        Ring.B: (100, 140),
        Ring.C: (140, 180),
        Ring.D: (180, 220)
    }
    
    right_slices = {
        18: 200, 1: 240, 2: 280, 3: 320, 
        4: 0, 5: 40, 6: 80, 7: 120, 8: 160
    }
    left_slices = {
        9: 340, 10: 300, 11: 260, 12: 220, 
        13: 180, 14: 140, 15: 100, 16: 60, 17: 20
    }
    
    colors = ["#ff5252", "#32ff7e", "#fffa65", "#18dcff"]
    tile_centers = {}
    
    def draw_loop(center, slices_dict):
        for slice_num, ang_mid in slices_dict.items():
            a_start = ang_mid - 20
            a_end = ang_mid + 20
            for ring in Ring:
                r_in, r_out = ring_radii[ring]
                path_d = get_arc_path(center[0], center[1], r_in, r_out, a_start, a_end)
                
                # Colors according to rules
                color_idx = (ring.value + slice_num) % 4
                fill_color = colors[color_idx]
                
                dwg.add(dwg.path(d=path_d, fill=fill_color, stroke='#222222', stroke_width=2, opacity=0.75))
                
                # Store center
                c_mid = (r_in + r_out) / 2
                tcx, tcy = polar_to_cart(center[0], center[1], c_mid, ang_mid)
                tile_centers[Coordinate(ring, slice_num)] = (tcx, tcy)
                
                # Label
                dwg.add(dwg.text(f"{ring.name}{slice_num}", insert=(tcx, tcy+16), font_size=10, fill='#000000', text_anchor='middle', font_family='monospace', font_weight='bold', opacity=0.4))
    
    # Draw overlapping loops
    draw_loop(C_L, left_slices)
    draw_loop(C_R, right_slices)
    
    # Highlight moves
    if highlighted_moves:
        for move in highlighted_moves:
            tcx, tcy = tile_centers[move.end]
            dwg.add(dwg.circle(center=(tcx, tcy), r=18, fill='none', stroke='#ff00ff', stroke_width=4, opacity=0.9))
            if move.is_capture:
                dwg.add(dwg.circle(center=(tcx, tcy), r=18, fill='#ff0000', opacity=0.5))
                
    # Draw Pieces
    piece_chars = {
        PieceType.PAWN: '♟', PieceType.KNIGHT: '♞', PieceType.BISHOP: '♝',
        PieceType.ROOK: '♜', PieceType.QUEEN: '♛', PieceType.KING: '♚'
    }
    
    for coord, piece in board.squares.items():
        if coord not in tile_centers: continue
        tcx, tcy = tile_centers[coord]
        
        char = piece_chars[piece.piece_type]
        color = '#ffffff' if piece.color == Color.WHITE else '#000000'
        stroke = '#000000' if piece.color == Color.WHITE else '#ffffff'
        
        # Render unicode piece with a nice shadow/outline
        dwg.add(dwg.text(char, insert=(tcx, tcy+10), font_size=32, fill=color, stroke=stroke, stroke_width=1.5, text_anchor='middle', font_family='sans-serif'))

    dwg.save()

def main():
    board = Board()
    board.reset()
    
    ifen = to_ifen(board)
    legal_moves = list(board.generate_legal_moves())
    legal_moves.sort(key=lambda m: (m.start.slice, m.start.ring.value, m.end.slice, m.end.ring.value))
    moves_str = ", ".join(str(m) for m in legal_moves)
    
    os.makedirs("tests/visuals", exist_ok=True)
    generate_svg(board, "tests/visuals/start_position.svg")
    generate_svg(board, "tests/visuals/start_moves.svg", highlighted_moves=legal_moves)
    
    readme_content = f"""# Test Visualizations

This directory contains high-quality visual representations of board states and legal move generation to verify the engine's behavior, specifically mapped to the true Lemniscate figure-eight topology.

## Standard Starting Position

**IFEN (Infinite FEN):** `{ifen}`

![Start Position](visuals/start_position.svg)

## Legal Moves from Start Position

The following image highlights all available legal moves for White (Turn: w) in the starting position.

![Legal Moves from Start](visuals/start_moves.svg)

### Legal Moves List ({len(legal_moves)} moves):
`{moves_str}`
"""
    with open("tests/README.md", "w") as f:
        f.write(readme_content)

if __name__ == "__main__":
    main()
