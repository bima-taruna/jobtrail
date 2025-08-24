from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel
from .services import UserService
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.main import get_session
auth_router = APIRouter()
users_service = UserService()

@auth_router.post('/signup',response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data : UserCreateModel, session:AsyncSession =  Depends(get_session)):
    email = user_data.email
    user_exists = await users_service.user_exists(email,session)
    if user_exists :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email is already exists") 
    new_user  = await users_service.create_user(user_data, session)
    return new_user