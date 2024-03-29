import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


class DBCredentials:
    USER_NAME = os.environ["USER_NAME"]
    PASSWORD = os.environ["PASSWORD"]
    HOST = os.environ["HOST"]
    PORT = os.environ["PORT"] or 5432
    DATABASE = os.environ["DATABASE"]


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class DBConfig(metaclass=Singleton):
    session = None

    def __init__(self):
        self.URL = "postgresql+psycopg2://{}:{}@{}:{}/{}".format(
            DBCredentials.USER_NAME, DBCredentials.PASSWORD, DBCredentials.HOST, DBCredentials.PORT,
            DBCredentials.DATABASE
        )
        self.engine = create_engine(self.URL)
        self.engine.connect()
        self.session = sessionmaker(bind=self.engine)()

    def connection(self):
        return self.session


def test_list_table_names():
    session = DBConfig().connection()

    for x in session.execute(text('SELECT * FROM "pg_catalog"."pg_tables" ')).all():
        print(x)
        assert x is not None
