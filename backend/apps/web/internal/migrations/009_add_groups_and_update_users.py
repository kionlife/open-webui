"""Peewee migrations -- 009_add_groups_and_update_users.py."""

import peewee as pw
from peewee_migrate import Migrator


def migrate(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your migrations here."""

    # Create Group table
    @migrator.create_model
    class Group(pw.Model):
        id = pw.AutoField()
        name = pw.CharField(max_length=255)
        created_at = pw.BigIntegerField()
        updated_at = pw.BigIntegerField()

        class Meta:
            table_name = "group"

    # Add group_id field to User table
    migrator.add_fields('user', group_id=pw.IntegerField(default=0))


def rollback(migrator: Migrator, database: pw.Database, *, fake=False):
    """Write your rollback migrations here."""

    # Remove group_id field from User table
    migrator.remove_fields('user', 'group_id')

    # Remove Group table
    migrator.remove_model('group')
