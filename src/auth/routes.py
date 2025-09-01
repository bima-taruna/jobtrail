from fastapi import APIRouter, Depends, status
from src.db.redis import add_jti_to_blocklist
from .dependencies import AccessTokenBearer
from .schemas import UserCreateModel, UserModel, UserLoginModel, UserJobAppsModel
from .services import UserService
from .utils import create_access_token, decode_token, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from src.db.main import get_session
from datetime import timedelta
from fastapi.responses import JSONResponse
from src.auth.dependencies import AccessTokenBearer
from .dependencies import RefreshTokenBearer, get_current_user, RoleChecker
from datetime import datetime


access_token_bearer = AccessTokenBearer()
auth_router = APIRouter()
users_service = UserService()
role_checker_standard = Depends(RoleChecker(['ADMIN', 'USER', 'GUEST']))

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

@auth_router.get("/refresh_token", dependencies=[role_checker_standard])
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer)):
    expiry_timestamp = token_details['exp']
    
    if datetime.fromtimestamp(expiry_timestamp)>datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user']
        )
        
        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token")

@auth_router.get('/me',response_model=UserJobAppsModel, dependencies=[role_checker_standard])
async def get_me(token_detail: dict = Depends(AccessTokenBearer()), session: AsyncSession = Depends(get_session)):
    user = await get_current_user(token_detail=token_detail, session=session)
    return user

@auth_router.get("/logout", dependencies=[role_checker_standard])
async def revoke_token(token_details:dict=Depends(AccessTokenBearer())):
    jti = token_details['jti']
    await add_jti_to_blocklist(jti)
    return JSONResponse(
        content={
            "message": "Logged out succesfully"
        },
        status_code=status.HTTP_200_OK
    )