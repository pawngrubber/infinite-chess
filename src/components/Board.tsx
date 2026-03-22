import React, { useState, useEffect } from 'react';

const InfiniteBoard = ({ data, socket }) => {
  const [board, setBoard] = useState(data.board);
  const [selected, setSelected] = useState(null);
  const [legalMoves, setLegalMoves] = useState([]);

  useEffect(() => {
    if (!socket) return;

    const handleMessage = (event) => {
      const msg = JSON.parse(event.data);
      if (msg.type === 'update') {
        setBoard(msg.board);
        setSelected(null);
        setLegalMoves([]);
      }
    };

    socket.addEventListener('message', handleMessage);
    return () => socket.removeEventListener('message', handleMessage);
  }, [socket]);

  const getPieceSymbol = (piece) => {
    const symbols = {
      WHITE: { PAWN: '♙', KNIGHT: '♘', BISHOP: '♗', ROOK: '♖', QUEEN: '♕', KING: '♔' },
      BLACK: { PAWN: '♟', KNIGHT: '♞', BISHOP: '♝', ROOK: '♜', QUEEN: '♛', KING: '♚' }
    };
    return symbols[piece.color][piece.type];
  };

  const handleTileClick = (ring, slice) => {
    const coordStr = `${ring}${slice}`;
    const piece = board.squares[coordStr];

    if (selected) {
      // Try to move
      socket.send(json.stringify({
        type: 'move',
        game_id: data.game_id,
        move: {
          start: selected.coord,
          end: { ring, slice }
        }
      }));
      setSelected(null);
    } else if (piece && piece.color === data.color) {
      setSelected({ coord: { ring, slice }, piece });
      // We could request legal moves from server here, but for now we'll just select
    }
  };

  // Helper to get SVG coordinates for a ring/slice
  const getPos = (ring, slice) => {
    const r_val = { A: 120, B: 140, C: 160, D: 180 }[ring];
    const angle = ((slice - 1) / 18) * 2 * Math.PI;
    
    // Lemniscate equation (parametric)
    // a * cos(t) / (1 + sin^2(t)), a * sin(t) * cos(t) / (1 + sin^2(t))
    const a = r_val * 2;
    const t = angle - Math.PI/2;
    const x = (a * Math.cos(t)) / (1 + Math.pow(Math.sin(t), 2));
    const y = (a * Math.sin(t) * Math.cos(t)) / (1 + Math.pow(Math.sin(t), 2));
    
    return { x: 400 + x, y: 200 + y };
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-zinc-900 text-white p-4">
      <div className="mb-4 text-xl font-mono">
        COLOR: <span className={data.color === 'WHITE' ? 'text-white' : 'text-zinc-500'}>{data.color}</span> | 
        TURN: <span className={board.turn === 'WHITE' ? 'text-white' : 'text-zinc-500'}>{board.turn}</span>
      </div>
      
      <div className="relative w-full max-w-4xl aspect-[2/1] bg-black rounded-xl overflow-hidden shadow-2xl border border-zinc-800">
        <svg viewBox="0 0 800 400" className="w-full h-full">
          {/* Render Tiles */}
          {['A', 'B', 'C', 'D'].map(ring => (
            Array.from({ length: 18 }, (_, i) => i + 1).map(slice => {
              const pos = getPos(ring, slice);
              const isSelected = selected && selected.coord.ring === ring && selected.coord.slice === slice;
              const piece = board.squares[`${ring}${slice}`];
              
              return (
                <g key={`${ring}${slice}`} onClick={() => handleTileClick(ring, slice)} className="cursor-pointer">
                  <circle 
                    cx={pos.x} cy={pos.y} r="15" 
                    fill={isSelected ? '#444' : '#111'} 
                    stroke="#333" strokeWidth="1"
                  />
                  {piece && (
                    <text 
                      x={pos.x} y={pos.y + 7} 
                      textAnchor="middle" 
                      fontSize="20" 
                      fill={piece.color === 'WHITE' ? 'white' : '#888'}
                      className="select-none pointer-events-none"
                    >
                      {getPieceSymbol(piece)}
                    </text>
                  )}
                </g>
              );
            })
          ))}
          
          {/* Crossing Intersection path */}
          <path
            d="M 400,200 C 600,0 800,200 600,400 C 400,200 200,0 0,200 C 200,400 400,200 Z"
            fill="none"
            stroke="#222"
            strokeWidth="2"
            opacity="0.3"
            pointerEvents="none"
          />
        </svg>
      </div>

      <div className="mt-8 text-zinc-400 max-w-lg text-center font-mono">
        {selected ? `Selected ${selected.piece.type} at ${selected.coord.ring}${selected.coord.slice}` : 'Select a piece to move'}
      </div>
    </div>
  );
};

export default InfiniteBoard;
