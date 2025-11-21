from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.services.group_services import create_group, add_member, list_group_for_user, list_group_members, delete_group, remove_member, exit_group, edit_group
from app.schemas.group import GroupCreate, GroupMemberOut, GroupOut
from app.schemas.user import UserOut
from app.core.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=GroupOut)
async def create_new_group(
    data:GroupCreate,
    db: AsyncSession = Depends(get_db),
    user = Depends(get_current_user)
):
    group = await create_group(db, data.name, user.id)
    return group

@router.delete("/{group_id}")
async def del_group(group_id: int, db: AsyncSession = Depends(get_db), current_user: int = Depends(get_current_user)):
    return await delete_group(db, group_id=group_id, creator_id=current_user.id)

@router.post("/{group_id}/add/{user_id}", response_model=GroupMemberOut)
async def add_user_to_group(group_id: int, user_id: int, db: AsyncSession = Depends(get_db)):
    return await add_member(db, group_id, user_id)

@router.delete("/{group_id}/remove/{user_id}")
async def rem_mem(group_id: int, user_id : int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await remove_member(db, group_id=group_id, user_id=user_id, creator_id = current_user.id)

@router.delete("/{group_id}/exit")
async def exit(group_id: int, db:AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await exit_group(db, group_id=group_id, user_id=current_user.id)

@router.get("/my-groups", response_model=list[GroupOut])
async def my_groups(db: AsyncSession = Depends(get_db), user = Depends(get_current_user)):
    return await list_group_for_user(db, user.id)

@router.get("/{group_id}/group-members", response_model=list[UserOut])
async def group_members(group_id: int, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await list_group_members(db, current_user.id, group_id=group_id)

@router.patch("/{group_id}")
async def edit(group_id: int, data, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    return await edit_group(db, group_id, current_user.id, data)