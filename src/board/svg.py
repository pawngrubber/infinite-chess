import math
from typing import Dict, Iterable
import chess.svg
from .board import Board, Color, PieceType
from .logic import Coordinate, Ring

def polar_to_cartesian(cx, cy, r, angle):
    return {
        "x": cx + r * math.cos(angle),
        "y": cy + r * math.sin(angle)
    }

def get_piece_svg(piece_char, is_white):
    piece_type = {
        'P': chess.PAWN,
        'N': chess.KNIGHT,
        'B': chess.BISHOP,
        'R': chess.ROOK,
        'Q': chess.QUEEN,
        'K': chess.KING
    }[piece_char.upper()]
    color = chess.WHITE if is_white else chess.BLACK
    full_svg = chess.svg.piece(chess.Piece(piece_type, color))
    start = full_svg.find(">") + 1
    end = full_svg.rfind("</svg>")
    return full_svg[start:end]

class Arrow:
    def __init__(self, tail: Coordinate, head: Coordinate, color: str = "green"):
        self.tail = tail
        self.head = head
        self.color = color

def board_to_svg(board: Board, highlights: Dict[Coordinate, str] = None, arrows: Iterable[Arrow] = None) -> str:
    if highlights is None:
        highlights = {}
    if arrows is None:
        arrows = []
    tile_size = 100
    light_color = '#ebd7b5'
    dark_color = '#ad7f5d'
    
    # Mapping table: Coordinate -> (x, y)
    coords = {}

    # 1. Core 4x4 (Ranks 8-11)
    for row in range(4):
        for col in range(4):
            lane = ['D', 'C', 'B', 'A'][col]
            ring = Ring[lane]
            rank = 8 + row
            coords[Coordinate(ring, rank)] = (col * tile_size + 50, row * tile_size + 50)

    # 2. Right Lobe (Ranks 1-7)
    cx_r, cy_r = 500, -100
    for r in range(4):
        lane = ['A', 'B', 'C', 'D'][r]
        ring = Ring[lane]
        for s in range(7):
            rank = 7 - s
            if s == 0:
                tx, ty = (3 - r) * 100 + 50, -50
            elif s == 6:
                tx, ty = 450, r * 100 + 50
            else:
                mid_angle = (180 + 22.5 + (s - 0.5) * 45) * math.pi / 180
                mp = polar_to_cartesian(cx_r, cy_r, (r + 1.5) * 100, mid_angle)
                tx, ty = mp["x"], mp["y"]
            coords[Coordinate(ring, rank)] = (tx, ty)

    # 3. Left Lobe (Ranks 12-18)
    cx_l, cy_l = -100, 500
    for r in range(4):
        lane = ['D', 'C', 'B', 'A'][r]
        ring = Ring[lane]
        for s in range(7):
            rank = 12 + s
            if s == 0:
                tx, ty = r * 100 + 50, 450
            elif s == 6:
                tx, ty = -50, (3 - r) * 100 + 50
            else:
                mid_angle = (22.5 + (s - 0.5) * 45) * math.pi / 180
                mp = polar_to_cartesian(cx_l, cy_l, (r + 1.5) * 100, mid_angle)
                tx, ty = mp["x"], mp["y"]
            coords[Coordinate(ring, rank)] = (tx, ty)

    paths = []
    
    # Render Tiles
    for row in range(4):
        for col in range(4):
            is_light = (row + col) % 2 != 0
            coord = Coordinate(['D', 'C', 'B', 'A'][col], 8 + row)
            fill = highlights.get(coord, light_color if is_light else dark_color)
            paths.append(f'<rect x="{col * tile_size}" y="{row * tile_size}" width="{tile_size}" height="{tile_size}" fill="{fill}" stroke="#000" stroke-width="1.5" />')

    def get_lobe_paths(cx, cy, is_left):
        lobe_paths = []
        for r in range(4):
            R1, R2 = (r + 1) * tile_size, (r + 2) * tile_size
            lane = (['D', 'C', 'B', 'A'] if is_left else ['A', 'B', 'C', 'D'])[r]
            for s in range(7):
                is_light = (r + s) % 2 != 0
                rank = (12 + s) if is_left else (7 - s)
                coord = Coordinate(Ring[lane], rank)
                fill = highlights.get(coord, light_color if is_light else dark_color)
                
                if s == 0:
                    if not is_left:
                        theta2, c = 202.5 * math.pi / 180, 3 - r
                        p2, p3 = polar_to_cartesian(cx, cy, R2, theta2), polar_to_cartesian(cx, cy, R1, theta2)
                        d = f'M {c * 100} 0 L {c * 100} -100 A {R2} {R2} 0 0 1 {p2["x"]} {p2["y"]} L {p3["x"]} {p3["y"]} A {R1} {R1} 0 0 0 {(c + 1) * 100} -100 L {(c + 1) * 100} 0 Z'
                    else:
                        theta2 = 22.5 * math.pi / 180
                        p3, p4 = polar_to_cartesian(cx, cy, R2, theta2), polar_to_cartesian(cx, cy, R1, theta2)
                        d = f'M {r * 100} 400 L {(r + 1) * 100} 400 L {(r + 1) * 100} 500 A {R2} {R2} 0 0 1 {p3["x"]} {p3["y"]} L {p4["x"]} {p4["y"]} A {R1} {R1} 0 0 0 {r * 100} 500 Z'
                elif s == 6:
                    if not is_left:
                        theta1 = 427.5 * math.pi / 180
                        p1, p2 = polar_to_cartesian(cx, cy, R1, theta1), polar_to_cartesian(cx, cy, R2, theta1)
                        d = f'M {p1["x"]} {p1["y"]} L {p2["x"]} {p2["y"]} A {R2} {R2} 0 0 1 500 {(r + 1) * 100} L 400 {(r + 1) * 100} L 400 {r * 100} L 500 {r * 100} A {R1} {R1} 0 0 0 {p1["x"]} {p1["y"]} Z'
                    else:
                        theta1 = 247.5 * math.pi / 180
                        p1, p2 = polar_to_cartesian(cx, cy, R1, theta1), polar_to_cartesian(cx, cy, R2, theta1)
                        d = f'M {p1["x"]} {p1["y"]} L {p2["x"]} {p2["y"]} A {R2} {R2} 0 0 1 -100 {(3 - r) * 100} L 0 {(3 - r) * 100} L 0 {(4 - r) * 100} L -100 {(4 - r) * 100} A {R1} {R1} 0 0 0 {p1["x"]} {p1["y"]} Z'
                else:
                    base = 180 + 22.5 if not is_left else 22.5
                    t1, t2 = (base + (s - 1) * 45) * math.pi / 180, (base + s * 45) * math.pi / 180
                    p1, p2, p3, p4 = polar_to_cartesian(cx, cy, R1, t1), polar_to_cartesian(cx, cy, R2, t1), polar_to_cartesian(cx, cy, R2, t2), polar_to_cartesian(cx, cy, R1, t2)
                    d = f'M {p1["x"]} {p1["y"]} L {p2["x"]} {p2["y"]} A {R2} {R2} 0 0 1 {p3["x"]} {p3["y"]} L {p4["x"]} {p4["y"]} A {R1} {R1} 0 0 0 {p1["x"]} {p1["y"]} Z'
                lobe_paths.append(f'<path d="{d}" fill="{fill}" stroke="#000" stroke-width="1.5" />')
        return lobe_paths

    paths.extend(get_lobe_paths(cx_r, cy_r, False))
    paths.extend(get_lobe_paths(cx_l, cy_l, True))

    # Render Pieces
    piece_symbols = {
        PieceType.PAWN: 'P',
        PieceType.KNIGHT: 'N',
        PieceType.BISHOP: 'B',
        PieceType.ROOK: 'R',
        PieceType.QUEEN: 'Q',
        PieceType.KING: 'K'
    }

    for coord, piece in board.squares.items():
        if coord in coords:
            x, y = coords[coord]
            char = piece_symbols[piece.piece_type]
            is_white = piece.color == Color.WHITE
            content = get_piece_svg(char, is_white)
            scale = 1.9
            paths.append(f'<g transform="translate({x}, {y}) rotate(-45) scale({scale}) translate(-22.5, -22.5)" filter="url(#shadow)">{content}</g>')

    # Render Arrows
    arrow_colors = {
        "green": "#15781B80",
        "red": "#88202080",
        "yellow": "#e68f00b3",
        "blue": "#00308880",
    }

    for arrow in arrows:
        if arrow.tail in coords and arrow.head in coords:
            xtail, ytail = coords[arrow.tail]
            xhead, yhead = coords[arrow.head]
            color = arrow_colors.get(arrow.color, arrow.color)
            
            if (xtail, ytail) == (xhead, yhead):
                paths.append(f'<circle cx="{xhead}" cy="{yhead}" r="40" stroke-width="10" stroke="{color}" fill="none" />')
            else:
                marker_size = 35
                marker_margin = 5
                dx, dy = xhead - xtail, yhead - ytail
                hypot = math.hypot(dx, dy)
                shaft_x = xhead - dx * (marker_size + marker_margin) / hypot
                shaft_y = yhead - dy * (marker_size + marker_margin) / hypot
                xtip = xhead - dx * marker_margin / hypot
                ytip = yhead - dy * marker_margin / hypot
                
                paths.append(f'<line x1="{xtail}" y1="{ytail}" x2="{shaft_x}" y2="{shaft_y}" stroke="{color}" stroke-width="20" stroke-linecap="butt" />')
                
                # Marker polygon
                p1 = (xtip, ytip)
                p2 = (shaft_x + dy * 0.5 * marker_size / hypot, shaft_y - dx * 0.5 * marker_size / hypot)
                p3 = (shaft_x - dy * 0.5 * marker_size / hypot, shaft_y + dx * 0.5 * marker_size / hypot)
                points = f"{p1[0]},{p1[1]} {p2[0]},{p2[1]} {p3[0]},{p3[1]}"
                paths.append(f'<polygon points="{points}" fill="{color}" />')

    content = "\n".join(paths)
    svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg viewBox="0 0 2400 2400" xmlns="http://www.w3.org/2000/svg">
<defs>
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feGaussianBlur in="SourceAlpha" stdDeviation="2"/>
        <feOffset dx="1" dy="2" result="offsetblur"/>
        <feComponentTransfer>
            <feFuncA type="linear" slope="0.5"/>
        </feComponentTransfer>
        <feMerge>
            <feMergeNode/>
            <feMergeNode in="SourceGraphic"/>
        </feMerge>
    </filter>
</defs>
<rect width="100%" height="100%" fill="#000" />
<g transform="translate(1200, 1200) rotate(45) translate(-200, -200)">
{content}
</g>
</svg>"""
    return svg
