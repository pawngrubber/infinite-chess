# Advanced Feature & Failure Documentation

This document tracks the visual progress of complex features and 'known failures' that are being actively developed. It highlights the most ambitious aspects of the figure-eight chess engine.

## The Knight 'Wormhole' Jump
**Test**: `test_knight_true_lemniscate_jump`

**Scenario**:
A Knight is standing at the junction (Slice 9) and wants to jump to the other side of the intersection (Slice 18).

**Description**:
Because the tracks physically cross at the center, a square on one side of the intersection is actually very close to a square on the opposite side. An 'L' shape for a Knight should be able to bridge this physical gap, even if the coordinates (9 vs 18) look distant. This test validates this advanced 'topology-aware' movement.

**Pass Condition (Boolean Check)**:
The test verifies that the target square (C18) is present in the Knight's list of valid moves.
<img src='tdd_knight_jump.svg' width='600'>

## Checkmate Validation
**Test**: `test_is_checkmate`

**Scenario**:
A Black King at A1 is completely trapped. Every square it could move to is controlled by White Rooks, and it is currently under attack.

**Description**:
Checkmate occurs when you are in check and have zero legal ways to escape. This test sets up a 'cage' of Rooks and validates that the engine correctly identifies the end of the game.

**Pass Condition (Boolean Check)**:
The test confirms that 'is_checkmate' returns True for the Black side.
<img src='tdd_checkmate.svg' width='600'>
