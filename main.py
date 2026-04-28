from fastapi import FastAPI, Request, Response
import os, requests
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = FastAPI()

WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")

@app.get("/")
def home():
    return {"status": "online"}

@app.get("/webhook")
def verify_webhook(request: Request):
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")
    if token == "legison_token_secreto":
        return Response(content=challenge, media_type="text/plain")
    return "Token inválido"

@app.post("/webhook")
async def receive_whatsapp(request: Request):
    data = await request.json()
    try:
        if 'messages' in data['entry'][0]['changes'][0]['value']:
            message = data['entry'][0]['changes'][0]['value']['messages'][0]
            sender_number = message['from']
            text_received = message['text']['body']

            # IA Processando
            completion = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "Você é o assistente jurídico LegisON. Responda de forma empática e profissional."},
                    {"role": "user", "content": text_received}
                ]
            )
            resposta_ia = completion.choices[0].message.content

            # Envio de volta (Versão v25.0 atualizada)
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
            
            response = requests.post(url, json=payload, headers=headers)
            print(f"RESPOSTA DA META: {response.status_code} - {response.text}")

    except Exception as e:
        print(f"ERRO NO PROCESSAMENTO: {e}")
    
    return {"status": "ok"}
