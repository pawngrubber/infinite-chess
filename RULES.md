# Infinite Chess Rules

Official rules for the Infinite Chess variant created by **PhoenixfischTheFish** on r/AnarchyChess.

## 1. The Board Topology & Coordinates
The board is a non-Euclidean tiling of 72 tiles defined by four color complexes: **Red (R), Yellow (Y), Blue (B), and Green (G)**.

### The Coordinate System
The game uses a polar-lemniscate notation system to map the board's complex geometry:
- **Rings (A, B, C, D)**: There are four concentric tracks. Ring 'A' is the innermost loop closest to the holes, progressing outward to ring 'D' on the exterior boundary.
- **Slices (1 to 18)**: The board is divided into 18 radial segments that follow the path of the lemniscate. Slices 1-7 wrap around the right loop, 8-11 span the crossing intersection, and 12-18 wrap around the left loop.
- A tile is uniquely identified by combining its ring and slice (e.g., **A1**).
- **The Intersection**: Slice 9 and Slice 18 are physically adjacent at the crossing point, allowing specialized movement between the two loops.

### Color Connections
Tile color is determined by the formula: `(ring_index + slice_index) % 4`.
- **Complexes**: This creates four distinct color complexes. 
- **Restrictions**: Pieces like Bishops are strictly confined to their specific color complex (e.g., a Bishop starting on a Red tile can only ever move to Yellow, Blue, or Green tiles within its allowed complex path).

## 2. Piece Movement
Movement rules are based on standard chess but adapted to the non-Euclidean geometry:

### Rooks (Straight)
- Move along a single **Ring** (changing slice) or a single **Slice** (changing ring).
- Rooks orbit the loops indefinitely unless blocked.

### Bishops (Diagonal)
- Move by simultaneously changing both **Ring** and **Slice** at each step.
- Bishops follow the "zig-zag" diagonal paths defined by the lemniscate's tiling.

### Knights
- Move in an "L" shape: 2 steps in one cardinal direction (Ring or Slice) and 1 step perpendicularly.
- **Wormhole Jumps**: Knights can jump across the central intersection (e.g., from Slice 9 to specific tiles on Slice 18) following the physical crossing logic.

### Queens
- Combine the movement of the Rook and Bishop.

### Kings
- Move one tile in any direction (including diagonals).
- **Teleportation**: Kings can step directly between Slice 9 and Slice 18 where the loops physically cross in the center.

### Pawns
- **Movement**: Move one tile "forward" along their slice path.
- **Directionality**: Pawns must maintain their initial heading (+1 or -1 slice index).
- **Promotion**: Occurs after moving **10 spaces** forward from the starting position. 
- **En Passant**: **Mandatory**. If an En Passant capture is available, it must be taken. The target is created when a pawn makes a double-step move from its starting position.

## 3. Special Mechanics
- **No Castling**: Due to the non-Euclidean nature of the starting wedge, castling is not supported.
- **Matchmaking**: Players are paired into private rooms via the central server.
- **Victory**: Standard Checkmate rules apply. A player is in check if their King is under attack by an enemy piece, considering all non-Euclidean paths.
