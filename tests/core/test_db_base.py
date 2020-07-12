import os

from unittest import TestCase
import pytest
import sqlalchemy

from db.core.db_base import DBBase, DBBaseAttributeException
from db.core.db_config import DBConfig, DBConfigValueError

class TestGamblrDBBase(TestCase):
    def setUp(self):
        self.driver = 'postgres+psycopg2'
        self.user_name = 'test_user_name'
        self.password = 'test_password'
        self.host = 'test_host'
        self.port = '9999'
        self.db_name = 'test_db_name'

        os.environ['USER_NAME'] = self.user_name
        os.environ['PASSWORD'] = self.password
        os.environ['PORT'] = self.port
        os.environ['HOST'] = self.host
        os.environ['DB_NAME'] = self.db_name
        self.os_environ_dict = {key: os.environ.get(key.upper()) for key in ['user_name', 'password', 'host', 'port', 'db_name']}
        self.os_environ_dict.update({'driver': self.driver})

    def test_db_base_instantiation(self):
        test_uri = '{driver}://{user_name}:{password}@{host}:{port}/{db_name}'
        with pytest.raises(DBConfigValueError):
            dbase = DBBase()
        dbase = DBBase(**{'driver': self.driver})
        self.os_environ_dict.update({'driver': self.driver})
        self.assertEqual(dbase.connect_string, test_uri.format(**self.os_environ_dict))
        self.os_environ_dict.pop('driver')

    def test_dbase_engine(self):
        dbase = DBBase(**{'driver': self.driver})
        self.assertTrue(dbase.engine is not None)
        self.assertIsInstance(dbase.engine, sqlalchemy.engine.base.Engine)
        with pytest.raises(DBBaseAttributeException):
            dbase.engine = object()
            dbase.engine = object

    def test_db_base_from_kwargs(self):
        test_uri = '{driver}://{user_name}:{password}@{host}:{port}/{db_name}'
        test_dict = {'driver': self.driver, 'host': 1000}
        dbase = DBBase(**test_dict)
        self.os_environ_dict.update({'host': 1000})
        self.assertTrue(dbase.connect_string, test_uri.format(**self.os_environ_dict))

        os.environ.pop('DB_NAME')
        with pytest.raises(DBConfigValueError):
            dbase = DBBase(**test_dict)
        self.os_environ_dict.update({'db_name': 'new_db_name'})
        test_dict.update({'db_name': 'new_db_name'})
        dbase = DBBase(**test_dict)
        self.assertEqual(dbase.connect_string, test_uri.format(**self.os_environ_dict))
