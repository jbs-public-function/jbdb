from functools import partial
import sqlalchemy


class DBBase(object):
    driver = 'base_driver'
    __slots__ = ['_engine', 'db_config']

    def __init__(self, **config):
        self._engine = self.create_engine()
        self.db_config = self.load_db_config(**config)

    @property
    def engine(self):
        if hasattr(self._engine, '__call__'):
            self._engine = self._engine(self.db_config.connect_string)
        return self._engine

    @engine.setter
    def engine(self, engine:sqlalchemy.engine.base.Engine):
        self._engine = self.validate_engine(engine)
    
    @classmethod
    def create_engine(cls):
        return partial(sqlalchemy.create_engine)

    @classmethod
    def get_db_config(cls):
        from db.core.db_config_base import DBConfigBase
        return DBConfigBase

    @classmethod
    def validate_engine(cls, engine: sqlalchemy.engine.base.Engine):
        if not isinstance(engine, sqlalchemy.engine.base.Engine):
            m = f'Invalid engine object of type ({engine.__class__}). Engine must be of type sqlalchemy.engine.base.Engine'
            raise DBBaseAttributeException(m)
        return engine

    @classmethod
    def load_db_config(cls, **config):
        db_config = cls.get_db_config()
        if config.get('driver') is None:
            config.update({'driver': cls.driver})
        return db_config(**config)


class DBBaseAttributeException(AttributeError):
    pass
