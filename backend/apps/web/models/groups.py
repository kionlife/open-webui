from pydantic import BaseModel
from peewee import *
from playhouse.shortcuts import model_to_dict
from typing import List, Union, Optional
import time
from utils.misc import get_gravatar_url

from apps.web.internal.db import DB
from apps.web.models.chats import Chats

####################
# Group DB Schema
####################


class Group(Model):
    id = CharField(unique=True)
    name = CharField()

    updated_at = BigIntegerField()
    created_at = BigIntegerField()

    class Meta:
        database = DB

class GroupModel(BaseModel):
    id: str
    name: str

    updated_at: int  # timestamp in epoch
    created_at: int  # timestamp in epoch

####################
# Forms
####################


class GroupUpdateForm(BaseModel):
    name: str

class GroupsTable:
    def __init__(self, db):
        self.db = db
        self.db.create_tables([Group])

    def insert_new_group(
        self,
        id: str,
        name: str,
    ) -> Optional[GroupModel]:
        group = GroupModel(
            **{
                "id": id,
                "name": name,
                "created_at": int(time.time()),
                "updated_at": int(time.time()),
            }
        )
        result = Group.create(**group.model_dump())
        if result:
            return group
        else:
            return None

    def get_group_by_id(self, id: str) -> Optional[GroupModel]:
        try:
            group = Group.get(Group.id == id)
            return GroupModel(**model_to_dict(group))
        except:
            return None

    def get_groups(self, skip: int = 0, limit: int = 50) -> List[GroupModel]:
        return [
            GroupModel(**model_to_dict(group))
            for group in Group.select()
            # .limit(limit).offset(skip)
        ]

    def get_num_groups(self) -> Optional[int]:
        return Group.select().count()

    def get_first_group(self) -> GroupModel:
        try:
            group = Group.select().order_by(Group.created_at).first()
            return GroupModel(**model_to_dict(group))
        except:
            return None


    def update_group_by_id(self, id: str, updated: dict) -> Optional[GroupModel]:
        try:
            query = Group.update(**updated).where(Group.id == id)
            query.execute()

            group = Group.get(Group.id == id)
            return GroupModel(**model_to_dict(group))
        except:
            return None

    def delete_group_by_id(self, id: str) -> bool:
        try:
            # Delete Group Chats
            result = Chats.delete_chats_by_group_id(id)

            if result:
                # Delete Group
                query = Group.delete().where(Group.id == id)
                query.execute()  # Remove the rows, return number of rows removed.

                return True
            else:
                return False
        except:
            return False


Groups = GroupsTable(DB)
