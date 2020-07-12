import os

from unittest import TestCase
import pytest

from db.core.db_base import DBBase, DBConfig, DBBaseVariablesException, DBBaseAttributeException


class TestGamblrDBBase(TestCase):
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


    def test_db_base_instantiation(self):
        dbase = DBBase(None, None)
        self.assertEqual(dbase.db_config.db_variables, DBBase.db_variables)
        with pytest.raises(DBBaseAttributeException):
            dbase.engine = object()
            DBBase(object(), None)
            dbase.db_config = object()

        dbase.db_config = dbase.db_config
        self.assertIsInstance(dbase.db_config, DBConfig)

        with pytest.raises(DBBaseVariablesException):
            dbase = DBBase(None, ['x', 'y', 'z'])
        