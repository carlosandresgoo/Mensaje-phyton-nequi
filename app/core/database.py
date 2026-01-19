from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# URL de conexión a la base de datos SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./mensaje_nequi.db"

# Crear el motor de la base de datos
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear la clase base para los modelos ORM
Base = declarative_base()

# Crear la fábrica de sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener una sesión de base de datos en los endpoints. Cierra la sesión automáticamente al finalizar.
def get_db():
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()