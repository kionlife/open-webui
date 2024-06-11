from pydantic import BaseModel
from peewee import *
from playhouse.shortcuts import model_to_dict

from apps.web.internal.db import DB
from typing import List, Optional
import time

####################
# Group DB Schema
####################

class Group(Model):
    id = AutoField()
    name = CharField(unique=True)
    created_at = BigIntegerField()
    updated_at = BigIntegerField()

    class Meta:
        table_name = "group"
        database = DB

class GroupModel(BaseModel):
    id: int
    name: str
    created_at: int
    updated_at: int

class GroupsTable:
    def __init__(self, db):
        self.db = db
        self.db.create_tables([Group])

    def insert_new_group(self, name: str) -> Optional[GroupModel]:
        created_at = int(time.time())
        updated_at = created_at
        group = Group.create(name=name, created_at=created_at, updated_at=updated_at)
        return GroupModel(
            id=group.id,
            name=group.name,
            created_at=group.created_at,
            updated_at=group.updated_at
        )

    def get_group_by_id(self, id: int) -> Optional[GroupModel]:
        try:
            group = Group.get(Group.id == id)
            return GroupModel(**model_to_dict(group))
        except:
            return None

    def get_groups(self, skip: int = 0, limit: int = 50) -> List[GroupModel]:
        groups = Group.select().limit(limit).offset(skip)
        return [
            GroupModel(
                id=group.id,
                name=group.name,
                created_at=group.created_at,
                updated_at=group.updated_at
            )
            for group in groups
        ]

    def update_group_by_id(self, id: int, updated: dict) -> Optional[GroupModel]:
        try:
            query = Group.update(**updated).where(Group.id == id)
            query.execute()

            group = Group.get(Group.id == id)
            return GroupModel(**model_to_dict(group))
        except:
            return None

    def delete_group_by_id(self, id: int) -> bool:
        try:
            query = Group.delete().where(Group.id == id)
            query.execute()  # Remove the rows, return number of rows removed.
            return True
        except:
            return False

Groups = GroupsTable(DB)
