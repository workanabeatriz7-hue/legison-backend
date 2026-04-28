from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from openai import OpenAI

# Importando a nossa configuração do Banco de Dados
from database import SessionLocal, engine
import models

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="LegisON API", description="Motor do Assistente Jurídico Inteligente")

# Aqui incluímos o espaço para a "dissertação" livre que o Tony pediu
class DadosLead(BaseModel):
    nome: str
    area_direito: str
    relato_do_cliente: str 

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "online", "mensagem": "API do LegisON.ia está rodando perfeitamente! 🚀"}

@app.post("/gerar-peticao/")
def gerar_peticao(dados: DadosLead, db: Session = Depends(get_db)):
    
    # 1. Garante que o Advogado (Tony) existe no banco
    advogado = db.query(models.Advogado).first()
    if not advogado:
        advogado = models.Advogado(nome="Tony Silvério", email="tony@legison.com")
        db.add(advogado)
        db.commit()
        db.refresh(advogado)

    # 2. Salva o Cliente no banco de dados
    novo_lead = models.Lead(
        tenant_id=advogado.id,
        nome=dados.nome,
        telefone="11999999999", 
        area_direito=dados.area_direito
    )
    db.add(novo_lead)
    db.commit()
    db.refresh(novo_lead)

    # 3. O "Cérebro" da IA refinado para ler o textão do cliente
    prompt_sistema = f"""
    Você é um assistente jurídico sênior altamente qualificado no Brasil, especialista em Direito {dados.area_direito}.
    Sua tarefa é ler o relato cru e informal do cliente e transformar isso em um parágrafo inicial formal e técnico de uma petição inicial.
    Foque apenas nos fatos juridicamente relevantes. Não invente leis, use apenas a legislação vigente e jurisprudência aplicável.
    """
    
    prompt_usuario = f"Nome do Cliente: {dados.nome}\nRelato do Cliente (com as próprias palavras): {dados.relato_do_cliente}\n\nEscreva a introdução da petição."

    resposta = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt_sistema},
            {"role": "user", "content": prompt_usuario}
        ],
        temperature=0.3
    )
    texto_peticao = resposta.choices[0].message.content

    # 4. Salva a Petição gerada no banco de dados
    nova_peticao = models.Peticao(
        tenant_id=advogado.id,
        lead_id=novo_lead.id,
        conteudo_gerado=texto_peticao
    )
    db.add(nova_peticao)
    db.commit()
    
    return {
        "mensagem": "Sucesso! Tudo salvo no Banco de Dados. 💾",
        "cliente": novo_lead.nome,
        "peticao_gerada": texto_peticao
    }