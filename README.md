# Infinite Chess

A chess variant played on a lemniscate (figure-eight) board, where pieces can orbit the loops.

## Features
- **Modern Tech Stack**: React (TypeScript) + Django Channels.
- **Anonymous Matchmaking**: Real-time pairing without user accounts.
- **Infinite Topology**: A board where straight lines can return to their origin.

## Development

### Backend
1. Install [uv](https://github.com/astral-sh/uv).
2. `cd apps/backend`
3. `uv sync`
4. `uv run python manage.py runserver`

### Frontend
1. `cd apps/frontend`
2. `npm install`
3. `npm run dev`

## Architecture
- Matchmaking is handled in-memory by Django Channels.
- Game state is synchronized via WebSockets.
- Board is rendered as a responsive SVG path for non-Euclidean movement.
