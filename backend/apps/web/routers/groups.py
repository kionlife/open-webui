from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from pydantic import BaseModel
import logging

from apps.web.models.groups import GroupModel, Groups
from utils.utils import get_admin_user, get_groupadmin_user, get_admin_or_groupadmin_user

log = logging.getLogger(__name__)
router = APIRouter()

############################
# GetGroups
############################

@router.get("/", response_model=List[GroupModel])
async def get_groups(skip: int = 0, limit: int = 50, user=Depends(get_admin_user)):
    return Groups.get_groups(skip, limit)


############################
# GetGroupById
############################

@router.get("/{group_id}", response_model=GroupModel)
async def get_group_by_id(group_id: int, user=Depends(get_admin_user)):
    group = Groups.get_group_by_id(group_id)
    if group:
        return group
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found",
        )


############################
# CreateGroup
############################

class GroupCreateForm(BaseModel):
    name: str

@router.post("/", response_model=Optional[GroupModel])
async def create_group(form_data: GroupCreateForm, user=Depends(get_admin_user)):
    new_group = Groups.insert_new_group(form_data.name)
    if new_group:
        return new_group
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create group",
        )


############################
# UpdateGroupById
############################

class GroupUpdateForm(BaseModel):
    name: str

@router.put("/{group_id}", response_model=Optional[GroupModel])
async def update_group_by_id(
        group_id: int, form_data: GroupUpdateForm, user=Depends(get_admin_user)
):
    updated_group = Groups.update_group_by_id(group_id, form_data.dict())
    if updated_group:
        return updated_group
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update group",
        )


############################
# DeleteGroupById
############################

@router.delete("/{group_id}", response_model=bool)
async def delete_group_by_id(group_id: int, user=Depends(get_admin_user)):
    result = Groups.delete_group_by_id(group_id)
    if result:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete group",
        )
