import peewee

# TODO remove this hack
from utils import model


class IPTask(model.BaseModel):
    start_ip = peewee.CharField(max_length=50, unique=True)
    t_range = peewee.IntegerField()
    last_test_date = peewee.DateTimeField(null=True, default=None)


class PreProxy(model.BaseModel):
    ip = peewee.CharField(max_length=50)
    port = peewee.IntegerField()
    location = peewee.TextField(null=True)

    last_test_date = peewee.DateTimeField(null=True, default=None)
    is_ok = peewee.BooleanField(null=True, default=None)

    class Meta:
        indexes = (
            (("ip", "port"), True),
        )
