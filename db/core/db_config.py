import os
import settings


class DBConfig(object):
    db_variables = ['user_name', 'password', 'host', 'port', 'db_name']
    uri = 'postgres+psycopg2://{user_name}:{password}@{host}:{port}/{db_name}'
    
    def __init__(self, **kwargs):
        self.validate_db_variables(list(kwargs.keys()))
        for key, value in kwargs.items():
            setattr(self, key, value)
        
    def to_dict(self, db_variables: list=None):
        if db_variables is None:
            db_variables = self.db_variables
        return {db_variable: getattr(self, db_variable) for db_variable in db_variables}
    
    @property
    def connect_string(self):
        return self.uri.format(**self.to_dict())

    @classmethod
    def validate_db_variables(cls, db_variables):
        validation_variables = cls.db_variables
        validation_variables = [v.lower() for v in validation_variables]
        db_variables = [d.lower() for d in db_variables]
        if len(db_variables) < len(validation_variables):
            raise DBBaseVariablesException(db_variables, validation_variables)

        if any([db_variable not in validation_variables for db_variable in db_variables]):
            raise DBBaseVariablesException(db_variables, validation_variables)

    @classmethod
    def create_db_config(cls, db_variables: list=None):
        if isinstance(db_variables, dict):
            return DBConfig(**db_variables)
        if db_variables is None:
            db_variables = cls.db_variables
        if not isinstance(db_variables, (list, tuple)):
            db_variables = [db_variables]
        return DBConfig(**{db_variable: os.environ.get(db_variable.upper()) for db_variable in db_variables})


class DBBaseVariablesException(Exception):
    def __init__(self, db_variables, validation_keys):
        err = [f"- {db_variable}\n" for db_variable in db_variables if db_variable not in validation_keys]
        err.extend([f"- {db_variable}\n" for db_variable in validation_keys if db_variable not in db_variables])
        self.message = f'The following required variables were missing in the provided validation variables set\n{"".join(err)}'
        super().__init__(self.message)

