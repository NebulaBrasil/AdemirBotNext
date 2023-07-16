import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import asyncio
from interactions import Client
from extensions.back_utils import DataBaseStatus

@pytest.fixture
def client():
    return Client()

def test_get_database_status_online(client):
    with patch('pymongo.MongoClient') as mock_client:
        mock_db = MagicMock()
        mock_db.command.return_value = {'ok': 1}

        mock_client.return_value = mock_db

        db_status = DataBaseStatus(client)
        status = db_status.get_database_status()

        assert status == 'Online'

def test_get_database_status_offline(client):
    with patch('pymongo.MongoClient') as mock_client:
        mock_client.side_effect = Exception('connection failed')

        db_status = DataBaseStatus(client)
        status = db_status.get_database_status()

        assert status == 'Offline'

@pytest.mark.asyncio
async def test_dbstatus_command(client):
    db_status = DataBaseStatus(client)

    mock_get_database_status = AsyncMock(return_value='Online')
    db_status.get_database_status = mock_get_database_status

    ctx = AsyncMock()

    await asyncio.gather(db_status.dbstatus(ctx))

    mock_get_database_status()
    mock_get_database_status.assert_called_once()
    ctx.send.assert_called_with('Database: **Online**')