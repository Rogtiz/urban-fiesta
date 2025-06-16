from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, Response, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError, jwt

from app.tags.dao import TagsDAO
from app.users.auth import ALGORITHM, SECRET_KEY, create_access_token, create_email_confirmation_token, create_refresh_token, get_current_user, get_password_hash, get_token, verify_email_confirmation_token, verify_password
from app.users.dao import UsersDAO
from app.groups.dao import GroupsDAO
from app.users.schemas import TokenResponse, UserCollaborators, UserCreate, UserResponse, UserFullInfoSchema, UserUpdate
from app.users.models import Users
from app.users.utils import send_verification_email

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# background_tasks = BackgroundTasks()

@router.post("/register")
async def register_user(user_data: UserCreate):
    result = await UsersDAO.find_one_or_none(username=user_data.username)
    if result:
        if result.username == user_data.username:
            raise HTTPException(status_code=400, detail="Username already exists")
        if result.email == user_data.email:
            raise HTTPException(status_code=400, detail="Email already exists")
        
    user = Users(
        username=user_data.username,
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password)
    )

    await UsersDAO.add(username=user.username, email=user.email, hashed_password=user.hashed_password)

    token = create_email_confirmation_token(user)
    send_verification_email(user.email, token)

    return {"Info": "User registered successfully. Please verify your email"}


@router.get("/verify-email")
async def verify_email(token: str):
    payload = verify_email_confirmation_token(token)
    if not payload:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    user = await UsersDAO.find_by_email(payload.get("sub"))
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    await UsersDAO.update(user.id, is_verified=True)

    return {"Info": "Email verified successfully"}


@router.get("/request-email-verification")
async def request_email_verification(user: Users = Depends(get_current_user)):
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Email already verified")
    
    token = create_email_confirmation_token(user)
    send_verification_email(user.email, token)

    return {"Info": "Verification email sent successfully"}


@router.post("/login")
async def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    user = await UsersDAO.find_one_or_none(username=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response.set_cookie("access_token", access_token, httponly=True, max_age=1800)
    response.set_cookie("refresh_token", refresh_token, httponly=True, max_age=604800)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh")
async def refresh(request: Request, response: Response):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=400, detail="Invalid token")
    
    access_token = await get_token(request, response)

    return {"access_token": access_token}


@router.get("/me", response_model=UserResponse)
async def get_me(user: Users = Depends(get_current_user)):
    return user


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"Info": "Logged out successfully"}


@router.get("/info")
async def get_user_info(user: Users = Depends(get_current_user)):
    return {"Info": "User info"}


@router.put("/update")
async def update_user(user_data: UserUpdate, user: Users = Depends(get_current_user)):
    result = await UsersDAO.find_one_or_none(username=user_data.username)
    if result:
        if result.username == user_data.username and result.id != user.id:
            raise HTTPException(status_code=400, detail="Username already exists")
        if result.email == user_data.email and result.id != user.id:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    # await UsersDAO.update(user.id, username=user_data.username, email=user_data.email)
    await UsersDAO.update(user.id, **user_data.dict(exclude_unset=True))

    return {"Info": "User updated successfully"}


@router.post("/{user_id}/groups/{group_id}")
async def add_user_to_group(user_id: int, group_id: int, user: Users = Depends(get_current_user)):
    found_user = await UsersDAO.find_by_id(user_id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    found_group = await GroupsDAO.find_by_id(group_id)
    if found_group.owner_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this group")
    if not found_group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if found_group.id in [group.id for group in await GroupsDAO.get_user_groups(user_id)]:
        raise HTTPException(status_code=400, detail="User already added to this group")
    
    await GroupsDAO.set_user_group(user_id, group_id)

    return {"Info": "User added to group successfully"}


@router.get("/open_to_collab", response_model=List[UserCollaborators])
async def get_open_to_collaboration(user: Users = Depends(get_current_user)):
    users = await UsersDAO.find_all_collaborators(user.id)
    
    return [
        {
            "id": user.id,
            "username": user.username,
            "full_name": user.full_name,
            "description": user.description,
            "tags": [tag.name for tag in await TagsDAO.get_user_tags(user.id)]
        }
        for user in users
    ]


@router.get("/collaborators/{user_id}", response_model=UserCollaborators)
async def get_user_collaborators(user_id: int, user: Users = Depends(get_current_user)):
    found_user = await UsersDAO.find_by_id(user_id)
    if not found_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": found_user.id,
        "username": found_user.username,
        "full_name": found_user.full_name,
        "description": found_user.description,
        "tags": [tag.name for tag in await TagsDAO.get_user_tags(found_user.id)]
    }
