# Test Board

## [IC-001] Around The World Check
**Test**: `test_around_the_world_check`

**Description**:
Test that a sliding piece (Rook) can attack the King from 'behind' by wrapping around the empty loop.

**Pass Condition (Boolean Check)**:
The Black King is reported as being 'In Check'.

<img src='assets/test_board_test_around_the_world_check.svg' width='600'>

## [IC-002] Self Intersection
**Test**: `test_self_intersection`

**Description**:
Test that a sliding piece does not count its own square as a move after a full lap.

**Pass Condition (Boolean Check)**:
No move end coordinate matches the start coordinate.

<img src='assets/test_board_test_self_intersection.svg' width='600'>

## [IC-003] Pin Slide
**Test**: `test_pin_slide`

**Description**:
Test that a Rook pinned along a ring CAN move along that same ring, but CANNOT step off it.

**Pass Condition (Boolean Check)**:
All legal moves for the Rook stay on Ring A.

<img src='assets/test_board_test_pin_slide.svg' width='600'>

## [IC-004] En Passant
**Test**: `test_en_passant`

**Description**:
Test en passant capture logic on a curved track.

**Pass Condition (Boolean Check)**:
A move exists with the 'is_en_passant' flag set to true.

<img src='assets/test_board_test_en_passant.svg' width='600'>

## [IC-005] King Teleportation Check
**Test**: `test_king_teleportation_check`

**Description**:
Test King intersection jump check legality at the crossing slices 9 and 18.

**Pass Condition (Boolean Check)**:
The King can capture an unprotected piece across the intersection.

<img src='assets/test_board_test_king_teleportation_check.svg' width='600'>
