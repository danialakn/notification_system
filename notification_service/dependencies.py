from fastapi import Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import Annotated
from database import get_session
from services.auth_service_connector import get_current_user_from_token
from typing import Dict,Any


SessionDep = Annotated[Session, Depends(get_session)]


async def get_validated_user_data(token: str = Query(...) ) -> Dict[str, Any]:

    user_data = await get_current_user_from_token(token)

    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user_data

