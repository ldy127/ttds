from db.MongoDB import MongoDB
from db.DBInterface import DBInterface


def get_db_instance() -> DBInterface:
    return MongoDB()


