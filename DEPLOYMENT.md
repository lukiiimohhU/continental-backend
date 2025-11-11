# Guía de Despliegue - Continental Card Game Backend

Esta guía te ayudará a desplegar el backend del juego Continental en Render.

## 📋 Requisitos Previos

1. Una cuenta en [Render](https://render.com)
2. Una cuenta en [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) (o cualquier MongoDB en la nube)
3. Tu repositorio de GitHub con este código

## 🚀 Paso 1: Configurar MongoDB Atlas

1. Ve a [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Crea un cluster gratuito (M0)
3. Crea un usuario de base de datos:
   - Ve a "Database Access"
   - Click en "Add New Database User"
   - Guarda el usuario y contraseña
4. Configura acceso desde cualquier IP:
   - Ve a "Network Access"
   - Click en "Add IP Address"
   - Selecciona "Allow Access from Anywhere" (0.0.0.0/0)
5. Obtén tu connection string:
   - Ve a "Database" → "Connect"
   - Selecciona "Connect your application"
   - Copia el connection string (ej: `mongodb+srv://usuario:contraseña@cluster.mongodb.net/`)

## 🌐 Paso 2: Desplegar en Render

### 2.1 Crear Web Service

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Click en "New +" → "Web Service"
3. Conecta tu repositorio de GitHub
4. Configura el servicio:

   **Basic Settings:**
   - **Name**: `continental-backend` (o el nombre que prefieras)
   - **Region**: Elige la región más cercana a tus usuarios
   - **Branch**: `main` (o tu rama principal)
   - **Root Directory**: Déjalo vacío (a menos que el backend esté en una subcarpeta)
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`

   **Instance Type:**
   - Selecciona "Free" para empezar

### 2.2 Configurar Variables de Entorno

En la sección "Environment Variables" de tu servicio en Render, añade:

1. **MONGO_URL**
   - Value: Tu connection string de MongoDB Atlas
   - Ejemplo: `mongodb+srv://usuario:contraseña@cluster.mongodb.net/`

2. **DB_NAME**
   - Value: `continental_game`

3. **CORS_ORIGINS**
   - Value: Las URLs de tu frontend separadas por comas
   - Ejemplos:
     - Para desarrollo local: `http://localhost:3000,http://127.0.0.1:3000`
     - Para producción: `https://tu-frontend.vercel.app,https://tu-dominio.com`
     - Para ambos: `http://localhost:3000,https://tu-frontend.vercel.app`

### 2.3 Desplegar

1. Click en "Create Web Service"
2. Espera a que Render construya y despliegue tu aplicación
3. Una vez completado, verás tu URL (ej: `https://continental-backend-xxxx.onrender.com`)

## ✅ Paso 3: Verificar el Despliegue

1. Abre tu URL de Render en el navegador (ej: `https://continental-backend-xxxx.onrender.com`)
2. Deberías ver una respuesta JSON como:
   ```json
   {
     "status": "ok",
     "message": "Continental Card Game Backend API",
     "version": "1.0",
     "endpoints": {
       "api": "/api",
       "websocket": "/api/ws/{room_code}/{player_id}"
     }
   }
   ```

3. Verifica que los endpoints funcionan:
   - Health check: `https://tu-url.onrender.com/`
   - API base: `https://tu-url.onrender.com/api`

## 🔧 Paso 4: Configurar el Frontend

En tu proyecto frontend, actualiza la URL del backend:

### Opción A: Variable de entorno (recomendado)

Crea un archivo `.env` en tu frontend:

```env
REACT_APP_BACKEND_URL=https://continental-backend-xxxx.onrender.com
REACT_APP_WS_URL=wss://continental-backend-xxxx.onrender.com
```

Y úsalo en tu código:

```javascript
const API_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';
```

### Opción B: Archivo de configuración

Crea un archivo `src/config.js`:

```javascript
const config = {
  development: {
    apiUrl: 'http://localhost:8000',
    wsUrl: 'ws://localhost:8000'
  },
  production: {
    apiUrl: 'https://continental-backend-xxxx.onrender.com',
    wsUrl: 'wss://continental-backend-xxxx.onrender.com'
  }
};

const env = process.env.NODE_ENV || 'development';
export default config[env];
```

## 🐛 Solución de Problemas

### Problema: 404 en todas las rutas

**Solución**: Asegúrate de que:
- El comando de inicio es exactamente: `uvicorn server:app --host 0.0.0.0 --port $PORT`
- El archivo `server.py` está en la raíz del repositorio

### Problema: CORS errors en el frontend

**Solución**: Verifica que:
1. La variable `CORS_ORIGINS` en Render incluye la URL exacta de tu frontend
2. La URL incluye el protocolo (`http://` o `https://`)
3. No hay espacios en la lista de URLs
4. Si usas múltiples URLs, están separadas por comas sin espacios: `http://localhost:3000,https://miapp.vercel.app`

### Problema: "Application failed to respond"

**Solución**: Esto puede significar:
1. MongoDB no está accesible - verifica tu connection string
2. Falta la variable `$PORT` - asegúrate de usar `--port $PORT` en el comando de inicio
3. El servidor no arrancó correctamente - revisa los logs en Render

### Problema: WebSocket connection failed

**Solución**: Asegúrate de:
1. Usar `wss://` (no `ws://`) para HTTPS
2. La URL del WebSocket incluye `/api/ws/` en la ruta
3. No hay proxies bloqueando WebSocket

### Problema: "No routes matched location '/continental'"

**Solución**: Esto es un problema del frontend:
1. Verifica que React Router esté configurado correctamente
2. Asegúrate de que la ruta `/continental` existe en tu configuración de rutas
3. Si usas React Router v6, revisa la sintaxis de las rutas

## 📊 Monitoreo

1. **Logs**: Ve a tu servicio en Render → "Logs" para ver logs en tiempo real
2. **Metrics**: Ve a "Metrics" para ver uso de CPU, memoria, y requests
3. **Events**: Ve a "Events" para ver despliegues y errores

## 🔄 Actualizaciones

Render automáticamente redesplega cuando:
- Haces push a la rama configurada (ej: `main`)
- Cambias variables de entorno (requiere despliegue manual)

Para desplegar manualmente:
1. Ve a tu servicio en Render
2. Click en "Manual Deploy" → "Deploy latest commit"

## 💡 Consejos Adicionales

1. **Free Tier**: Los servicios gratuitos de Render se "duermen" después de 15 minutos de inactividad. La primera request puede tardar 30-50 segundos en responder.

2. **Mantener activo**: Si quieres mantener tu servicio activo, puedes usar servicios como [UptimeRobot](https://uptimerobot.com/) para hacer ping cada 5 minutos.

3. **Logs**: Siempre revisa los logs en Render si algo no funciona. Contienen información valiosa sobre errores.

4. **Variables de entorno**: Nunca commitees archivos `.env` con credenciales reales. Usa siempre las variables de entorno de Render.

5. **MongoDB Atlas**: El tier gratuito de Atlas tiene un límite de 512MB. Para producción, considera actualizar.

## 🔐 Seguridad

1. **MongoDB**: Usa contraseñas fuertes y únicas
2. **CORS**: Solo permite los orígenes que realmente necesitas
3. **Variables de entorno**: Nunca expongas tus credenciales en el código
4. **HTTPS**: Render proporciona HTTPS automáticamente - siempre úsalo

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Render
2. Verifica que todas las variables de entorno estén configuradas
3. Prueba los endpoints manualmente con Postman o curl
4. Revisa la documentación de [Render](https://render.com/docs)

---

**¡Listo!** Tu backend debería estar funcionando en Render. 🎉
