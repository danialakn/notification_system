import asyncio
from celery import shared_task
from typing import Optional

from database import AsyncSessionLocal
from models.notif_model import NotificationModel
from services.auth_service_connector import get_all_user_ids, get_list_user_ids


@shared_task
def create_broadcast_notifications_task(message: str, sender_id: Optional[int] = None):
    print(f"Starting broadcast task for message: {message} ")
    async def async_work():

        all_user_ids = await get_all_user_ids()

        if not all_user_ids:
            print("No users found.")
            return 0


        async with AsyncSessionLocal() as db:
            for user_id in all_user_ids:
                db_notification = NotificationModel(
                    sender_id=sender_id,
                    receiver_id=user_id,
                    message=message
                )
                db.add(db_notification)

            await db.commit()
        return len(all_user_ids)

    try:
        num_users = asyncio.run(async_work())
        result_message = f"Broadcast notification created for {num_users} users."
        print(result_message)
        return result_message
    except Exception as e:
        print(f"An error occurred in broadcast task: {e}")
        return "Task failed."


@shared_task
def notify_list_users_task(message: str,receivers_ids: list[int], sender_id: Optional[int] = None):
    print(f"Starting list users task for message: {message} ")
    async def async_work():

        user_ids =await get_list_user_ids(receivers_ids)
        print(user_ids)
        if not user_ids:
            print("No users found.")
            return 0

        async with AsyncSessionLocal() as db:
            for user_id in user_ids:
                db_notification = NotificationModel(
                    sender_id=sender_id,
                    receiver_id=user_id,
                    message=message
                )
                db.add(db_notification)
            await db.commit()
        return len(user_ids)

    try:
        num_users = asyncio.run(async_work())
        result_message = f"Broadcast notification created for {num_users} users."
        print(result_message)
        return result_message
    except Exception as e:
        print(f"An error occurred in broadcast task: {e}")
        return "Task failed."