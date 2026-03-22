# Test Logic

## [IC-010] Bishop Diagonal Geometry
**Test**: `test_bishop_moves`

**Description**:
Test that Bishops move along diagonals, changing both ring and slice.

**Pass Condition (Boolean Check)**:
Bishop moves diagonally to adjacent rings and slices.

<img src='assets/test_logic/test_bishop_moves.svg' width='600'>

## [IC-011] King Intersect Jump
**Test**: `test_king_moves`

**Description**:
Test King movement across the physical intersection (Slice 9 to 18).

**Pass Condition (Boolean Check)**:
King can jump directly from Slice 9 to Slice 18.

<img src='assets/test_logic/test_king_moves.svg' width='600'>

## [IC-012] Knight L-Shape Jumps
**Test**: `test_knight_moves`

**Description**:
Test Knight movement on the curved manifold.

**Pass Condition (Boolean Check)**:
Knight performs valid L-shaped jumps, including wrapping.

<img src='assets/test_logic/test_knight_moves.svg' width='600'>

## [IC-013] Pawn Forward Step
**Test**: `test_pawn_moves`

**Description**:
Test Pawn movement following the loop direction.

**Pass Condition (Boolean Check)**:
Pawn moves one step forward and wraps correctly.

<img src='assets/test_logic/test_pawn_moves.svg' width='600'>

## [IC-014] Rook Movement Geometry
**Test**: `test_rook_moves`

**Description**:
Test that Rooks move along rings and slices on an empty board.

**Pass Condition (Boolean Check)**:
Rook moves to adjacent rings and wraps around the same ring.

<img src='assets/test_logic/test_rook_moves.svg' width='600'>
