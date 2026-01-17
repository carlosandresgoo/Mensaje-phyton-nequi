# API de Mensajería - Prueba Técnica Nequi

## 1. Descripción General del Proyecto
Este proyecto consiste en una API REST desarrollada con **FastAPI** para la gestión y procesamiento de mensajes. La solución implementa una arquitectura limpia (Clean Architecture) dividida en capas de API, Servicios y Repositorios.

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
    cd Mensaje-phyton-nequi
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
La documentación técnica detallada (OpenAPI/Swagger) se genera automáticamente y se puede consultar en:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Autenticación
Todas las peticiones a los endpoints protegidos deben incluir un encabezado de autenticación:
* **Header:** `X-API-Key`
* **Valor:** `nequi-secret-2026`

### Endpoints

#### `POST /api/messages`
Envía un mensaje para ser procesado y almacenado. El contenido del mensaje es analizado para filtrar palabras prohibidas y calcular metadatos.

*   **Request Body:**
    ```json
    {
        "message_id": "string",
        "session_id": "string",
        "content": "string",
        "timestamp": "2024-01-01T12:00:00Z",
        "sender": "string"
    }
    ```

*   **Success Response (201):**
    ```json
    {
        "status": "success",
        "data": {
            "message_id": "string",
            "session_id": "string",
            "content": "string",
            "timestamp": "2024-01-01T12:00:00Z",
            "sender": "string",
            "metadata": {
                "word_count": 0,
                "char_count": 0,
                "has_profanity": false
            }
        }
    }
    ```

#### `GET /api/messages/{session_id}`
Consulta el historial de mensajes asociados a una `session_id` específica.

*   **Path Parameters:**
    *   `session_id` (string): Identificador de la sesión a consultar.

*   **Query Parameters (Opcionales):**
    *   `sender` (string): Filtra los mensajes por el remitente.
    *   `skip` (int, default: 0): Omite los primeros N resultados (para paginación).
    *   `limit` (int, default: 10): Limita el número de resultados devueltos.

*   **Success Response (200):**
    ```json
    [
        {
            "status": "success",
            "data": {
                "message_id": "string",
                "session_id": "string",
                "content": "string",
                // ... otros campos del mensaje
            }
        }
    ]
    ```

---

## 4. Instrucciones para Pruebas
El proyecto utiliza **Pytest** para las pruebas unitarias y de integración. Los reportes de cobertura son generados para asegurar la calidad del código.

### Ejecución de Pruebas
Para ejecutar el conjunto de pruebas, utilice el siguiente comando desde la raíz del proyecto:

```powershell
$env:PYTHONPATH = "."
python -m pytest
```

