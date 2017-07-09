import peewee
from datetime import datetime

from utils.db import DataBaseConnection


class BaseModel(peewee.Model):
    create_date = peewee.DateTimeField(default=datetime.now)
    modify_date = peewee.DateTimeField()

    def save(self, force_insert=False, only=None):
        self.modify_date = datetime.now()
        super(BaseModel, self).save(force_insert=force_insert, only=only)

    class Meta:
        database = DataBaseConnection()
