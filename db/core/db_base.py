import sqlalchemy

from db.core.db_config import DBConfig


class DBBase(DBConfig):
    def __init__(self, **db_config):
        self._engine = None
        super().__init__(**db_config)

    @property
    def engine(self):
        if self._engine is None:
            self._engine = sqlalchemy.create_engine(self.connect_string)
        return self._engine

    @engine.setter
    def engine(self, engine:sqlalchemy.engine.base.Engine):
        self._engine = self.validate_engine(engine)
    
    @classmethod
    def validate_engine(cls, engine: sqlalchemy.engine.base.Engine):
        if not isinstance(engine, sqlalchemy.engine.base.Engine):
            m = f'Invalid engine object of type ({engine.__class__}). Engine must be of type sqlalchemy.engine.base.Engine'
            raise DBBaseAttributeException(m)
        return engine


class DBBaseAttributeException(AttributeError):
    pass
