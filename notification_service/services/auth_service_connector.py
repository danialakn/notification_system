# services/auth_service_client.py
import httpx
import os
from typing import List , Optional , Dict , Any


async def get_all_user_ids() -> List[int]:
    """
    Calls the internal API of the Auth service asynchronously to get all user IDs.
    """
    auth_service_url = os.getenv("AUTH_SERVICE_ALL_USER", "http://localhost:8000/accounts/api/internal/all-user-ids/")
    secret_key = os.getenv("INTERNAL_SERVICE_KEY")

    if not secret_key:
        print("Error: INTERNAL_SERVICE_KEY is not set.")
        return []

    headers = {'X-Internal-Service-Key': secret_key}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(auth_service_url, headers=headers, timeout=5)
            response.raise_for_status()

            user_data = response.json()
            return [user['id'] for user in user_data]

        except httpx.RequestError as e:
            print(f"Could not fetch user IDs from auth service: {e}")
            return []

#....................................................................................................

async def get_list_user_ids(users_list: list[int]) -> List[int]:
    """
    Calls the internal API of the Auth service asynchronously to get a list of user IDs.
    """
    auth_service_url = os.getenv("AUTH_SERVICE_LIST_USER", "http://localhost:8000/accounts/api/internal/list-user-ids/")
    secret_key = os.getenv("INTERNAL_SERVICE_KEY")

    if not secret_key:
        print("Error: INTERNAL_SERVICE_KEY is not set.")
        return []


    headers = {'X-Internal-Service-Key': secret_key}

    ids_as_strings = [str(user_id) for user_id in users_list]
    ids_query_string = ",".join(ids_as_strings)  # -> "1,5,12"
    params = {'ids': ids_query_string}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(auth_service_url, headers=headers, params=params, timeout=5)
            response.raise_for_status()

            user_ids = response.json()
            return [user['id'] for user in user_ids]

        except httpx.RequestError as e:
            print(f"Could not fetch user IDs from auth service: {e}")
            return []
#....................................................................................................


async def get_current_user_from_token(token: str) -> Optional[Dict[Any, Any]]:

    auth_service_url = os.getenv("AUTH_SERVICE_VALIDATE_URL", "http://localhost:8000/accounts/api/internal/token/validate/")
    secret_key = os.getenv("INTERNAL_SERVICE_KEY")


    if not secret_key:
        print("Error: INTERNAL_SERVICE_KEY is not set.")
        return None

    headers = {'X-Internal-Service-Key': secret_key}
    request_body = {"token": token}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(auth_service_url, headers=headers, json=request_body, timeout=5)
            response.raise_for_status()
            payload = response.json()
            return {
                "user_id": payload.get("user_id"),
                "role": payload.get("role")
            }

        except httpx.HTTPStatusError as e:

            print(f"Token validation failed: {e.response.status_code}")
            return None
        except httpx.RequestError as e:
            print(f"Could not connect to auth service: {e}")
            return None

#....................................................................................................
