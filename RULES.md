# Infinite Chess Rules

Official rules for the Infinite Chess variant created by **PhoenixfischTheFish** on r/AnarchyChess.

## 1. The Board Topology & Coordinates
The board is a non-Euclidean tiling of 72 squares defined by four colors: **Red (R), Yellow (Y), Blue (B), and Green (G)**.

### The Coordinate System
The game uses a polar-lemniscate notation system to map the board's complex geometry:
- **Rings (A, B, C, D)**: There are four concentric tracks. Ring 'A' is the innermost loop closest to the holes, progressing outward to ring 'D' on the exterior boundary.
- **Slices (1 to 18)**: The board is divided into 18 radial segments that follow the path of the lemniscate. Slices 1-7 wrap around the right loop, 8-11 span the crossing intersection, and 12-18 wrap around the left loop.
- A tile is uniquely identified by combining its ring and slice (e.g., **A1** is the innermost tile at the start of the right loop).

### Color Connections
- **Opposites**: Red is always opposite Yellow; Blue is always opposite Green.
- **Connectivity**: Red tiles connect to Yellow tiles from adjacent sides; Blue connects to Green.
- **Rotation**: The colors follow a clockwise rotation: **Red → Green → Yellow → Blue → Red**.
- **The Loop**: The board is geometrically infinite. Straight lines eventually return to their origin or continue indefinitely.

## 2. Piece Movement
Movement rules are based on standard chess but adapted to the color-tiled geometry:

### Rooks (Straight)
- Move through adjacent tiles by following the "opposite" color rule.
- Example: From a **Red** tile, a Rook moves into an adjacent **Yellow** tile to continue a "straight" line.

### Bishops (Diagonal)
- Move diagonally by following specific color connection paths.
- If a Bishop leaves a **Green** tile, it must enter a **Blue** tile and continue alternating between those two colors.

### Knights
- Move in the standard "L" shape (two squares in one cardinal direction and one square perpendicular).
- The "perpendicular" direction is determined by the clockwise/counter-clockwise rotation of the colors.

### Queens
- Combine the movement of the Rook and Bishop.

### Kings
- Move one tile in any direction.
- Due to the board's topology, the King can transition between different "loops" of the lemniscate.

### Pawns
- **Movement**: Move one tile "forward" toward the opponent's starting side.
- **Directionality (The Heading Marker)**: In the middle intersection of the lemniscate, "forward" can be ambiguous. Pawns must always continue in their original direction. To track this, pieces should have a physical or digital marker indicating their current heading.
- **Promotion**: Occurs when a pawn reaches the **opposing royal tile row** (the row where the opponent's King and Queen were originally stationed).
- **Distance**: On the infinity board, promotion typically requires moving **10 spaces** forward from the starting position.
- **En Passant**: Mandatory (as per r/AnarchyChess tradition). It follows standard logic but can occur in geometrically varied positions due to the board's curve.


## 3. Special Mechanics
- **Royal Lineup Tiles**: Special tiles where standard color connectivity might appear to conflict. These are treated as standard tiles for movement to maintain game flow.
- **Matchmaking**: Players are paired anonymously into infinite loops.
- **Victory**: Standard Checkmate rules apply, though navigating the infinite geometry makes this significantly more complex.
