import os

from unittest import TestCase
import pytest

from db.postgres.config.postgres_config import PostgresConfig
from db.core.db_config_base import DBConfigAttributeError

class TestPostgresConfig(TestCase):
    def setUp(self):
        self.test_connect_string = 'postgresql+psycopg2://usr:pass@localhost:5400/db_name'
        self.driver = 'postgresql+psycopg2'

        os.environ['USER_NAME'] = 'usr'
        os.environ['PASSWORD'] = 'pass'
        os.environ['HOST'] = 'localhost'
        os.environ['PORT'] = '5400'
        os.environ['DB_NAME'] = 'db_name'

    def test_postgres_config(self):
        with pytest.raises(DBConfigAttributeError):
            PostgresConfig()
        p = PostgresConfig(**{'driver': self.driver})
        self.assertEqual(p.connect_string, self.test_connect_string)

        os.environ.pop('PASSWORD')
        with pytest.raises(DBConfigAttributeError):
            PostgresConfig(**{'driver': self.driver})
