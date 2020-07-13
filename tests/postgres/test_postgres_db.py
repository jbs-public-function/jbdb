import os

from unittest import TestCase
import pytest

from db.postgres.postgres_db import PostgresDB
from db.postgres.config.postgres_config import PostgresConfig


class TestPostgresConfig(TestCase):
    def test_postgres_db(self):
        p = PostgresDB()
        self.assertIsInstance(p.db_config, PostgresConfig)
        self.assertIsInstance(p.db_config, p.get_db_config())

        self.assertEqual(p.driver, 'postgresql+psycopg2')
