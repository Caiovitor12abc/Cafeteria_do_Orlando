from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# URL de conexão local com o arquivo da base de dados
SQLALCHEMY_DATABASE_URL = "sqlite:///./cafeteria.db"

# Engine de conexão
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criador de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe Base para os modelos da base de dados
Base = declarative_base()

# Função utilitária para abrir e fechar conexões
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()