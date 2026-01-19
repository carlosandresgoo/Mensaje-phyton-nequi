# API de Mensajería - Prueba Técnica Nequi

## 1. Descripción General del Proyecto
Este proyecto consiste en una API REST desarrollada con **FastAPI** para la gestión y procesamiento de mensajes. La solución implementa una arquitectura limpia dividida en capas de API, Servicios y Repositorios, garantizando escalabilidad y mantenibilidad.

**Funcionalidades principales:**
* **Persistencia:** Almacenamiento de mensajes en base de datos SQLite mediante SQLAlchemy.
* **Procesamiento:** Filtro automático de palabras prohibidas y cálculo de metadatos (conteo de palabras y caracteres).
* **Seguridad:** Protección de endpoints mediante validación de **API Key**.
* **Calidad:** Cobertura de pruebas unitarias y de integración del **97%**.

---

## 2. Instrucciones de Configuración

### Instalación Local
1.  **Clonar el repositorio:**
    ```powershell
     git clone https://github.com/carlosandresgoo/Mensaje-phyton-nequi.git
    ```

2.  **Configurar entorno virtual:**
    ```powershell
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Instalar dependencias:**
    ```powershell
    pip install -r requirements.txt
    ```

4.  **Ejecutar la aplicación:**
    ```powershell
    uvicorn app.main:app --reload
    ```
    La API estará disponible en `http://127.0.0.1:8000`.

---

## 3. Documentación de la API
La documentación técnica detallada (OpenAPI/Swagger) se genera automáticamente:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Autenticación
Todas las peticiones a los endpoints protegidos deben incluir:
* **Header:** `X-API-Key`
* **Valor:** `nequi-secret-2026`

### Endpoints Principales

#### `POST /api/messages`
Envía un mensaje para ser procesado y almacenado.

#### `GET /api/messages/{session_id}`
Consulta el historial de mensajes asociados a una sesión específica.

#### `GET /api/messages/search`
Busca mensajes por contenido o remitente.

#### `WebSocket /ws/messages`
Permite recibir actualizaciones de mensajes en tiempo real mediante WebSocket.

**Conexión:**
```
ws://127.0.0.1:8000/ws/messages
```

**Funcionamiento:**
- Cada vez que un cliente envía un mensaje JSON por el WebSocket, este se retransmite (broadcast) a todos los clientes conectados.
- El mensaje debe tener formato JSON.

**Ejemplo de conexión en JavaScript:**
```js
const ws = new WebSocket('ws://127.0.0.1:8000/ws/messages');
ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.event === 'new_message') {
        console.log('Nuevo mensaje:', data.data);
    }
};
ws.onopen = () => {
    ws.send(JSON.stringify({ message: '¡Hola en tiempo real!' }));
};
```

---

## 4. Instrucciones para Pruebas
El proyecto utiliza **Pytest** para asegurar la calidad del código.

### Ejecución de Pruebas
```powershell
$env:PYTHONPATH = "."
python -m pytest
```

---

## 5. Puntos Extra Implementados

### Mecanismo de Autenticación Simple
Todos los endpoints protegidos requieren el header `X-API-Key` con un valor secreto para acceder. Si la clave es incorrecta o falta, la API responde con `401 Unauthorized`. Esto asegura que solo usuarios autorizados puedan interactuar con los recursos sensibles.

### WebSocket para Actualizaciones en Tiempo Real
Se implementó un endpoint WebSocket (`/ws/messages`) que permite a los clientes recibir notificaciones instantáneas cada vez que se envía un nuevo mensaje. Los mensajes enviados por un cliente se retransmiten automáticamente a todos los clientes conectados, facilitando la comunicación en tiempo real.

### Búsqueda Avanzada
Endpoint especializado para filtrar mensajes de forma eficiente.
* **Ruta:** `GET /api/messages/search`
* **Filtros:** Contenido (query string) y remitente (user_id).

###  Soporte Docker
Se incluye configuración para despliegue contenerizado, facilitando la portabilidad del microservicio.
* **Comando:** `docker compose up --build -d`

### Rate Limiting (Limitación de Tasa)
Mecanismo de seguridad para prevenir abusos de tráfico.
* **Límite:** 10 peticiones por minuto por IP.
* **Error:** `429 Too Many Requests`.

### Infraestructura como Código (IaC)
Propuesta de despliegue automatizado en **Azure** utilizando **Terraform** (ubicado en carpeta `/terraform`).
* **Recursos:** Azure Container Registry (ACR) y App Service.


