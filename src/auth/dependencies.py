from fastapi import Request, status,Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from fastapi.exceptions import HTTPException
from src.db.redis import token_in_blocklist
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .services import UserService
from typing import Any, List
from src.db.models import User
from src.job_application.services import JobApplicationService
from src.job_timeline.services import JobTimelineService

user_service = UserService()

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error =  True):
        super().__init__(auto_error=auto_error)
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        if creds is None or creds.credentials is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authenticated"
            )
        token = creds.credentials
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid or expired token"
            )
        
        # if token_data['refresh']:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Please provide an access token"
        #     )
        
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error" :"Token is invalid or has been revoked",
                    "resolution": "Please get a new token" 
                }
            ) 
        self.verify_token_data(token_data)    
        
        return token_data # type: ignore
    
    
    def token_valid(self, token:str)->bool:
        token_data = decode_token(token)
        if token_data is not None:
            return True
        else:
            return False
        
    def verify_token_data(self, token_data):
        raise  NotImplementedError('Please override this method in child classes')
        
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict)->None:
        if token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token"
            )


class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data:dict)->None:
        if not token_data.get("refresh", False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an refresh token"
            )


async def get_current_user(
    token_detail:dict = Depends(AccessTokenBearer()),
    session:AsyncSession = Depends(get_session)
    ):
    user_email = token_detail['user']['email']
    user = await user_service.get_user_by_email(user_email, session)
    return user

class RoleChecker:
    def __init__(self, allowed_roles:List[str]) -> None:
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user:User=Depends(get_current_user)) -> Any:
        if current_user.user_type.value in self.allowed_roles:
            return True
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="you are not permitted to perform this action"
        )

def get_timeline_service() -> JobTimelineService:
    return JobTimelineService()
        
def get_job_service(
     timeline_service: JobTimelineService = Depends(get_timeline_service)
    ) -> JobApplicationService:
    return JobApplicationService(timeline_service = timeline_service)
        


