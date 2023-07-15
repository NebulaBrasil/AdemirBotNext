import asyncio
import unittest
from unittest.mock import MagicMock, AsyncMock, Mock
from interactions import Client, Guild, SlashContext, ModalContext
from extensions.member_manage import MemberManage
from utils.async_test import async_test

class TestMemberManage(unittest.TestCase):
    def setUp(self):
        self.client = Client()
        self.extension = MemberManage(self.client)

    def test_split_and_parse_member_ids(self):
        member_ids = "123\n456\n789"
        expected_result = [123, 456, 789]
        result = self.extension.split_and_parse_member_ids(member_ids)
        self.assertEqual(result, expected_result)

    @async_test
    async def test_ban_members(self):
        guild = Guild(client=self.client, id=123123, owner_id=123123, name='fake', preferred_locale='pt-BR')
        member_ids = [123, 456, 789]
        guild.fetch_member = AsyncMock(return_value=MagicMock(return_value=[123, 456, 789]))
        guild.ban = AsyncMock()
        await self.extension.ban_members(guild, member_ids)
        self.assertEqual(guild.fetch_member.call_count, 3)
        self.assertEqual(guild.ban.call_count, len(member_ids))

    @async_test
    async def test_kick_members(self):
        guild = Guild(client=self.client, id=123123, owner_id=123123, name='fake', preferred_locale='pt-BR')
        member_ids = [123, 456, 789]

        guild.fetch_member = AsyncMock(return_value=MagicMock())
        guild.kick = AsyncMock()

        await self.extension.kick_members(guild, member_ids)
        self.assertEqual(guild.fetch_member.call_count, len(member_ids))
        self.assertEqual(guild.kick.call_count, len(member_ids))
      
if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMemberManage)
    asyncio.run(suite)