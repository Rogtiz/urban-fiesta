from fastapi import APIRouter, Depends, HTTPException
from app.groups.dao import GroupsDAO, InvitationsDAO
from app.groups.schemas import InvitationCreate, SGroup, SGroupCreate, GroupResponse
from app.users.auth import get_current_user
from app.users.models import Users


router = APIRouter(
    prefix="/groups",
    tags=["Groups"],
)

# windows 2003 Для диплома

@router.get("/")
async def get_groups(user: Users = Depends(get_current_user)) -> list[SGroup]:
    return await GroupsDAO.get_user_groups(user.id)


@router.get("/owned")
async def get_owned_groups(user: Users = Depends(get_current_user)) -> list[SGroup]:
    return await GroupsDAO.find_all(owner_id=user.id)


@router.get("/{group_id}/members")
async def get_group_members(group_id: int, user: Users = Depends(get_current_user)):
    group = await GroupsDAO.find_by_id(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    users = await GroupsDAO.get_group_members(group_id)
    if not users:
        raise HTTPException(status_code=404, detail="No members found in this group")
    return users


@router.get("/{group_id}")
async def get_group_by_id(group_id: int, user: Users = Depends(get_current_user)) -> GroupResponse:
    found_group = await GroupsDAO.find_by_id(group_id)
    if not found_group:
        raise HTTPException(status_code=404, detail="Group not found")
    # if found_group.owner_id != user.id:
    #     raise HTTPException(status_code=403, detail="Not authorized to access this group")
    group_members = await GroupsDAO.get_group_members(group_id)

    response_data = {
        "id": found_group.id,
        "name": found_group.name,
        "owner_id": found_group.owner_id,
        "members": group_members,
    }

    return response_data


@router.post("/")
async def create_group(group: SGroupCreate, user: Users = Depends(get_current_user)):
    # group.owner_id = user.id
    # existed_group = await GroupsDAO.find_one_or_none(name=group.name, owner_id=user.id)
    # if existed_group:
    #     raise HTTPException(status_code=400, detail="Group with this name already exists")
    # await GroupsDAO.add(**group.dict())
    # await GroupsDAO.set_user_group(user.id, group.id)
    # return {"detail": "Group created successfully"}
    existed_group = await GroupsDAO.find_one_or_none(name=group.name, owner_id=user.id)
    if existed_group:
        raise HTTPException(status_code=400, detail="Group with this name already exists")
    group_data = group.dict()
    group_data["owner_id"] = user.id
    new_group = await GroupsDAO.add(**group_data)
    await GroupsDAO.set_user_group(user.id, new_group.id)
    return {"detail": "Group created successfully"}


@router.put("/{group_id}")
async def update_group(group_id: int, group: SGroup, user: Users = Depends(get_current_user)) -> SGroup:
    found_group = await GroupsDAO.find_by_id(group_id)
    if not found_group:
        raise HTTPException(status_code=404, detail="Group not found")
    if found_group.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this group")

    updated_group = await GroupsDAO.update(group_id, **group.dict())
    return updated_group


@router.delete("/{group_id}")
async def delete_group(group_id: int, user: Users = Depends(get_current_user)) -> dict:
    found_group = await GroupsDAO.find_by_id(group_id)
    if not found_group:
        raise HTTPException(status_code=404, detail="Group not found")
    if found_group.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this group")

    await GroupsDAO.delete_group(group_id)
    return {"detail": "Group deleted successfully"}


@router.delete("/{group_id}/members/{user_id}")
async def remove_user_from_group(group_id: int, user_id: int, user: Users = Depends(get_current_user)) -> dict:
    found_group = await GroupsDAO.find_by_id(group_id)
    if not found_group:
        raise HTTPException(status_code=404, detail="Group not found")
    if found_group.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this group")

    await GroupsDAO.remove_user_group(user_id, group_id)
    return {"detail": "User removed from group successfully"}


@router.post("/{group_id}/leave")
async def leave_group(group_id: int, user: Users = Depends(get_current_user)) -> dict:
    found_group = await GroupsDAO.find_by_id(group_id)
    if not found_group:
        raise HTTPException(status_code=404, detail="Group not found")
    if found_group.owner_id == user.id:
        raise HTTPException(status_code=403, detail="Owner cannot leave the group")

    await GroupsDAO.remove_user_group(user.id, group_id)
    return {"detail": "Left the group successfully"}


@router.post("/invitations/send")
async def send_invitation(data: InvitationCreate, user: Users = Depends(get_current_user)):
    group = await GroupsDAO.find_by_id(data.group_id)
    if not group or group.owner_id != user.id:
        raise HTTPException(403, "Нет доступа к группе")

    existing = await InvitationsDAO.find_one_or_none(sender_id=user.id, receiver_id=data.receiver_id, group_id=data.group_id, status="pending")
    if existing:
        raise HTTPException(400, "Приглашение уже отправлено")

    return await InvitationsDAO.add(sender_id=user.id, receiver_id=data.receiver_id, group_id=data.group_id, message=data.message)


@router.get("/invitations/get")
async def get_my_invitations(user: Users = Depends(get_current_user)):
    invitations = await InvitationsDAO.find_all(receiver_id=user.id)

    return [
        {
            "id": invitation.id,
            "sender_id": invitation.sender_id,
            "group_id": invitation.group_id,
            "message": invitation.message,
            "status": invitation.status,
            "group_name": (await GroupsDAO.find_by_id(invitation.group_id)).name,
            "created_at": invitation.created_at,
        }
        for invitation in invitations
    ]


@router.post("/invitations/{id}/accept")
async def accept_invitation(id: int, user: Users = Depends(get_current_user)):
    invitation = await InvitationsDAO.find_by_id(id)
    if invitation.receiver_id != user.id:
        raise HTTPException(403, "Не ваше приглашение")

    await GroupsDAO.set_user_group(user.id, invitation.group_id)
    await InvitationsDAO.update_status(id, "accepted")
    return {"msg": "Вы присоединились к группе"}


@router.post("/invitations/{id}/decline")
async def decline_invitation(id: int, user: Users = Depends(get_current_user)):
    invitation = await InvitationsDAO.find_by_id(id)
    if invitation.receiver_id != user.id:
        raise HTTPException(403, "Не ваше приглашение")

    await InvitationsDAO.update_status(id, "declined")
    return {"msg": "Приглашение отклонено"}
