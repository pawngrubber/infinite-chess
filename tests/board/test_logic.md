# Logic Test Visuals (`test_logic.py`)

## Knight Moves wrapping around the loop
**Test**: `test_knight_moves`

**Description**:
A White Knight at **B2** can jump to various squares, including those that wrap around the figure-eight loop.
- **B2 -> C4, A4** (Standard L-shape)
- **B2 -> D3** (Standard L-shape)
- **B2 -> C18, A18** (Wrapping around Rank 1/18 boundary)

<img src="visuals/knight_moves.svg" width="800" alt="Knight Moves Visual">
