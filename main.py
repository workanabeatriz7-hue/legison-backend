from fastapi import FastAPI, Request, Response
import os, requests
from openai import OpenAI

# Inicialização segura do app
app = FastAPI()

# Carregamento das Variáveis de Ambiente do Render
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

# Tenta inicializar o cliente OpenAI sem derrubar o servidor se falhar
try:
    if OPENAI_KEY:
        client = OpenAI(api_key=OPENAI_KEY)
    else:
        client = None
        print("AVISO: Variável OPENAI_API_KEY não encontrada no Render.")
except Exception as e:
    client = None
    print(f"ERRO ao configurar OpenAI: {e}")

@app.get("/")
def home():
    return {"status": "LegisON API Online", "openai_configured": client is not None}

# 1. Validação do Webhook (Aperto de mão com a Meta)
@app.get("/webhook")
def verify_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    
    if token == "legison_token_secreto":
        return Response(content=challenge, media_type="text/plain")
    return Response(content="Token Inválido", status_code=403)

# 2. Recebimento e Resposta automática
@app.post("/webhook")
async def receive_whatsapp(request: Request):
    data = await request.json()
    
    try:
        # Verifica se é uma mensagem de texto recebida
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            value = data['entry'][0]['changes'][0]['value']
            message = value['messages'][0]
            sender_number = message['from']
            text_received = message.get('text', {}).get('body', '')

            if not text_received:
                return {"status": "no text"}

            # Processamento com a IA
            if client:
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "Você é o assistente jurídico LegisON. Seja profissional, empático e breve nas respostas via WhatsApp."},
                        {"role": "user", "content": text_received}
                    ]
                )
                resposta_ia = completion.choices[0].message.content
            else:
                resposta_ia = "Desculpe, estou em manutenção técnica (Chave de API ausente)."

            # Envio de volta para o WhatsApp (API v25.0)
            url = f"https://graph.facebook.com/v25.0/{PHONE_NUMBER_ID}/messages"
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
            
            resp_meta = requests.post(url, json=payload, headers=headers)
            print(f"RESPOSTA DA META: {resp_meta.status_code} - {resp_meta.text}")

    except Exception as e:
        print(f"ERRO NO PROCESSAMENTO: {str(e)}")
    
    return {"status": "ok"}
