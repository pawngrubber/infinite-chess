from dataclasses import dataclass
from typing import Callable, Optional
from .board import Board

@dataclass
class Scenario:
    """Metadata for a chess test scenario used for documentation generation."""
    id: str
    name: str
    description: str
    pass_condition: str

def scenario(id: str, name: str, description: str, pass_condition: str):
    """Decorator to attach scenario metadata to a test function."""
    def decorator(func: Callable):
        func._scenario = Scenario(
            id=id,
            name=name,
            description=description,
            pass_condition=pass_condition
        )
        return func
    return decorator

# Global state to capture the board from the last executed test
_ACTIVE_BOARD: Optional[Board] = None

def capture_board(board: Board):
    """Explicitly capture a board state for documentation."""
    global _ACTIVE_BOARD
    _ACTIVE_BOARD = board

def get_captured_board() -> Optional[Board]:
    """Retrieve the last captured board state."""
    return _ACTIVE_BOARD
