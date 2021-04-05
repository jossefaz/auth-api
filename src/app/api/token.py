from typing import Optional

from fastapi import APIRouter, status, HTTPException, Header
from .schemas import User
from ..utils import token, http

router = APIRouter()


def raise_401_exception():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect Credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(request: User):
    credentials = await http.check_user_credentials(request)
    if not credentials:
        raise_401_exception()
    access_token = token.create_access_token(
        data={"username": request.username, "id": credentials["id"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/credentials', status_code=status.HTTP_200_OK)
async def check_token(access_token: Optional[str] = Header(None)):
    if not access_token:
        raise_401_exception()
    token_data = token.verify_token(access_token)
    if not token_data:
        raise_401_exception()
    return token_data
