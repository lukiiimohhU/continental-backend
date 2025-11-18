# Guía de Implementación Frontend - Controles del Host

Este documento describe cómo implementar las nuevas funcionalidades de control del host en el frontend.

## Tabla de Contenidos

1. [Transferencia de Host](#1-transferencia-de-host)
2. [Menú de Controles del Host](#2-menú-de-controles-del-host)
3. [Finalizar Ronda](#3-finalizar-ronda)
4. [Finalizar Partida](#4-finalizar-partida)
5. [Saltar a Ronda](#5-saltar-a-ronda)
6. [Cambiar Puntos de Jugador](#6-cambiar-puntos-de-jugador)
7. [Eventos WebSocket](#7-eventos-websocket)

---

## 1. Transferencia de Host

### Backend Behavior
Cuando el host abandona la partida, el sistema automáticamente:
- Selecciona un jugador aleatorio de los restantes
- Le asigna el rol de host
- Envía un broadcast a todos los jugadores

### Frontend Changes Requeridos

#### 1.1 Manejar Evento de Transferencia

```tsx
// Ejemplo: useWebSocket.ts

useEffect(() => {
  if (!ws) return;

  const handleMessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data);

    switch (data.type) {
      case 'host_transferred':
        // Actualizar estado local
        setHostId(data.new_host_id);

        // Mostrar notificación
        toast.info(data.message); // "NombreJugador es ahora el anfitrión"

        // Si eres tú el nuevo host, mostrar mensaje especial
        if (data.new_host_id === currentPlayerId) {
          toast.success('¡Ahora eres el anfitrión!');
        }
        break;

      // ... otros casos
    }
  };

  ws.addEventListener('message', handleMessage);
  return () => ws.removeEventListener('message', handleMessage);
}, [ws]);
```

#### 1.2 Actualizar UI según Rol de Host

```tsx
// Ejemplo: GameBoard.tsx

const GameBoard = ({ playerId, players }) => {
  const isHost = players.find(p => p.id === playerId)?.is_host || false;

  return (
    <div className="game-board">
      <header>
        {isHost && <HostBadge />}
        <GameMenu isHost={isHost} onLeaveGame={handleLeaveGame} />
      </header>
      {/* ... */}
    </div>
  );
};
```

---

## 2. Menú de Controles del Host

### Estructura del Menú

El menú hamburguesa ahora debe tener **dos versiones**:

1. **Versión Normal (No Host):** Solo "Abandonar Partida"
2. **Versión Host:** Todos los controles de host + "Abandonar Partida"

### 2.1 Componente del Menú Actualizado

```tsx
// Ejemplo: GameMenu.tsx

import { useState } from 'react';
import { Menu, X, Flag, Zap, SkipForward, Edit3 } from 'lucide-react';

interface GameMenuProps {
  isHost: boolean;
  onLeaveGame: () => void;
  onEndRound: (countPoints: boolean) => void;
  onEndGame: (countPoints: boolean) => void;
  onJumpToRound: (round: number, countPoints: boolean) => void;
  onChangePlayerScore: (playerId: string, newScore: number) => void;
  players: Array<{ id: string; name: string; score: number }>;
}

const GameMenu = ({
  isHost,
  onLeaveGame,
  onEndRound,
  onEndGame,
  onJumpToRound,
  onChangePlayerScore,
  players
}: GameMenuProps) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [activeSubmenu, setActiveSubmenu] = useState<string | null>(null);

  return (
    <div className="game-menu-container">
      {/* Botón hamburguesa */}
      <button
        className="menu-toggle-btn"
        onClick={() => setIsMenuOpen(true)}
        aria-label="Abrir menú"
      >
        <Menu size={24} />
      </button>

      {/* Modal del menú */}
      {isMenuOpen && (
        <div className="menu-overlay" onClick={() => setIsMenuOpen(false)}>
          <div className="menu-panel" onClick={(e) => e.stopPropagation()}>
            {/* Botón cerrar */}
            <button
              className="menu-close-btn"
              onClick={() => setIsMenuOpen(false)}
            >
              <X size={20} />
            </button>

            <div className="menu-content">
              <h3>{isHost ? 'Panel de Control' : 'Menú'}</h3>

              {/* Controles del Host */}
              {isHost && (
                <div className="host-controls">
                  <h4>Controles del Anfitrión</h4>

                  {/* Finalizar Ronda */}
                  <EndRoundControl
                    onEndRound={onEndRound}
                    activeSubmenu={activeSubmenu}
                    setActiveSubmenu={setActiveSubmenu}
                  />

                  {/* Finalizar Partida */}
                  <EndGameControl
                    onEndGame={onEndGame}
                    activeSubmenu={activeSubmenu}
                    setActiveSubmenu={setActiveSubmenu}
                  />

                  {/* Saltar a Ronda */}
                  <JumpToRoundControl
                    onJumpToRound={onJumpToRound}
                    activeSubmenu={activeSubmenu}
                    setActiveSubmenu={setActiveSubmenu}
                  />

                  {/* Cambiar Puntos */}
                  <ChangeScoreControl
                    players={players}
                    onChangePlayerScore={onChangePlayerScore}
                    activeSubmenu={activeSubmenu}
                    setActiveSubmenu={setActiveSubmenu}
                  />
                </div>
              )}

              {/* Abandonar Partida (todos) */}
              <div className="menu-divider" />
              <button
                className="leave-game-btn"
                onClick={() => {
                  if (confirm('¿Estás seguro de que quieres abandonar?')) {
                    onLeaveGame();
                    setIsMenuOpen(false);
                  }
                }}
              >
                Abandonar Partida
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default GameMenu;
```

---

## 3. Finalizar Ronda

### 3.1 Componente EndRoundControl

```tsx
// Ejemplo: EndRoundControl.tsx

const EndRoundControl = ({ onEndRound, activeSubmenu, setActiveSubmenu }) => {
  const isOpen = activeSubmenu === 'end-round';

  return (
    <div className="control-group">
      <button
        className="control-btn"
        onClick={() => setActiveSubmenu(isOpen ? null : 'end-round')}
      >
        <Flag size={18} />
        Finalizar Ronda
        <span className={`arrow ${isOpen ? 'open' : ''}`}>▼</span>
      </button>

      {isOpen && (
        <div className="submenu">
          <button
            className="submenu-btn"
            onClick={() => {
              if (confirm('¿Finalizar ronda y contar puntos?')) {
                onEndRound(true);
                setActiveSubmenu(null);
              }
            }}
          >
            Contar Puntos
          </button>
          <button
            className="submenu-btn"
            onClick={() => {
              if (confirm('¿Finalizar ronda sin contar puntos (0 puntos para todos)?')) {
                onEndRound(false);
                setActiveSubmenu(null);
              }
            }}
          >
            Sin Contar Puntos (0 pts)
          </button>
        </div>
      )}
    </div>
  );
};
```

### 3.2 Función WebSocket

```tsx
// Ejemplo: useGameActions.ts

const endRound = (countPoints: boolean) => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      action: 'host_end_round',
      count_points: countPoints
    }));
  }
};
```

---

## 4. Finalizar Partida

### 4.1 Componente EndGameControl

```tsx
// Ejemplo: EndGameControl.tsx

const EndGameControl = ({ onEndGame, activeSubmenu, setActiveSubmenu }) => {
  const isOpen = activeSubmenu === 'end-game';

  return (
    <div className="control-group">
      <button
        className="control-btn danger"
        onClick={() => setActiveSubmenu(isOpen ? null : 'end-game')}
      >
        <Zap size={18} />
        Finalizar Partida
        <span className={`arrow ${isOpen ? 'open' : ''}`}>▼</span>
      </button>

      {isOpen && (
        <div className="submenu">
          <button
            className="submenu-btn"
            onClick={() => {
              if (confirm('¿Finalizar partida y contar puntos?')) {
                onEndGame(true);
                setActiveSubmenu(null);
              }
            }}
          >
            Contar Puntos
          </button>
          <button
            className="submenu-btn"
            onClick={() => {
              if (confirm('¿Finalizar partida sin contar puntos (0 puntos para todos)?')) {
                onEndGame(false);
                setActiveSubmenu(null);
              }
            }}
          >
            Sin Contar Puntos (0 pts)
          </button>
        </div>
      )}
    </div>
  );
};
```

### 4.2 Función WebSocket

```tsx
const endGame = (countPoints: boolean) => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      action: 'host_end_game',
      count_points: countPoints
    }));
  }
};
```

---

## 5. Saltar a Ronda

### 5.1 Componente JumpToRoundControl

```tsx
// Ejemplo: JumpToRoundControl.tsx

const JumpToRoundControl = ({ onJumpToRound, activeSubmenu, setActiveSubmenu }) => {
  const isOpen = activeSubmenu === 'jump-round';
  const [selectedRound, setSelectedRound] = useState<number | null>(null);

  const roundNames = {
    1: "Ronda 1: 2 Tríos",
    2: "Ronda 2: 1 Trío + 1 Escalera",
    3: "Ronda 3: 2 Escaleras",
    4: "Ronda 4: 3 Tríos",
    5: "Ronda 5: 2 Tríos + 1 Escalera",
    6: "Ronda 6: 1 Trío + 2 Escaleras",
    7: "Ronda 7: 3 Escaleras"
  };

  return (
    <div className="control-group">
      <button
        className="control-btn"
        onClick={() => setActiveSubmenu(isOpen ? null : 'jump-round')}
      >
        <SkipForward size={18} />
        Saltar a Ronda
        <span className={`arrow ${isOpen ? 'open' : ''}`}>▼</span>
      </button>

      {isOpen && (
        <div className="submenu">
          {!selectedRound ? (
            // Mostrar lista de rondas
            <div className="round-list">
              {[1, 2, 3, 4, 5, 6, 7].map(round => (
                <button
                  key={round}
                  className="round-btn"
                  onClick={() => setSelectedRound(round)}
                >
                  {roundNames[round]}
                </button>
              ))}
            </div>
          ) : (
            // Mostrar opciones de contar puntos
            <div className="points-options">
              <p className="selected-round">
                {roundNames[selectedRound]}
              </p>
              <button
                className="submenu-btn"
                onClick={() => {
                  if (confirm(`¿Saltar a ronda ${selectedRound} contando puntos?`)) {
                    onJumpToRound(selectedRound, true);
                    setSelectedRound(null);
                    setActiveSubmenu(null);
                  }
                }}
              >
                Contar Puntos
              </button>
              <button
                className="submenu-btn"
                onClick={() => {
                  if (confirm(`¿Saltar a ronda ${selectedRound} sin contar puntos?`)) {
                    onJumpToRound(selectedRound, false);
                    setSelectedRound(null);
                    setActiveSubmenu(null);
                  }
                }}
              >
                Sin Contar Puntos (0 pts)
              </button>
              <button
                className="back-btn"
                onClick={() => setSelectedRound(null)}
              >
                ← Volver
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
```

### 5.2 Función WebSocket

```tsx
const jumpToRound = (targetRound: number, countPoints: boolean) => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      action: 'host_jump_to_round',
      target_round: targetRound,
      count_points: countPoints
    }));
  }
};
```

---

## 6. Cambiar Puntos de Jugador

### 6.1 Componente ChangeScoreControl

```tsx
// Ejemplo: ChangeScoreControl.tsx

const ChangeScoreControl = ({
  players,
  onChangePlayerScore,
  activeSubmenu,
  setActiveSubmenu
}) => {
  const isOpen = activeSubmenu === 'change-score';
  const [selectedPlayerId, setSelectedPlayerId] = useState<string | null>(null);
  const [newScore, setNewScore] = useState<string>('');

  const handleSubmit = () => {
    if (!selectedPlayerId || newScore === '') return;

    const score = parseInt(newScore, 10);
    if (isNaN(score) || score < 0) {
      alert('Por favor introduce un número válido (0 o mayor)');
      return;
    }

    const player = players.find(p => p.id === selectedPlayerId);
    if (confirm(`¿Cambiar puntos de ${player?.name} a ${score}?`)) {
      onChangePlayerScore(selectedPlayerId, score);
      setSelectedPlayerId(null);
      setNewScore('');
      setActiveSubmenu(null);
    }
  };

  return (
    <div className="control-group">
      <button
        className="control-btn"
        onClick={() => setActiveSubmenu(isOpen ? null : 'change-score')}
      >
        <Edit3 size={18} />
        Cambiar Puntos
        <span className={`arrow ${isOpen ? 'open' : ''}`}>▼</span>
      </button>

      {isOpen && (
        <div className="submenu">
          <div className="score-editor">
            {/* Seleccionar jugador */}
            <label>Jugador:</label>
            <select
              value={selectedPlayerId || ''}
              onChange={(e) => {
                setSelectedPlayerId(e.target.value);
                const player = players.find(p => p.id === e.target.value);
                if (player) {
                  setNewScore(player.score.toString());
                }
              }}
            >
              <option value="">Selecciona un jugador</option>
              {players.map(player => (
                <option key={player.id} value={player.id}>
                  {player.name} ({player.score} pts)
                </option>
              ))}
            </select>

            {/* Editar puntos */}
            {selectedPlayerId && (
              <>
                <label>Nuevos Puntos:</label>
                <input
                  type="number"
                  min="0"
                  value={newScore}
                  onChange={(e) => setNewScore(e.target.value)}
                  placeholder="0"
                />
                <button
                  className="submit-btn"
                  onClick={handleSubmit}
                >
                  Guardar
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
```

### 6.2 Función WebSocket

```tsx
const changePlayerScore = (targetPlayerId: string, newScore: number) => {
  if (ws && ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({
      action: 'host_change_player_score',
      target_player_id: targetPlayerId,
      new_score: newScore
    }));
  }
};
```

---

## 7. Eventos WebSocket

### Eventos que el Frontend debe ENVIAR

```typescript
// 1. Finalizar ronda
{
  action: 'host_end_round',
  count_points: boolean  // true = contar puntos, false = 0 puntos para todos
}

// 2. Finalizar partida
{
  action: 'host_end_game',
  count_points: boolean
}

// 3. Saltar a ronda
{
  action: 'host_jump_to_round',
  target_round: number,  // 1-7
  count_points: boolean
}

// 4. Cambiar puntos de jugador
{
  action: 'host_change_player_score',
  target_player_id: string,
  new_score: number  // >= 0
}
```

### Eventos que el Frontend debe ESCUCHAR

```typescript
// 1. Transferencia de host
{
  type: 'host_transferred',
  new_host_id: string,
  new_host_name: string,
  message: string  // "NombreJugador es ahora el anfitrión"
}

// 2. Notificación (para todas las acciones del host)
{
  type: 'notification',
  message: string
  // Ejemplos:
  // - "El anfitrión ha finalizado la ronda contando puntos"
  // - "El anfitrión ha finalizado la partida sin contar puntos"
  // - "El anfitrión saltó a la ronda 3 contando puntos"
  // - "El anfitrión cambió los puntos de Juan de 50 a 100"
}

// 3. Estado del juego actualizado (se envía después de cada acción)
{
  type: 'game_state',
  round: number,
  round_ended: boolean,
  game_over: boolean,
  players: Array<{
    id: string,
    name: string,
    score: number,
    is_host: boolean,  // ¡Importante! Verificar quién es el host
    // ...
  }>,
  // ... resto del estado
}
```

---

## 8. Estilos CSS Recomendados

```css
/* styles/HostControls.css */

/* Panel de control del host */
.host-controls {
  margin-bottom: 16px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.host-controls h4 {
  font-size: 14px;
  font-weight: 600;
  color: #6b7280;
  margin-bottom: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Grupos de controles */
.control-group {
  margin-bottom: 8px;
}

.control-btn {
  width: 100%;
  padding: 10px 12px;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  gap: 8px;
  position: relative;
}

.control-btn:hover {
  background-color: #e5e7eb;
}

.control-btn.danger {
  background-color: #fef2f2;
  border-color: #fecaca;
  color: #dc2626;
}

.control-btn.danger:hover {
  background-color: #fee2e2;
}

.control-btn .arrow {
  margin-left: auto;
  transition: transform 0.2s;
}

.control-btn .arrow.open {
  transform: rotate(180deg);
}

/* Submenús */
.submenu {
  margin-top: 8px;
  padding: 8px;
  background-color: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.submenu-btn {
  width: 100%;
  padding: 8px 12px;
  margin-bottom: 4px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.submenu-btn:last-child {
  margin-bottom: 0;
}

.submenu-btn:hover {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

/* Lista de rondas */
.round-list {
  max-height: 300px;
  overflow-y: auto;
}

.round-btn {
  width: 100%;
  padding: 10px 12px;
  margin-bottom: 6px;
  background-color: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 4px;
  font-size: 13px;
  text-align: left;
  cursor: pointer;
  transition: all 0.2s;
}

.round-btn:hover {
  background-color: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

/* Opciones de puntos */
.points-options {
  padding: 4px;
}

.selected-round {
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 12px;
  padding: 8px;
  background-color: #eff6ff;
  border-left: 3px solid #3b82f6;
  border-radius: 4px;
}

.back-btn {
  width: 100%;
  padding: 8px 12px;
  margin-top: 8px;
  background-color: #f3f4f6;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.back-btn:hover {
  background-color: #e5e7eb;
}

/* Editor de puntos */
.score-editor {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.score-editor label {
  font-size: 12px;
  font-weight: 600;
  color: #374151;
}

.score-editor select,
.score-editor input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  font-size: 14px;
}

.score-editor select:focus,
.score-editor input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.submit-btn {
  padding: 10px 16px;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:hover {
  background-color: #059669;
}

/* Divider */
.menu-divider {
  height: 1px;
  background-color: #e5e7eb;
  margin: 16px 0;
}

/* Badge de host */
.host-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  background-color: #fef3c7;
  border: 1px solid #fbbf24;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  color: #92400e;
}
```

---

## 9. Ejemplo de Integración Completa

```tsx
// Ejemplo: GameBoard.tsx

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'react-hot-toast';
import GameMenu from './GameMenu';

const GameBoard = () => {
  const router = useRouter();
  const { roomCode, playerId } = router.query;
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [gameState, setGameState] = useState(null);
  const [players, setPlayers] = useState([]);
  const [isHost, setIsHost] = useState(false);

  // Conectar WebSocket
  useEffect(() => {
    if (!roomCode || !playerId) return;

    const websocket = new WebSocket(
      `${WS_URL}/api/ws/${roomCode}/${playerId}`
    );

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      switch (data.type) {
        case 'game_state':
          setGameState(data);
          setPlayers(data.players);
          // Actualizar si eres host
          const currentPlayer = data.players.find(p => p.id === playerId);
          setIsHost(currentPlayer?.is_host || false);
          break;

        case 'host_transferred':
          toast.info(data.message);
          if (data.new_host_id === playerId) {
            toast.success('¡Ahora eres el anfitrión!');
          }
          break;

        case 'notification':
          toast.info(data.message);
          break;

        // ... otros eventos
      }
    };

    setWs(websocket);
    return () => websocket.close();
  }, [roomCode, playerId]);

  // Funciones de control del host
  const handleEndRound = (countPoints: boolean) => {
    ws?.send(JSON.stringify({
      action: 'host_end_round',
      count_points: countPoints
    }));
  };

  const handleEndGame = (countPoints: boolean) => {
    ws?.send(JSON.stringify({
      action: 'host_end_game',
      count_points: countPoints
    }));
  };

  const handleJumpToRound = (targetRound: number, countPoints: boolean) => {
    ws?.send(JSON.stringify({
      action: 'host_jump_to_round',
      target_round: targetRound,
      count_points: countPoints
    }));
  };

  const handleChangePlayerScore = (targetPlayerId: string, newScore: number) => {
    ws?.send(JSON.stringify({
      action: 'host_change_player_score',
      target_player_id: targetPlayerId,
      new_score: newScore
    }));
  };

  const handleLeaveGame = () => {
    ws?.send(JSON.stringify({ action: 'leave_game' }));
    ws?.close();
    router.push('/');
  };

  return (
    <div className="game-board">
      <header className="game-header">
        <div className="room-info">
          {isHost && (
            <div className="host-badge">
              👑 Anfitrión
            </div>
          )}
          <span>Sala: {roomCode}</span>
          <span>Ronda: {gameState?.round || 1}</span>
        </div>

        {/* Menú con controles del host */}
        <GameMenu
          isHost={isHost}
          onLeaveGame={handleLeaveGame}
          onEndRound={handleEndRound}
          onEndGame={handleEndGame}
          onJumpToRound={handleJumpToRound}
          onChangePlayerScore={handleChangePlayerScore}
          players={players}
        />
      </header>

      {/* Resto del tablero */}
      {/* ... */}
    </div>
  );
};

export default GameBoard;
```

---

## 10. Testing Checklist

### Transferencia de Host
- [ ] Cuando el host abandona, se selecciona nuevo host aleatorio
- [ ] El nuevo host recibe notificación especial
- [ ] Otros jugadores ven quién es el nuevo host
- [ ] El menú se actualiza correctamente para el nuevo host
- [ ] El badge de host aparece/desaparece correctamente

### Finalizar Ronda
- [ ] Solo el host puede acceder a esta opción
- [ ] Opción "Contar Puntos" suma puntos correctamente
- [ ] Opción "Sin Contar Puntos" suma 0 puntos
- [ ] La ronda termina y se muestra RoundEndScreen
- [ ] Todos los jugadores ven la misma pantalla

### Finalizar Partida
- [ ] Solo el host puede acceder a esta opción
- [ ] Opción "Contar Puntos" suma puntos correctamente
- [ ] Opción "Sin Contar Puntos" suma 0 puntos
- [ ] El juego marca como terminado (game_over: true)
- [ ] Se muestra la pantalla final correctamente

### Saltar a Ronda
- [ ] Solo el host puede acceder a esta opción
- [ ] Se muestran las 7 rondas disponibles
- [ ] Al seleccionar ronda, aparecen las 2 opciones de puntos
- [ ] Saltar cuenta/no cuenta puntos según selección
- [ ] La nueva ronda comienza correctamente
- [ ] Las cartas se reparten según el objetivo de la ronda

### Cambiar Puntos
- [ ] Solo el host puede acceder a esta opción
- [ ] Se muestran todos los jugadores con sus puntos actuales
- [ ] Se puede editar el valor de puntos
- [ ] No permite valores negativos
- [ ] Los puntos se actualizan para todos los jugadores
- [ ] Se muestra notificación del cambio

---

## 11. Notas Importantes

1. **Seguridad:**
   - Todas las acciones verifican que el jugador sea host en el backend
   - No es posible ejecutar comandos de host si no lo eres
   - Los mensajes de error se envían solo al jugador que intentó la acción

2. **UX:**
   - Siempre pedir confirmación antes de acciones importantes
   - Mostrar mensajes claros de lo que va a suceder
   - Diferenciar visualmente las opciones destructivas (finalizar partida)

3. **Sincronización:**
   - El backend siempre envía `game_state` actualizado después de cada acción
   - Confía en el estado del servidor, no en el estado local
   - Actualiza la UI basándote en `game_state.players[].is_host`

4. **Responsiveness:**
   - El menú debe funcionar bien en móviles
   - Los submenús deben ser scrollables si son muy largos
   - Botones suficientemente grandes para touch

---

## 12. Soporte

**Eventos WebSocket disponibles:**
- `host_transferred` - Nuevo host asignado
- `notification` - Mensajes informativos de acciones
- `game_state` - Estado actualizado del juego
- `error` - Errores específicos

**Acciones WebSocket disponibles:**
- `host_end_round` - Finalizar ronda
- `host_end_game` - Finalizar partida
- `host_jump_to_round` - Saltar a ronda específica
- `host_change_player_score` - Cambiar puntos de jugador

---

**Fecha de actualización:** 2025-01-18
**Versión del Backend:** 1.2.0
