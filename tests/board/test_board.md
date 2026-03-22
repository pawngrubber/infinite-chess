# System-Level Test Documentation

This document visualizes high-level system behaviors like En Passant capture and loop-wide threat detection.

## En Passant Mechanics
**Test**: `test_en_passant`

**Scenario**:
A Black Pawn has just jumped two squares forward, passing through the square B5. A White Pawn is standing next to it at A4.

**Description**:
'En Passant' (In Passing) allows the White Pawn to capture the Black Pawn as it passes by. The White Pawn moves diagonally to the empty square (B5) that the Black Pawn skipped over, and the Black Pawn is removed from the board. This test validates that the 'target' square is correctly identified and the capture is handled properly.

**Pass Condition (Boolean Check)**:
The test looks through all available moves for the White Pawn and confirms that a move exists with the 'is_en_passant' flag set to true, pointing to the correct destination.
<img src='board_en_passant.svg' width='600'>

## Around the World Check
**Test**: `test_around_the_world_check`

**Scenario**:
A White Rook at A3 is attacking a Black King at A1. 

**Description**:
Because the board is a continuous loop, the Rook is attacking the King from two directions at once! It has a direct path (A3 -> A2 -> A1) and a very long path wrapping around the entire loop (A3 -> A4 -> A5 ... -> A18 -> A1). This test ensures that the check is detected correctly, recognizing that distance doesn't matter if the path is clear.

**Pass Condition (Boolean Check)**:
The test simply confirms that the Black King is reported as being 'In Check'.
<img src='board_around_world.svg' width='600'>
