from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()

# Dicionário para armazenar conexões dos usuários
connections = {}

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await websocket.accept()
    connections[user_id] = websocket  # Salva a conexão do usuário

    try:
        while True:
            data = await websocket.receive_text()  # Recebe mensagem
            
            # Determina o destinatário
            recipient_id = "user2" if user_id == "user1" else "user1"

            # Se o destinatário estiver conectado, envia a mensagem para ele
            if recipient_id in connections:
                await connections[recipient_id].send_text(data)
                print(f"Mensagem enviada de {user_id} para {recipient_id}: {data}")
            else:
                print(f"{recipient_id} não está conectado.")

            # Apaga a mensagem do destinatário após 5 segundos
            await asyncio.sleep(5)
            if recipient_id in connections:
                await connections[recipient_id].send_text("__clear__")

    except WebSocketDisconnect:
        print(f"{user_id} desconectado.")
        del connections[user_id]  # Remove usuário desconectado
