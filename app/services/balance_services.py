from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.utils import get_overall_net_map, simplify_debts
from app.models.user import User
from sqlalchemy import select
from decimal import Decimal

async def get_overall_balances(db: AsyncSession):
    net = await get_overall_net_map(db)

    return {
        uid: str(amount)
        for uid, amount in net.items()
        if amount != 0
    }

async def get_user_balance(
    db: AsyncSession,
    user_id: int
):
    net = await get_overall_net_map(db)
    return {
        "user_id": user_id,
        "net_balance": str(net.get(user_id, Decimal("0")))
    }

async def get_simplified_balances(db: AsyncSession):
    net = await get_overall_net_map(db)

    # Drop near-zero balances
    net = {
        uid: amt
        for uid, amt in net.items()
        if abs(amt) >= Decimal("0.01")
    }

    transfers = simplify_debts(net)

    if not transfers:
        return {
            "net": {},
            "settlements": []
        }

    user_ids = {u for t in transfers for u in (t[0], t[1])}

    q = select(User.id, User.name).where(User.id.in_(user_ids))
    res = await db.execute(q)
    users = {uid: name for uid, name in res.all()}

    return {
        "net": {
            uid: str(amt)
            for uid, amt in net.items()
        },
        "settlements": [
            {
                "from_id": f,
                "from_name": users.get(f),
                "to_id": t,
                "to_name": users.get(t),
                "amount": str(a)
            }
            for f, t, a in transfers
        ]
    }
