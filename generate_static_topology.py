# /// script
# dependencies = [
#   "svgwrite",
# ]
# ///

import math
import os
import svgwrite

def polar_to_cartesian(cx, cy, r, angle):
    return {
        'x': cx + r * math.cos(angle),
        'y': cy + r * math.sin(angle)
    }

def generate_topology_svg(filename):
    # Set a wider aspect ratio (1600x1000) to fit the horizontal figure-eight
    width, height = 1600, 1000
    dwg = svgwrite.Drawing(filename, size=(width, height), viewBox=f"0 0 {width} {height}")
    dwg.add(dwg.rect(insert=(0, 0), size=('100%', '100%'), fill='#000000'))
    
    # Translate to 800 (half of 1600) and 500 (half of 1000)
    # The 'rotate(45) translate(-200, -200)' establishes the diamond crossing at this center
    main_group = dwg.g(id='board-group', transform=f'translate({width/2}, {height/2}) rotate(45) translate(-200, -200)')
    dwg.add(main_group)

    tile_size = 100
    light_color = '#ebd7b5'
    dark_color = '#ad7f5d'

    def draw_rect_tile(col, row):
        is_light = abs(row + col) % 2 == 0
        fill = light_color if is_light else dark_color
        main_group.add(dwg.rect(
            insert=(col * tile_size, row * tile_size),
            size=(tile_size, tile_size),
            fill=fill,
            stroke='#000000',
            stroke_width=1.5
        ))

    def draw_arc_tile(cx, cy, r1, r2, theta1, theta2, is_light):
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

    # 1. Core 4x4
    for row in range(4):
        for col in range(4):
            draw_rect_tile(col, row)

    # 2. Right Extensions
    for col in range(4): draw_rect_tile(col, -1)
    for row in range(4): draw_rect_tile(4, row)

    # 3. Left Extensions
    for row in range(4): draw_rect_tile(-1, row)
    for col in range(4): draw_rect_tile(col, 4)

    # 4. Right Lobe
    cx, cy = 500, -100
    start_angle, end_angle = math.pi, math.pi * 2.5
    segments = 5
    for ring in range(4):
        r1, r2 = (ring + 1) * tile_size, (ring + 2) * tile_size
        for s in range(segments):
            theta1 = start_angle + (s / segments) * (end_angle - start_angle)
            theta2 = start_angle + ((s + 1) / segments) * (end_angle - start_angle)
            is_light = (ring + s + 1) % 2 == 0
            draw_arc_tile(cx, cy, r1, r2, theta1, theta2, is_light)

    # 5. Left Lobe
    cx, cy = -100, 500
    start_angle, end_angle = 0, math.pi * 1.5
    for ring in range(4):
        r1, r2 = (ring + 1) * tile_size, (ring + 2) * tile_size
        for s in range(segments):
            theta1 = start_angle + (s / segments) * (end_angle - start_angle)
            theta2 = start_angle + ((s + 1) / segments) * (end_angle - start_angle)
            is_light = (ring + s + 1) % 2 == 0
            draw_arc_tile(cx, cy, r1, r2, theta1, theta2, is_light)

    dwg.save()

if __name__ == "__main__":
    os.makedirs("assets", exist_ok=True)
    generate_topology_svg("assets/board_topology.svg")
