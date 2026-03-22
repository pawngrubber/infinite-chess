# Infinite Chess

An authoritative Infinite Chess matchmaking service with a non-Euclidean lemniscate (figure-eight) board.

## Architecture: Flat Source Monorepo

This project follows a "Flat Source" monorepo structure where the core logic, backend server, and frontend UI live together in a single, unified environment.

```text
infinite-chess/
├── pyproject.toml         # Unified Python dependencies (Logic + Server)
├── package.json           # Unified Node dependencies (React + Vite)
├── src/                   # Universal Source Code
│   ├── board/             # [BACKEND] Pure Python Chess logic (The "Rules")
│   ├── server/            # [BACKEND] Django / Channels (The "Network")
│   └── frontend/          # [FRONTEND] React / Vite (The "UI")
├── tests/                 # Parallel Testing Suite
│   ├── board/             # Unit tests for the chess engine
│   └── server/            # Integration tests for the Django server
└── assets/                # Reference material and game assets
```

## Getting Started

### Prerequisites
- [uv](https://github.com/astral-sh/uv) for Python management.
- [Node.js](https://nodejs.org/) (npm) for frontend management.

### Backend Setup (Server & Logic)
Install dependencies and sync the environment:
```bash
uv sync
```

Run the development server:
```bash
# PYTHONPATH=src is automatically handled by the library install
uv run manage runserver
```

### Frontend Setup (UI)
Install dependencies:
```bash
npm install
```

Start the Vite development server:
```bash
npm run dev
```

### Testing
Run all Python tests (Logic + Server):
```bash
uv run pytest
```

Run only the chess logic tests:
```bash
uv run pytest tests/board/
```

## Game Rules
- **The Board**: A 72-tile lemniscate board with 4 rings (A-D) and 18 slices.
- **Topology**: Slice 9 and Slice 18 physically intersect, allowing the King to "step across" the center.
- **Pawns**: 10-step promotion to Queen.
- **Bishops**: Restricted to their color complex (Red/Yellow or Green/Blue).
- **Mandatory En Passant**: If a capture is possible via En Passant, it must be taken.
- **No Castling**: Traditional castling is not supported in this topology.
