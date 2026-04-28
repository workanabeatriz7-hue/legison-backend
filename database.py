from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Nome do arquivo do banco de dados que será gerado localmente
SQLALCHEMY_DATABASE_URL = "sqlite:///./legison.db"

# Criando o "motor" do banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Criando a sessão (a "ponte" de comunicação entre o código e o banco)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para criarmos as nossas tabelas depois
Base = declarative_base()