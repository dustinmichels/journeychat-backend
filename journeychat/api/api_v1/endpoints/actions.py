from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from journeychat import crud, schemas
from journeychat.api import deps
from journeychat.models.user import User
from journeychat.schemas.room import Room, RoomCreate, RoomSearchResults
from journeychat.schemas.user import UserUpdate
from sqlalchemy.orm import Session

router = APIRouter()


@router.put("/join/{room_id}", response_model=Room)
def join_room(
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    room: Room = Depends(deps.get_room_authenticated),
) -> Any:
    """
    Join a room.
    """
    return crud.room.add_member(db=db, room=room, user=current_user)


@router.put("/invite/{room_id}/{username}", response_model=Room)
def add_user(
    username: str,
    *,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    room: Room = Depends(deps.get_room_authenticated),
) -> Any:
    """
    Invite a user to a room. If you are a member, they will be added immediately.
    """
    user_to_add = crud.user.get_by_username(db, username=username)
    if not user_to_add:
        raise HTTPException(
            status_code=404, detail=f"User with username '{username}' not found"
        )
    return crud.room.add_member(db=db, room=room, user=user_to_add)
