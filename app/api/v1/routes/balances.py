from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.services.balance_services import get_overall_balances, get_user_balance, get_simplified_balances

router = APIRouter()

@router.get("/overall")
async def overall_balances(
    db: AsyncSession = Depends(get_db)
):
    return await get_overall_balances(db)


@router.get("/user/{user_id}")
async def user_balance(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    return await get_user_balance(db, user_id)


@router.get("/simplified")
async def simplified_balances(
    db: AsyncSession = Depends(get_db)
):
    return await get_simplified_balances(db)
