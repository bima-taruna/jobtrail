from fastapi import APIRouter, Depends, status
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .services import UserService
from .utils import create_access_token, decode_token, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from datetime import timedelta
from fastapi.responses import JSONResponse
auth_router = APIRouter()
users_service = UserService()

REFRESH_TOKEN_EXPIRY = 2

@auth_router.post('/signup',response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data : UserCreateModel, session:AsyncSession =  Depends(get_session)):
    email = user_data.email
    user_exists = await users_service.user_exists(email,session)
    if user_exists :
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email is already exists") 
    new_user  = await users_service.create_user(user_data, session)
    return new_user

@auth_router.post('/login')
async def login_users(login_data:UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    
    user = await users_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid :
            access_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_id':str(user.id)
                }
            )
            
            refresh_token = create_access_token(
                user_data={
                    'email':user.email,
                    'user_id':str(user.id)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            
            return JSONResponse(
                content={
                    "message" : "Login Successfull",
                    "access_token" : access_token,
                    "refresh_token":refresh_token,
                    "user" : {
                        "email" : user.email,
                        "user_id" : str(user.id)
                    }
                }
            )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="invalid email or password"
    )

        
    