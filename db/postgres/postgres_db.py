from db.core.db_base import DBBase


class PostgresDB(DBBase):
    driver = 'postgresql+psycopg2'
    
    @classmethod
    def get_db_config(cls):
        from db.postgres.config.postgres_config import PostgresConfig
        return PostgresConfig
