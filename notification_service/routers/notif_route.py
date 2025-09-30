from fastapi import APIRouter,websockets , WebSocketDisconnect, Depends
from starlette.websockets import WebSocket
import asyncio
from sqlalchemy.future import select

from connection_manager import manager
from models.notif_model import NotificationModel
from dependencies import SessionDep,get_validated_user_data
from schemas.notif_shema import ReceiveNotifySchema, SendNotifySchema , NotificationKind
from tasks.notif_tasks import create_broadcast_notifications_task, notify_list_users_task
from rabbitmq_manager import rb_manager
router = APIRouter()

#......................................................................................................................

@router.post("/notif/send")
async def send_notification_route(notif_data: ReceiveNotifySchema, db: SessionDep):
    payload = {
        "type": "notification",
        "sender": notif_data.sender_id,
        "message": notif_data.message
    }
    kind = notif_data.kind
    if kind == NotificationKind.BROADCAST:
        await rb_manager.publish_to_fanout("fanout_ex", payload)
        create_broadcast_notifications_task.delay(message=notif_data.message, sender_id=notif_data.sender_id)
        return {"status": "Broadcast message sent."}

    elif kind == NotificationKind.LIST:
        receivers_list = notif_data.receiver_ids
        if receivers_list:
            #await manager.send_to_list(payload,user_ids=receivers_list)
            for receiver_id in receivers_list:
                await rb_manager.publish_to_queue(exchange_name="dc_ex", message=payload ,routing_key=str(receiver_id))
            notify_list_users_task.delay(message=notif_data.message,receivers_ids=receivers_list,sender_id=notif_data.sender_id)
            return {"status": "Notification list sent."}

    elif kind == NotificationKind.PERSONAL:
        receiver_list = notif_data.receiver_ids
        receiver=receiver_list[0]
        await rb_manager.publish_to_queue(exchange_name="dc_ex", message=payload, routing_key=str(receiver))
        notif_model = NotificationModel(sender_id=notif_data.sender_id, message=notif_data.message,receiver_id=receiver)
        db.add(notif_model)
        await db.commit()
        await db.refresh(notif_model)

        return {"status": "Notification sent."}
#......................................................................................................................


@router.websocket("/notif/{user_id}")
async def notif(websocket: WebSocket, user_id: int, db: SessionDep, user_data: dict = Depends(get_validated_user_data)):

    #Authentication
    token_user_id =int(user_data.get("user_id"))
    if token_user_id != user_id:
        await websocket.close(code=1008)
        return
    await websocket.accept()
    print(f"User {user_id} with role {user_data.get('role')} connected.")
    #websocket_ready_event = asyncio.Event()


    async def handle_rabbitmq_messages():
        #await websocket_ready_event.wait()
        await rb_manager.consume(user_id, websocket)

    async def handle_client_commands():
        """Listens for commands from the client and processes them."""
        try:
            while True:
                #websocket_ready_event.set()
                data = await websocket.receive_json()
                action = data.get("action")

                if action == "ping":
                    await websocket.send_json({"type": "pong"})

                # Corrected: Changed to 'elif'
                elif action == "mark_as_read":
                    notification_id = data.get("notification_id")
                    if notification_id:
                        notif_to_update = db.query(NotificationModel).filter(
                            NotificationModel.id == notification_id,
                            NotificationModel.receiver_id == user_id).first()

                        if notif_to_update:
                            notif_to_update.is_read = True
                            db.commit()
                            db.refresh(notif_to_update)

                            await websocket.send_json({
                                "status": "success",
                                "message": f"Notification {notification_id} marked as read."
                            })
        except WebSocketDisconnect:
            #websocket_ready_event.clear()
            manager.disconnect(user_id)


    await asyncio.gather(handle_rabbitmq_messages(),handle_client_commands())



#......................................................................................................................
