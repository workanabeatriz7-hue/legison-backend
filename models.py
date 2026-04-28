from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.sql import func
from database import Base

class Advogado(Base):
    """Tabela dos donos da conta (Os Tenants / Clientes do Tony)"""
    __tablename__ = "advogados"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class Lead(Base):
    """Tabela dos clientes finais (que respondem o WhatsApp)"""
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("advogados.id")) # A mágica do isolamento multi-tenant
    nome = Column(String)
    telefone = Column(String)
    area_direito = Column(String) # Trabalhista, Consumidor ou Previdenciario

class Peticao(Base):
    """Tabela dos documentos gerados pela IA"""
    __tablename__ = "peticoes"
    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("advogados.id"))
    lead_id = Column(Integer, ForeignKey("leads.id"))
    conteudo_gerado = Column(Text)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())