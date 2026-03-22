# /// script
# dependencies = [
#   "svgwrite",
# ]
# ///

import math
import os
import sys
import svgwrite

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from board.board import Board, Color, PieceType
from board.logic import Coordinate, Ring

# Standard Wikimedia Chess Piece Paths
PIECE_PATHS = {
    'K': "M 22.5,11.63 V 6 M 20,8 h 5 M 22.5,25 C 22.5,25 27,17.5 27,13 C 27,10.51 24.99,8.5 22.5,8.5 C 20.01,8.5 18,10.51 18,13 C 18,17.5 22.5,25 22.5,25 Z M 11.5,37 c 5.5,3.5 15.5,3.5 21,0 v -7 s 9,-4.5 9,-14 c 0,-4 -2,-8 -6,-10 c -4,-2 -8,0 -10,1 c -2,-1 -6,-3 -10,-1 c -4,2 -6,6 -6,10 c 0,9.5 9,14 9,14 v 7 z M 9,26 c 8.5,-1.5 18.5,-1.5 27,0 M 11.5,30 c 5.5,-3 15.5,-3 21,0 m -21,3.5 c 5.5,-3 15.5,-3 21,0",
    'Q': "M 9 26 c 8.5 -1.5 18.5 -1.5 27 0 M 9 26 c 0 2 2 4.5 2 4.5 c 5 3 15 3 20 0 c 0 0 2 -2.5 2 -4.5 M 11.5 30 c 5.5 -3 15.5 -3 21 0 m -21 3.5 c 5.5 -3 15.5 -3 21 0 M 9 26 L 6 10 L 12 18 L 18 6 L 22.5 18 L 27 6 L 33 18 L 39 10 L 36 26 M 12 18 a 2 2 0 1 1 -4 0 a 2 2 0 1 1 4 0 z M 18 6 a 2 2 0 1 1 -4 0 a 2 2 0 1 1 4 0 z M 24.5 6 a 2 2 0 1 1 -4 0 a 2 2 0 1 1 4 0 z M 31 6 a 2 2 0 1 1 -4 0 a 2 2 0 1 1 4 0 z M 38 18 a 2 2 0 1 1 -4 0 a 2 2 0 1 1 4 0 z",
    'R': "M 9,39 h 27 v -3 H 9 v 3 z M 12,36 v -4 h 21 v 4 H 12 z M 11,14 V 9 h 4 v 2 h 5 V 9 h 5 v 2 h 5 V 9 h 4 v 5",
    'B': "M 9,36 c 3,3.5 24,3.5 27,0 M 15,32 c 2.5,2.5 12.5,2.5 15,0 M 9,26 c 3.995,1.583 12.662,2.25 18,2.25 c 5.338,0 14.005,-0.667 18,-2.25 M 17,21 c -2,2 -2,4 0,6 c 2,2 5,2 7,0 c 2,-2 2,-4 0,-6 c -2,-2 -5,-2 -7,0 z M 12,12 c 4,12 21,12 25,0 c 1,-1 1,-4 -2,-6 c -3,-2 -6,-2 -8,0 c -2,2 -3,2 -4,0 c -1,-1 -4,-3 -7,-2 c -3,1 -5,4 -4,8 z M 26,13 a 2,2 0 1 1 -4,0 a 2,2 0 1 1 4,0 z",
    'N': "M 22,10 c 10.5,1 16.5,8 16,29 H 15 c 0,-9 10,-6.5 8,-21",
    'P': "M 22.5,9 a 5,5 0 1 1 -10,0 a 5,5 0 1 1 10,0 z M 22.5,14 c -6,0 -10,6 -10,12 c 0,1.5 0,3 0,4.5 h 20 c 0,-1.5 0,-3 0,-4.5 c 0,-6 -4,-12 -10,-12 z M 12.5,31 c 0,1.5 1,3 2.5,3 h 15 c 1.5,0 2.5,-1.5 2.5,-3 h -20 z m 0,3.5 c 0,1.5 1,3 2.5,3 h 15 c 1.5,0 2.5,-1.5 2.5,-3 h -20 z m -2.5,4 c 0,1.5 1.5,3 3,3 h 19 c 1.5,0 3,-1.5 3,-3 h -25 z"
}

def polar_to_cartesian(cx, cy, r, angle):
    return {
        'x': cx + r * math.cos(angle),
        'y': cy + r * math.sin(angle)
    }

def draw_rect_tile(dwg, main_group, col, row, tile_size, light_color, dark_color):
    is_light = abs(row + col) % 2 == 0
    fill = light_color if is_light else dark_color
    main_group.add(dwg.rect(
        insert=(col * tile_size, row * tile_size),
        size=(tile_size, tile_size),
        fill=fill,
        stroke='#000000',
        stroke_width=1.5
    ))

def draw_arc_tile(dwg, main_group, cx, cy, r1, r2, theta1, theta2, is_light, light_color, dark_color):
    p1 = polar_to_cartesian(cx, cy, r1, theta1)
    p2 = polar_to_cartesian(cx, cy, r2, theta1)
    p3 = polar_to_cartesian(cx, cy, r2, theta2)
    p4 = polar_to_cartesian(cx, cy, r1, theta2)

    path_data = f"M {p1['x']} {p1['y']} L {p2['x']} {p2['y']} "
    path_data += f"A {r2} {r2} 0 0 1 {p3['x']} {p3['y']} "
    path_data += f"L {p4['x']} {p4['y']} "
    path_data += f"A {r1} {r1} 0 0 0 {p1['x']} {p1['y']} Z"

    fill = light_color if is_light else dark_color
    main_group.add(dwg.path(d=path_data, fill=fill, stroke='#000000', stroke_width=1.5))

def draw_piece(dwg, main_group, x, y, type_char, color):
    # Scale pieces down slightly from 45x45 to fit 100x100 tiles better
    scale = 1.2
    offset = (45 * scale) / 2
    piece_group = dwg.g(transform=f"translate({x-offset}, {y-offset}) scale({scale})")
    path_data = PIECE_PATHS[type_char]
    fill = "white" if color == Color.WHITE else "black"
    stroke = "black" if color == Color.WHITE else "white"
    piece_group.add(dwg.path(d=path_data, fill=fill, stroke=stroke, stroke_width=1.5))
    main_group.add(piece_group)

def generate_starting_position_svg(filename):
    print("Generating board layout...")
    width, height = 2200, 1100
    dwg = svgwrite.Drawing(filename, size=(width, height), viewBox=f"0 0 {width} {height}")
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='#000000'))
    
    main_group = dwg.g(id='board-group', transform=f'translate({width/2}, {height/2}) scale(0.9) rotate(45) translate(-200, -200)')
    dwg.add(main_group)

    tile_size = 100
    light_color = '#ebd7b5'
    dark_color = '#ad7f5d'

    # 1. Core 4x4
    for row in range(4):
        for col in range(4):
            draw_rect_tile(dwg, main_group, col, row, tile_size, light_color, dark_color)

    # 2. Extensions
    for col in range(4): draw_rect_tile(dwg, main_group, col, -1, tile_size, light_color, dark_color)
    for row in range(4): draw_rect_tile(dwg, main_group, 4, row, tile_size, light_color, dark_color)
    for row in range(4): draw_rect_tile(dwg, main_group, -1, row, tile_size, light_color, dark_color)
    for col in range(4): draw_rect_tile(dwg, main_group, col, 4, tile_size, light_color, dark_color)

    # 3. Lobes
    segments = 5
    # Right Lobe
    cx, cy = 500, -100
    start_angle, end_angle = math.pi, math.pi * 2.5
    for ring in range(4):
        r1, r2 = (ring + 1) * tile_size, (ring + 2) * tile_size
        for s in range(segments):
            theta1 = start_angle + (s / segments) * (end_angle - start_angle)
            theta2 = start_angle + ((s + 1) / segments) * (end_angle - start_angle)
            is_light = (ring + s + 1) % 2 == 0
            draw_arc_tile(dwg, main_group, cx, cy, r1, r2, theta1, theta2, is_light, light_color, dark_color)

    # Left Lobe
    cx, cy = -100, 500
    start_angle, end_angle = 0, math.pi * 1.5
    for ring in range(4):
        r1, r2 = (ring + 1) * tile_size, (ring + 2) * tile_size
        for s in range(segments):
            theta1 = start_angle + (s / segments) * (end_angle - start_angle)
            theta2 = start_angle + ((s + 1) / segments) * (end_angle - start_angle)
            is_light = (ring + s + 1) % 2 == 0
            draw_arc_tile(dwg, main_group, cx, cy, r1, r2, theta1, theta2, is_light, light_color, dark_color)

    print("Placing pieces...")
    # Black Pieces (Top-Right)
    s4_theta = math.pi * 1.75
    draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 450, s4_theta).values(), 'K', Color.BLACK)
    draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 350, s4_theta).values(), 'Q', Color.BLACK)
    draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 250, s4_theta).values(), 'B', Color.BLACK)
    draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 150, s4_theta).values(), 'B', Color.BLACK)
    
    s2_theta, s6_theta = math.pi * 1.35, math.pi * 2.15
    draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 450, s2_theta).values(), 'R', Color.BLACK)
    draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 350, s2_theta).values(), 'N', Color.BLACK)
    draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 450, s6_theta).values(), 'R', Color.BLACK)
    draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 350, s6_theta).values(), 'N', Color.BLACK)
    
    for t in [math.pi*1.15, math.pi*1.55, math.pi*1.95, math.pi*2.35]:
        draw_piece(dwg, main_group, *polar_to_cartesian(500, -100, 250, t).values(), 'P', Color.BLACK)

    # White Pieces (Bottom-Left)
    s13_theta = math.pi * 0.75
    draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 450, s13_theta).values(), 'K', Color.WHITE)
    draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 350, s13_theta).values(), 'Q', Color.WHITE)
    draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 250, s13_theta).values(), 'B', Color.WHITE)
    draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 150, s13_theta).values(), 'B', Color.WHITE)
    
    s11_theta, s15_theta = math.pi * 0.35, math.pi * 1.15
    draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 450, s11_theta).values(), 'R', Color.WHITE)
    draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 350, s11_theta).values(), 'N', Color.WHITE)
    draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 450, s15_theta).values(), 'R', Color.WHITE)
    draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 350, s15_theta).values(), 'N', Color.WHITE)
    
    for t in [0.15*math.pi, 0.55*math.pi, 0.95*math.pi, 1.35*math.pi]:
        draw_piece(dwg, main_group, *polar_to_cartesian(-100, 500, 250, t).values(), 'P', Color.WHITE)

    print(f"Saving to {filename}...")
    dwg.save()

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    generate_starting_position_svg("assets/starting_position_topology.svg")
