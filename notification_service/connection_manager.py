from typing import Dict, Any , List
from fastapi import  WebSocket

from dotenv import load_dotenv

load_dotenv()




class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_json(self, data: Dict[str, Any], user_id: int):

        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            await websocket.send_json(data)

    async def send_to_list(self, data: Dict[str, Any], user_ids: List[int]):
        for user_id in user_ids:
            await self.send_personal_json(data, user_id)

    async def broadcast(self, data: Dict[str, Any]):
        for connection in list(self.active_connections.values()):
            await connection.send_json(data)


manager = ConnectionManager()