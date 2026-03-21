# Infinite Chess Edge Cases & TDD Scenarios

When adapting standard chess to a Polar-Lemniscate (figure-eight) topology, the geometry breaks many assumptions inherent to an 8x8 grid. To build a robust `Board.get_legal_moves()` function, the engine must handle the intersection of these rules across the infinite loop.

Here are the critical families of edge cases that our Test-Driven Development (TDD) must validate:

## 1. The "Infinite" Sliding Pieces (Rooks, Queens, Bishops)
Because the board is a continuous loop, sliding pieces project power in non-Euclidean ways.
*   **The "Around-the-World" Check**: A Rook or Queen can attack a King from *behind* by wrapping entirely around the loop. The engine must trace lines of sight in both directions along a ring.
*   **Self-Intersection & Infinite Loops**: If a ring is completely empty, a Rook sliding along it will eventually reach its own starting square. A sliding piece cannot capture itself, and move generation must stop tracing once the origin is reached.
*   **The Double-Attack from One Piece**: Due to the loop, it may be possible for a Queen to attack a square simultaneously from the "front" and the "back" of the same ring. Blocking one path does not necessarily break the line of sight from the other path.

## 2. Intersection Madness (Slices 8-11)
The center of the lemniscate where the paths cross creates unique physical constraints.
*   **Head-On Pawn Collisions**: Because the loops twist, two pawns moving "forward" from opposite sides of the board might meet head-on at the intersection. The engine must correctly resolve blocking.
*   **King "Teleportation" Checks**: The King can step directly across the physical intersection (e.g., from Slice 9 to 18). The engine must verify if the King is in check when stepping across this gap, and whether it can capture pieces across it.
*   **Knight's "Wormhole" Jump**: The Knight moves in an L-shape. When positioned at the intersection (e.g., Slice 9), its L-shape might mathematically wrap across the intersection. We must ensure it lands on valid tiles and doesn't fall into the geometric void.

## 3. "Trans Passant" (En Passant on a Curve)
En Passant is structurally disconnected from the target square, which gets weirder on a curve.
*   **The Intersection En Passant**: A pawn moves two spaces across the center intersection. The capturing pawn must execute the diagonal capture across the geometric gap.
*   **The "En Passant Pin" (Loop Edition)**: Capturing En Passant removes two pawns from the same ring or slice. If removing these pawns opens a line of sight around the loop from an enemy Rook to the capturing King, the En Passant must be deemed illegal.

## 4. The "Phantom Threat" & Absolute Pins
Pieces project threat even when they cannot legally move.
*   **Sliding Along the Loop Pin**: A Rook pinned to its King along Ring A cannot move to Ring B. However, it *can* move freely forward and backward along Ring A, because doing so does not break the line of sight between the pinning piece and the King.
*   **Checking with a Pinned Piece**: A piece that is absolutely pinned can still deliver Check to the enemy King across the loops.
*   **The Pinned Defender**: A pinned piece still defends other pieces on its loop, preventing the enemy King from capturing them.

## 5. Directionality & State ("Ghost State")
*   **Pawn Directional Amnesia**: Pawns must track a `.forward_direction` state (usually +1 or -1). If a pawn travels all the way around the loop and ends up in its own starting zone, it continues in its stored direction. Move generation must respect the piece's memory, not just its coordinates.
*   **En Passant Expiration**: The right to capture En Passant must expire immediately if not used on the exact next ply.

## 6. Check Evasion Precedence
When the King is in check, move generation is heavily restricted.
*   **Blocking a Loop Check with a Pinned Piece**: Moving a piece to block a check might open a *different* line of sight to a different attacker behind the blocker (perhaps via the other side of the loop).
*   **Double Check Escapes**: If attacked by two pieces via the loop geometry, blocking is impossible. The King *must* move.

We will use these scenarios as our TDD checklist for the `Board` object.