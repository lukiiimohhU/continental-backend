# Guía de Implementación Frontend - Nuevas Funcionalidades

Este documento describe los cambios necesarios en el frontend para implementar las nuevas funcionalidades del backend.

## Tabla de Contenidos

1. [Cambios en Código de Sala](#1-cambios-en-código-de-sala)
2. [Incremento de Jokers por Mazo](#2-incremento-de-jokers-por-mazo)
3. [Funcionalidad de Abandonar Partida](#3-funcionalidad-de-abandonar-partida)
4. [Unirse a Partida en RoundEndScreen](#4-unirse-a-partida-en-roundendscreen)

---

## 1. Cambios en Código de Sala

### Backend Changes
- **Antes:** Código de 6 caracteres alfanuméricos (ej: `A3B5C7`)
- **Ahora:** Código de 3 dígitos numéricos (ej: `123`, `456`, `999`)

### Frontend Changes Requeridos

#### 1.1 Input de Código de Sala

**Ubicación:** Componente de unirse a sala / HomePage

```tsx
// Ejemplo: JoinRoomInput.tsx o HomePage.tsx

// ANTES
<input
  type="text"
  maxLength={6}
  pattern="[A-Z0-9]{6}"
  placeholder="Código (ej: ABC123)"
/>

// AHORA
<input
  type="text"
  inputMode="numeric"
  maxLength={3}
  pattern="[0-9]{3}"
  placeholder="Código (ej: 123)"
  onChange={(e) => {
    // Solo permitir números
    const value = e.target.value.replace(/[^0-9]/g, '');
    setRoomCode(value);
  }}
/>
```

#### 1.2 Validación del Código

```tsx
// Función de validación actualizada
const validateRoomCode = (code: string): boolean => {
  // ANTES: return /^[A-Z0-9]{6}$/.test(code);
  // AHORA:
  return /^[0-9]{3}$/.test(code);
};
```

#### 1.3 Mostrar Código en UI

```tsx
// Ejemplo: RoomHeader.tsx o GameBoard.tsx
const RoomCodeDisplay = ({ code }: { code: string }) => (
  <div className="room-code">
    <span>Código de Sala:</span>
    <strong>{code}</strong> {/* Ahora muestra 3 dígitos en lugar de 6 caracteres */}
  </div>
);
```

---

## 2. Incremento de Jokers por Mazo

### Backend Changes
- **Antes:** 2 Jokers por mazo
- **Ahora:** 3 Jokers por mazo
- **Total con 2 mazos:** De 4 Jokers → 6 Jokers

### Frontend Changes Requeridos

#### 2.1 Actualizar Documentación/Tooltips

```tsx
// Ejemplo: GameRules.tsx o InfoTooltip.tsx
const JokerInfo = () => (
  <div className="joker-info">
    <p>Cada mazo contiene <strong>3 Jokers</strong></p>
    <p>Total en el juego: <strong>6 Jokers</strong> (2 mazos × 3 Jokers)</p>
  </div>
);
```

**Nota:** No se requieren cambios en la lógica del juego ya que el backend maneja completamente la creación y distribución de cartas.

---

## 3. Funcionalidad de Abandonar Partida

### Backend Implementation
El backend provee:
- **Acción WebSocket:** `leave_game`
- **Broadcast Event:** `player_left`
- **Actualización automática** del estado del juego

### Frontend Changes Requeridos

#### 3.1 UI del Menú Hamburguesa

**Ubicación:** Componente del tablero de juego (junto al "Objetivo de la ronda")

```tsx
// Ejemplo: GameBoard.tsx
import { useState } from 'react';
import { Menu, X } from 'lucide-react'; // O tu librería de iconos

const GameMenu = ({ onLeaveGame }: { onLeaveGame: () => void }) => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <div className="game-menu-container">
      {/* Botón del menú hamburguesa */}
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
            {/* Botón de cerrar (X) */}
            <button
              className="menu-close-btn"
              onClick={() => setIsMenuOpen(false)}
              aria-label="Cerrar menú"
            >
              <X size={20} />
            </button>

            {/* Contenido del menú */}
            <div className="menu-content">
              <h3>Menú</h3>
              <button
                className="leave-game-btn"
                onClick={() => {
                  if (confirm('¿Estás seguro de que quieres abandonar la partida?')) {
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
```

#### 3.2 Estilos CSS Recomendados

```css
/* styles/GameMenu.css */

.game-menu-container {
  position: relative;
}

.menu-toggle-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.menu-toggle-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.menu-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.menu-panel {
  background: white;
  border-radius: 12px;
  padding: 24px;
  min-width: 300px;
  max-width: 400px;
  position: relative;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.menu-close-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.menu-close-btn:hover {
  background-color: rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.menu-content {
  margin-top: 20px;
}

.menu-content h3 {
  margin-bottom: 16px;
  font-size: 18px;
  font-weight: 600;
}

.leave-game-btn {
  width: 100%;
  padding: 12px 24px;
  background-color: #ef4444;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s;
}

.leave-game-btn:hover {
  background-color: #dc2626;
}
```

#### 3.3 WebSocket - Enviar Acción de Abandonar

```tsx
// Ejemplo: useWebSocket.ts o GameContext.tsx

const leaveGame = () => {
  if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) {
    wsRef.current.send(JSON.stringify({
      action: 'leave_game'
    }));
  }
};
```

#### 3.4 WebSocket - Manejar Evento de Jugador que Abandona

```tsx
// Ejemplo: useWebSocket.ts

useEffect(() => {
  if (!ws) return;

  const handleMessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data);

    switch (data.type) {
      case 'player_left':
        // Mostrar notificación
        toast.info(data.message || `${data.player_name} ha abandonado la partida`);

        // Actualizar lista de jugadores (el backend ya envía game_state después)
        // No necesitas hacer nada más, el broadcast_game_state se encarga
        break;

      case 'game_state':
        // Actualizar estado del juego
        setGameState(data);
        break;

      // ... otros casos
    }
  };

  ws.addEventListener('message', handleMessage);
  return () => ws.removeEventListener('message', handleMessage);
}, [ws]);
```

#### 3.5 Manejo de Redirección después de Abandonar

```tsx
// Ejemplo: GameBoard.tsx o useGame.ts

const handleLeaveGame = () => {
  // Enviar acción al backend
  leaveGame();

  // Desconectar WebSocket
  if (wsRef.current) {
    wsRef.current.close();
  }

  // Redirigir al home
  router.push('/');

  // Mostrar mensaje
  toast.success('Has abandonado la partida');
};
```

---

## 4. Unirse a Partida en RoundEndScreen

### Backend Implementation
El backend permite:
- Unirse a partidas en estado `round_ended`
- Asigna puntos aleatorios (±20% del jugador con más puntos)
- Añade al jugador al final del orden de turnos

### Frontend Changes Requeridos

#### 4.1 Modificar Lógica de Unirse a Sala

```tsx
// Ejemplo: JoinRoom.tsx o HomePage.tsx

const joinRoom = async (roomCode: string, playerName: string) => {
  try {
    const response = await fetch(`${API_URL}/room/join`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        room_code: roomCode,
        player_name: playerName
      })
    });

    if (!response.ok) {
      const error = await response.json();
      // ANTES: Solo permitía unirse antes de que el juego comenzara
      // AHORA: El backend permite unirse durante round_ended
      throw new Error(error.detail || 'Error al unirse');
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error joining room:', error);
    throw error;
  }
};
```

#### 4.2 Manejar Evento de Mid-Game Join

```tsx
// Ejemplo: useWebSocket.ts

const handleMessage = (event: MessageEvent) => {
  const data = JSON.parse(event.data);

  switch (data.type) {
    case 'player_joined':
      if (data.mid_game_join) {
        // Jugador se unió en medio del juego (durante round_ended)
        toast.info(
          `${data.player.name} se ha unido a la partida con ${data.player.score} puntos`
        );
      } else {
        // Unión normal antes de empezar el juego
        toast.info(`${data.player.name} se ha unido a la sala`);
      }

      // Actualizar lista de jugadores
      setPlayers(prev => [...prev, data.player]);
      break;

    // ... otros casos
  }
};
```

#### 4.3 UI de RoundEndScreen - Mostrar Código para Nuevos Jugadores

```tsx
// Ejemplo: RoundEndScreen.tsx

const RoundEndScreen = ({ roomCode, scores }: Props) => {
  const [showShareCode, setShowShareCode] = useState(false);

  return (
    <div className="round-end-screen">
      <h2>Fin de Ronda</h2>

      {/* Tabla de puntuaciones */}
      <ScoreTable scores={scores} />

      {/* Sección para compartir código */}
      <div className="share-section">
        <button
          onClick={() => setShowShareCode(!showShareCode)}
          className="share-btn"
        >
          Invitar más jugadores
        </button>

        {showShareCode && (
          <div className="room-code-share">
            <p>Los nuevos jugadores pueden unirse ahora usando el código:</p>
            <div className="code-display">
              <span className="code">{roomCode}</span>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(roomCode);
                  toast.success('Código copiado');
                }}
                className="copy-btn"
              >
                Copiar
              </button>
            </div>
            <p className="info-text">
              Los nuevos jugadores empezarán con puntos aleatorios similares
              a los jugadores actuales
            </p>
          </div>
        )}
      </div>

      {/* Botón de continuar (solo para host) */}
      <button onClick={onContinue} className="continue-btn">
        Continuar a la siguiente ronda
      </button>
    </div>
  );
};
```

#### 4.4 Estilos CSS para RoundEndScreen

```css
/* styles/RoundEndScreen.css */

.share-section {
  margin: 24px 0;
  text-align: center;
}

.share-btn {
  padding: 10px 20px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.share-btn:hover {
  background-color: #2563eb;
}

.room-code-share {
  margin-top: 16px;
  padding: 16px;
  background-color: #f3f4f6;
  border-radius: 8px;
}

.code-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin: 12px 0;
}

.code {
  font-size: 32px;
  font-weight: bold;
  font-family: monospace;
  letter-spacing: 4px;
  padding: 8px 16px;
  background-color: white;
  border-radius: 8px;
  border: 2px solid #d1d5db;
}

.copy-btn {
  padding: 8px 16px;
  background-color: #10b981;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.copy-btn:hover {
  background-color: #059669;
}

.info-text {
  margin-top: 12px;
  font-size: 12px;
  color: #6b7280;
  font-style: italic;
}
```

#### 4.5 Actualizar Estado del Juego con Nuevos Jugadores

```tsx
// Ejemplo: useGameState.ts o GameContext.tsx

useEffect(() => {
  if (!ws) return;

  const handleMessage = (event: MessageEvent) => {
    const data = JSON.parse(event.data);

    if (data.type === 'game_state') {
      // El backend ya incluye los nuevos jugadores en game_state
      setGameState({
        ...data,
        // Los nuevos jugadores ya están en data.players
        // con sus puntos calculados y manos/melds vacíos
      });
    }
  };

  ws.addEventListener('message', handleMessage);
  return () => ws.removeEventListener('message', handleMessage);
}, [ws]);
```

---

## 5. Resumen de Eventos WebSocket

### Eventos que el Frontend debe ENVIAR

```typescript
// 1. Abandonar partida
{
  action: 'leave_game'
}
```

### Eventos que el Frontend debe ESCUCHAR

```typescript
// 1. Jugador abandonó la partida
{
  type: 'player_left',
  player_id: string,
  player_name: string,
  message: string
}

// 2. Jugador se unió (incluyendo mid-game)
{
  type: 'player_joined',
  player: {
    id: string,
    name: string,
    score: number,
    is_host: boolean
  },
  mid_game_join: boolean  // true si se unió durante round_ended
}

// 3. Estado del juego actualizado (se envía después de player_left y player_joined)
{
  type: 'game_state',
  // ... todo el estado del juego actualizado
  players: Array<Player>,  // Lista actualizada de jugadores
  // ... resto del estado
}
```

---

## 6. Testing Checklist

### Código de Sala
- [ ] Input solo acepta 3 dígitos numéricos
- [ ] No permite letras ni caracteres especiales
- [ ] Validación correcta antes de unirse
- [ ] Código se muestra correctamente en la UI

### Abandonar Partida
- [ ] Botón de menú hamburguesa visible en el tablero
- [ ] Modal se abre y cierra correctamente
- [ ] Confirmación antes de abandonar
- [ ] WebSocket envía acción correctamente
- [ ] Redirección al home después de abandonar
- [ ] Otros jugadores ven notificación
- [ ] Estado del juego se actualiza (turnos, cartas)

### Unirse Mid-Game
- [ ] Se puede unirse durante RoundEndScreen
- [ ] No se puede unirse durante una ronda activa
- [ ] Nuevo jugador recibe puntos aleatorios correctos
- [ ] Nuevo jugador aparece en la lista de jugadores
- [ ] Nuevo jugador recibe cartas en la siguiente ronda
- [ ] Código de sala se puede compartir fácilmente
- [ ] Notificación cuando alguien se une mid-game

### Jokers
- [ ] Información de reglas actualizada (3 jokers por mazo)
- [ ] Tooltips reflejan el nuevo número de jokers

---

## 7. Ejemplo de Integración Completa

```tsx
// Ejemplo: GameBoard.tsx - Componente principal del juego

import { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { toast } from 'react-hot-toast';
import GameMenu from './GameMenu';

const GameBoard = () => {
  const router = useRouter();
  const { roomCode, playerId } = router.query;
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [gameState, setGameState] = useState(null);

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
          break;

        case 'player_left':
          toast.info(data.message);
          break;

        case 'player_joined':
          if (data.mid_game_join) {
            toast.info(
              `${data.player.name} se unió con ${data.player.score} puntos`
            );
          } else {
            toast.info(`${data.player.name} se unió`);
          }
          break;

        // ... otros eventos
      }
    };

    setWs(websocket);

    return () => websocket.close();
  }, [roomCode, playerId]);

  // Función para abandonar partida
  const handleLeaveGame = () => {
    if (ws && ws.readyState === WebSocket.OPEN) {
      ws.send(JSON.stringify({ action: 'leave_game' }));
    }
    ws?.close();
    router.push('/');
    toast.success('Has abandonado la partida');
  };

  return (
    <div className="game-board">
      <header className="game-header">
        <div className="room-info">
          <span>Sala: {roomCode}</span>
          <span>Ronda: {gameState?.round || 1}</span>
        </div>

        {/* Menú hamburguesa para abandonar */}
        <GameMenu onLeaveGame={handleLeaveGame} />
      </header>

      {/* Resto del tablero de juego */}
      {/* ... */}
    </div>
  );
};

export default GameBoard;
```

---

## 8. Notas Importantes

1. **Código de Sala:**
   - Los códigos ahora son solo 3 dígitos (100-999)
   - Más fácil de compartir y recordar
   - Validar en el frontend antes de enviar al backend

2. **Abandonar Partida:**
   - Las cartas vuelven automáticamente al mazo (backend lo maneja)
   - Los turnos se ajustan automáticamente
   - Si todos abandonan, la sala se elimina

3. **Unirse Mid-Game:**
   - Solo posible durante `round_ended` (pantalla de puntuaciones)
   - El jugador nuevo empieza con puntos similares a los existentes
   - Se integra automáticamente en la siguiente ronda

4. **Jokers:**
   - Cambio transparente, solo actualizar documentación/UI
   - El backend maneja la creación de mazos

---

## 9. Recursos Adicionales

- **API URL:** `http://localhost:8000/api` (desarrollo)
- **WebSocket URL:** `ws://localhost:8000/api/ws/{room_code}/{player_id}`
- **Producción:** Actualizar URLs según tu deployment

---

## 10. Soporte

Si encuentras algún problema o necesitas aclaraciones:
- Revisa los logs del backend para ver los eventos que se están enviando
- Usa las herramientas de desarrollo del navegador para inspeccionar los mensajes WebSocket
- Verifica que los eventos se estén manejando correctamente en el frontend

---

**Fecha de actualización:** 2025-01-18
**Versión del Backend:** 1.1.0
