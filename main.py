from fastapi import FastAPI, Depends, Request, Response
from pydantic import BaseModel
from sqlalchemy.orm import Session
import os, requests
from openai import OpenAI
from database import SessionLocal, engine
import models

# Inicialização da OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Criação das tabelas no banco de dados
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Variáveis de Ambiente (Configuradas no Render)
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"status": "API do LegisON.ia está rodando perfeitamente!"}

# --- ROTAS DO WHATSAPP (WEBHOOK) ---

# 1. Validação do Webhook (O "Aperto de Mão" com a Meta)
@app.get("/webhook")
def verify_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if token == "legison_token_secreto":
        return Response(content=challenge, media_type="text/plain")
    return "Token de verificação inválido"

# 2. Recebimento e Resposta de Mensagens
@app.post("/webhook")
async def receive_whatsapp(request: Request):
    data = await request.json()
    
    try:
        # Extrai a mensagem e o número do remetente
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            message = entry['messages'][0]
            sender_number = message['from']
            text_received = message['text']['body']

            # A IA processa o relato do cliente
            resposta_ia = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é o assistente jurídico LegisON. Sua função é ouvir o relato do cliente, ser empático e organizar os pontos principais para uma petição. Responda de forma profissional e breve."},
                    {"role": "user", "content": text_received}
                ],
                max_tokens=500
            ).choices[0].message.content

            # Envia a resposta de volta para o WhatsApp do cliente via API da Meta
            url = f"https://graph.facebook.com/v18.0/{PHONE_NUMBER_ID}/messages"
            headers = {
                "Authorization": f"Bearer {WHATSAPP_TOKEN}",
                "Content-Type": "application/json"
            }
            payload = {
                "messaging_product": "whatsapp",
                "to": sender_number,
                "type": "text",
                "text": {"body": resposta_ia}
            }
            requests.post(url, json=payload, headers=headers)

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")
    
    return {"status": "ok"}
