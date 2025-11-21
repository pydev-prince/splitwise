from decimal import Decimal, ROUND_HALF_UP, getcontext
from typing import Dict, List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

getcontext().prec = 28
CENTS= Decimal("0.01")

def qround(d : Decimal) -> Decimal:
    return d.quantize(CENTS, rounding=ROUND_HALF_UP)

