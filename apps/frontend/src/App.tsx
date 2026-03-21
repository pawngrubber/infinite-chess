import React, { useState, useEffect } from 'react';
import InfiniteBoard from './components/Board';

function App() {
  const [status, setStatus] = useState('searching');
  const [gameData, setGameData] = useState(null);

  useEffect(() => {
    // Basic WebSocket connection for matchmaking
    const socket = new WebSocket('ws://localhost:8000/ws/matchmaking/');

    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'matched') {
        setStatus('playing');
        setGameData(data);
      }
    };

    return () => socket.close();
  }, []);

  if (status === 'searching') {
    return (
      <div className="flex items-center justify-center min-h-screen bg-black text-white">
        <div className="animate-pulse text-2xl font-mono">SEARCHING FOR OPPONENT...</div>
      </div>
    );
  }

  return <InfiniteBoard data={gameData} />;
}

export default App;
