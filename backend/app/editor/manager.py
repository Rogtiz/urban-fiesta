from fastapi import WebSocket
from typing import Dict, List


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, file_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.setdefault(file_id, []).append(websocket)

    async def disconnect(self, file_id: int, websocket: WebSocket):
        if file_id in self.active_connections:
            self.active_connections[file_id].remove(websocket)

    async def broadcast(self, file_id: int, message: str, sender: WebSocket = None):
        connections = self.active_connections.get(file_id, [])
        to_remove = []
        for connection in connections:
            if connection.client_state.name == "CONNECTED" and connection.application_state.name == "CONNECTED":
                if connection != sender:
                    try:
                        await connection.send_text(message)
                    except Exception:
                        to_remove.append(connection)
            else:
                to_remove.append(connection)

        for conn in to_remove:
            await self.disconnect(file_id, conn)
