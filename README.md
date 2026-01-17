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
    git clone [https://github.com/carlosandresgoo/Mensaje-phyton-nequi.git](https://github.com/carlosandresgoo/Mensaje-phyton-nequi.git)
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
La documentación técnica detallada (OpenAPI/Swagger) se genera automáticamente:

* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Autenticación Requerida
Todas las peticiones deben incluir el siguiente encabezado:
* **Header:** `X-API-Key`
* **Valor:** `nequi-secret-2026`

### Endpoints
* `POST /api/messages/`: Envía un mensaje para ser procesado y guardado.
* `GET /api/messages/{session_id}`: Consulta el historial de mensajes filtrado por sesión.

---

## 4. Instrucciones para Pruebas
Para garantizar la integridad del código, se utiliza **Pytest** con reportes de cobertura.

### Ejecución de pruebas unitarias:
```powershell
$env:PYTHONPATH = "."
python -m pytest