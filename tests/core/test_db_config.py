import os

from unittest import TestCase
import pytest

from db.core.db_config import DBConfig, DBBaseVariablesException


class TestGamblrDBConfig(TestCase):
    def setUp(self):
        self.user_name = 'test_user_name'
        self.password = 'test_password'
        self.host = 'test_host'
        self.port = 'test_port'
        self.db_name = 'test_db_name'

        os.environ['USER_NAME'] = self.user_name
        os.environ['PASSWORD'] = self.password
        os.environ['PORT'] = self.port
        os.environ['HOST'] = self.host
        os.environ['DB_NAME'] = self.db_name

        self.test_uri = f'postgres+psycopg2://{self.user_name}:{self.password}@{self.host}:{self.port}/{self.db_name}'
        self.instance_dict = dict(zip(DBConfig.db_variables, [self.user_name, self.password, self.host, self.port, self.db_name]))

    def test_db_config_instantiation(self):
        db_config1 = DBConfig(**self.instance_dict)
        db_config2 = DBConfig.create_db_config()
        db_config3 = DBConfig.create_db_config(list(self.instance_dict.keys()))
        db_config4 = DBConfig.create_db_config(self.instance_dict)

        self.assertSetEqual({os.environ.get(db_variable.upper()) for db_variable in db_config1.db_variables}, set(db_config1.to_dict().values()))
        for db_variable in DBConfig.db_variables:
            self.assertEqual(getattr(db_config1, db_variable), os.environ.get(db_variable.upper()))
            self.assertEqual(getattr(db_config1, db_variable), getattr(db_config2, db_variable))
            self.assertEqual(getattr(db_config2, db_variable), getattr(db_config3, db_variable))
            self.assertEqual(getattr(db_config3, db_variable), getattr(db_config4, db_variable))
        self.assertEqual(self.test_uri, db_config1.connect_string)
        self.assertEqual(self.test_uri, db_config2.connect_string)
        self.assertEqual(self.test_uri, db_config3.connect_string)
        self.assertEqual(self.test_uri, db_config4.connect_string)

    def test_db_config_exceptions(self):
        self.instance_dict.pop('user_name')
        os.environ.pop('HOST')
        with pytest.raises(DBBaseVariablesException):
            db_config1 = DBConfig(**self.instance_dict)
            db_config2 = DBConfig.create_db_config()
            db_config3 = DBConfig.create_db_config(list(self.instance_dict.keys()))
            db_config4 = DBConfig.create_db_config(self.instance_dict)

    def test_db_validate_variables(self):
        db_config = DBConfig
        db_config.db_variables = ['a', 'b', 'c', 'd', 'e']
        t1 = ['a', 'b', 'c', 'e', 'd']
        t2 = ['a', 'c', 'e', 'd']
        t3 = ['a', 'e', 'd']
        t4 = ['a', 'b', 'c', 'd', 'e', 'q', 'r']
        db_config.validate_db_variables(t1)

        with pytest.raises(DBBaseVariablesException):
            db_config.validate_db_variables(t1)
            db_config.validate_db_variables(t2)
            db_config.validate_db_variables(t3)
            db_config.validate_db_variables(t4)

        db_config.db_variables = ['a', 'b', 'c', 'd', 'e', 'q', 'r']
        db_config.validate_db_variables(t4)

    def test_db_to_dict(self):
        db_config = DBConfig(**self.instance_dict)
        self.assertDictEqual(db_config.to_dict(), self.instance_dict)
