import sqlalchemy

from db.core.db_config import DBConfig, DBBaseVariablesException


class DBBase(DBConfig):
    def __init__(self, engine=None, db_config_variables=None):
        self._engine = engine
        self._db_config = self.create_db_config(db_config_variables)

    @property
    def engine(self):
        if self._engine is None:
            self._engine = sqlalchemy.create_engine(self.db_config.connect_string)
        if not isinstance(self._engine, sqlalchemy.engine.base.Engine):
            m = f'Invalid engine object of type ({engine.__class__}). Engine must be of type sqlalchemy.engine.base.Engine'
            raise DBBaseAttributeException(m)
        return self._engine

    @engine.setter
    def engine(self, engine:sqlalchemy.engine.base.Engine):
        if not isinstance(engine, sqlalchemy.engine.base.Engine):
            m = f'Invalid engine object of type ({engine.__class__}). Engine must be of type sqlalchemy.engine.base.Engine'
            raise DBBaseAttributeException(m)
        self._engine = engine

    @property
    def db_config(self):
        return self._db_config
    
    @db_config.setter 
    def db_config(self, db_config: DBConfig):
        if not isinstance(db_config, DBConfig):
            m = f'Invalid config object of type ({DBConfig.__class__}). Engine must be of type db.core.db_config'
            raise DBBaseAttributeException(m)
        self._db_config = db_config


class DBBaseAttributeException(AttributeError):
    pass
