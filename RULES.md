# Infinite Chess Rules

Official rules for the Infinite Chess variant created by **PhoenixfischTheFish** on r/AnarchyChess.

## 1. The Board Topology (Color Rules)
The board is a non-Euclidean tiling defined by four colors: **Red (R), Yellow (Y), Blue (B), and Green (G)**.

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
- Move "forward" toward the opponent's starting side.
- **Promotion**: Occurs when a pawn reaches the "opposing royal tile row" (where the opponent's King/Queen started).
- **En Passant**: Mandatory (as per r/AnarchyChess tradition).

## 3. Special Mechanics
- **Royal Lineup Tiles**: Special tiles where standard color connectivity might appear to conflict. These are treated as standard tiles for movement to maintain game flow.
- **Matchmaking**: Players are paired anonymously into infinite loops.
- **Victory**: Standard Checkmate rules apply, though navigating the infinite geometry makes this significantly more complex.
