from db.core.db_config_base import DBConfigBase


class PostgresConfig(DBConfigBase):
    __slots__ = DBConfigBase.__slots__ + ['user_name', 'password', 'host', 'port', 'db_name']
    db_uri = DBConfigBase.db_uri + '://{user_name}:{password}@{host}:{port}/{db_name}'
