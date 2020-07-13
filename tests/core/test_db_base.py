import os

from unittest import TestCase, mock
import pytest
import sqlalchemy

from db.core.db_base import DBBase, DBBaseAttributeException
from db.core.db_config_base import DBConfigBase, DBConfigValueError, DBConfigAttributeError

class TestDBBase(TestCase):
    def setUp(self):
        self.test_connect_string = 'postgresql+psycopg2://usr:pass@localhost:5400/db_name'
        self.connect_string = DBConfigBase.connect_string
        self.p = mock.PropertyMock(return_value=self.test_connect_string)
        DBConfigBase.connect_string = self.p

    def tearDown(self):
        DBConfigBase.connect_string = self.connect_string

    def test_db_base_init(self):
        db = DBBase(**{'driver': 'test_driver'})
        self.assertEqual(db.db_config.driver, 'test_driver')

        db = DBBase()
        self.assertEqual(db.db_config.driver, 'base_driver')

    def test_db_base_init_db_config(self):
        db = DBBase(**{'driver': None})
        self.assertEqual(db.db_config.driver, 'base_driver')

        db = DBBase(**{'driver': 'test_driver', 'extra_slot': 'extra-slot'})
        self.assertFalse(hasattr(db.db_config, 'extra_slot'))
        self.assertEqual(db.db_config.driver, 'test_driver')

    def test_db_base_load_db_config(self):
        config = DBBase.load_db_config()
        db = DBBase()
        self.assertIsInstance(config, DBBase.get_db_config())
        self.assertEqual(config.driver, db.db_config.driver)

        config = DBBase.load_db_config(**{'driver': 'overwrite-driver'})
        db = DBBase(**{'driver': 'overwrite-driver'})
        self.assertNotEqual(config.driver, DBBase.driver)
        self.assertEqual(db.db_config.driver, config.driver)
        self.assertEqual(db.db_config.driver, 'overwrite-driver')

    def test_db_base_engine(self):
        db = DBBase()
        self.assertIsInstance(db.engine, sqlalchemy.engine.base.Engine)
        self.assertEqual(db.engine, db.engine)
        self.assertEqual(db.engine, db._engine)
        self.assertEqual(self.p.call_count, 1)
        
        with pytest.raises(DBBaseAttributeException):
            db.engine = object

        db_engine = DBBase.create_engine()
        with pytest.raises(DBBaseAttributeException):
            db.engine = db_engine

        db_engine = db.engine
        engine = sqlalchemy.create_engine(self.test_connect_string)
        self.assertNotEqual(db_engine, engine)

        db_engine = DBBase.create_engine()(self.test_connect_string)
        self.assertIsInstance(db_engine, sqlalchemy.engine.base.Engine)
