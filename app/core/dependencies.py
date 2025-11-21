from fastapi import Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import async_session
from app.core.jwt_config import decode_token, get_token_from_cookie
from app.services.user_service import get_user_by_id, get_user_by_email
from app.core.security import verify_password

async def get_db():
    async with async_session() as session:
        yield session

async def get_current_user(request: Request,db: AsyncSession = Depends(get_db)):
    try:
        token = get_token_from_cookie(request=request)
        payload = decode_token(token)
        print(payload)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        user = await get_user_by_id(db, int(user_id))

        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    
async def authenticate_user(db:AsyncSession, email:str, password:str):
    user = await get_user_by_email(db, email)
    if not user:
        return None
    
    if not verify_password(password, user.password_hash):
        return None
    
    return user

