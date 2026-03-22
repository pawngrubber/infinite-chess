# Board System Test Documentation

Visualizing system-level board state and move legality.

## Around the World Check
**Test**: `test_around_the_world_check`

A sliding piece can attack a king by wrapping all the way around the track. This validates that logic doesn't just look at local distance.

<img src='board_around_world.svg' width='600'>

## Pin Slide
**Test**: `test_pin_slide`

Validates that a pinned piece can still move as long as it stays on the line of the pin. The White Rook can move between A2 and A4 without breaking the pin.

<img src='board_pin_slide.svg' width='600'>

## En Passant Mechanics
**Test**: `test_en_passant`

Validates the capture of a pawn that has just double-moved. The capturing pawn moves to the 'skipped' square.

<img src='board_en_passant.svg' width='600'>
