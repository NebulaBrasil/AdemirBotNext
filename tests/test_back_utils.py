import pytest
from extensions.back_utils import DataBaseStatus

# Casos de teste
def test_get_database_status_online():
    db_status = DataBaseStatus(None)
    assert db_status.get_database_status() == 'Online'

def test_get_database_status_offline():
    db_status = DataBaseStatus(None)
    assert db_status.get_database_status() == 'Offline'
