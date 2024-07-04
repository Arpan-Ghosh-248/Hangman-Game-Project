import React, { useState } from 'react';
import axios from 'axios';
import './App.css'

function HangmanGame() {
  const [gameId, setGameId] = useState(null);
  const [gameState, setGameState] = useState(null);
  const [guess, setGuess] = useState('');
  const [message, setMessage] = useState('');

  const getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  };

  const startNewGame = () => {
    axios.post('http://localhost:8000/game/new/')
      .then(response => {
        console.log(response.data)
        setGameId(response.data.id);
        setGameState({ state: 'InProgress' });
        setMessage('');
      })
      .catch(error => {
        console.error('Error starting new game:', error);
        setMessage('Error starting new game. Please try again.');
      });
  };

  const handleGuess = () => {
    axios.post(`http://localhost:8000/game/${gameId}/guess/`, {
        character: guess.toLowerCase(),
      }, {
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': getCookie('csrftoken'),
        }
      })
      .then(response => {
        setGameState(response.data);
        setGuess('');
        if (response.data.state === 'Won') {
          setMessage('Congratulations! You won!');
        } else if (response.data.state === 'Lost') {
          setMessage('Game Over! You lost.');
        } else {
          setMessage('');
        }
      })
      .catch(error => {
        console.error('Error making guess:', error);
        setMessage('Error making guess. Please try again.');
      });
  };

  const handleChange = (event) => {
    setGuess(event.target.value.slice(0, 1));
  };

  return (
    <div className="HangmanGame">
      <h1>Hangman Game</h1>
      {!gameId && (
        <button onClick={startNewGame}>Start New Game</button>
      )}
      {gameId && (
        <div>
          <p>Game ID: {gameId}</p>
          {message && <p>{message}</p>}
          {gameState && (
            <div>
              <p>Game State: {gameState.state}</p>
              <p>Word State: {gameState.word_state}</p>
              <p>Incorrect Guesses: {gameState.incorrect_guesses}</p>
              <p>Remaining Incorrect Guesses: {gameState.remaining_incorrect_guesses}</p>
              {gameState.state === 'InProgress' && (
                <div>
                  <input 
                    type="text" 
                    value={guess} 
                    onChange={handleChange} 
                    maxLength="1"
                  />
                  <button onClick={handleGuess}>Make Guess</button>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default HangmanGame;
