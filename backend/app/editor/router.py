from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from app.users.auth import get_current_user_ws, get_current_user
from app.users.models import Users
from app.editor.manager import ConnectionManager
from app.editor.utils import is_user_allowed_to_edit


router = APIRouter(
    prefix="/editor",
    tags=["Editor"],
)
manager = ConnectionManager()


@router.websocket("/ws/{project_id}/{file_id}")
async def websocket_code_editor(
    websocket: WebSocket,
    project_id: int,
    file_id: str,
    user: Users = Depends(get_current_user_ws)
):
    # is_allowed = await is_user_allowed_to_edit(user.id, project_id)
    # if not is_allowed:
    #     await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    #     return

    await manager.connect(file_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(file_id, data, sender=websocket)
    except WebSocketDisconnect:
        await manager.disconnect(file_id, websocket)