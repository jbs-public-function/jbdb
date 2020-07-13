import os

from unittest import TestCase
import pytest
import sqlalchemy

from db.core.db_config_base import DBConfigBase, DBConfigValueError, DBConfigAttributeError

class TestDBConfigBase(TestCase):
    def test_db_config_init(self):
        with pytest.raises(DBConfigAttributeError):
            DBConfigBase()

        with pytest.raises(DBConfigValueError):
            DBConfigBase(**{'driver': None})
        
        config = DBConfigBase(**{'driver': 'test_driver', 'extra_slot': 'extra_slot'})
        self.assertFalse(hasattr(config, 'extra_slot'))

        config = DBConfigBase(**{'driver': 'test_driver'})
        self.assertEqual('test_driver', config.driver)
        self.assertEqual(config.driver, config.connect_string)

    def test_db_config_validate_slot_values(self):
        class Test1():
            def __init__(self):
                self.driver = None

        with pytest.raises(DBConfigValueError):
            DBConfigBase.validate_slot_values(Test1())

        class Test2():
            def __init__(self):
                self.driver = 'driver'
        DBConfigBase.validate_slot_values(Test2())

        class Test3():
            def __init__(self):
                self.extra_slot = 'extra_slot'
        DBConfigBase.validate_slot_values(Test2())

    def test_db_config_validate_slot_attributes(self):
        config = {'driver': None}
        DBConfigBase.validate_slot_attributes(config)

        config = {'driver': None, 'extra_slot': 'extra-slot'}
        DBConfigBase.validate_slot_attributes(config)

        config = {}
        with pytest.raises(DBConfigAttributeError):
            DBConfigBase.validate_slot_attributes(config)

    def test_db_config_connection_str(self):
        config = DBConfigBase(**{'driver': 'test-driver'})
        self.assertEqual(config.connect_string, 'test-driver')
