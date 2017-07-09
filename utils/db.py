import peewee

from utils.funcs import get_project_settings


def DataBaseConnection():
    settings = get_project_settings()
    db_settings = settings.get("DATABASE")
    if db_settings is None:
        raise ValueError("DATABASE is not set")
    db_params = db_settings.get("params")
    db_engine = db_settings.get("engine")
    if db_engine.lower() == "sqlite":
        db = peewee.SqliteDatabase(**db_params)
    elif db_engine.lower() == "mysql":
        db = peewee.MySQLDatabase(**db_params)
    elif db_engine.lower() == "postgresql":
        db = peewee.PostgresqlDatabase(**db_params)
    else:
        raise ValueError("DATABASE engine is not supported")
    return db


