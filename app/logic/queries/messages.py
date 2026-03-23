from dataclasses import dataclass
from typing import Iterable

from domain.entities.messages import Chat, Message
from infra.repositories.filters.messages import GetMessagesFilters
from infra.repositories.messages.base import BaseChatsRepository, BaseMessagesRepository
from logic.exceptions.messages import ChatNotFoundException
from logic.queries.base import BaseQuery, BaseQueryHandler, QT, QR


@dataclass(frozen=True)
class GetChatDetailQuery(BaseQuery):
    chat_oid: str


@dataclass(frozen=True)
class GetMessagesQuery(BaseQuery):
    chat_oid: str
    filters: GetMessagesFilters


@dataclass(frozen=True)
class GetChatDetailQueryHandler(BaseQueryHandler):
    chats_repository: BaseChatsRepository
    messages_repository: BaseMessagesRepository

    async def handler(self, query: GetChatDetailQuery) -> Chat:
        chat = await self.chats_repository.get_chat_by_oid(oid=query.chat_oid)

        print(1111111111111111111111111111111111111111111111111111111111)
        print(1111111111111111111111111111111111111111111111111111111111)
        print(1111111111111111111111111111111111111111111111111111111111)
        print(1111111111111111111111111111111111111111111111111111111111)

        if not chat:
            raise ChatNotFoundException(chat_oid=query.chat_oid)

        return chat


@dataclass(frozen=True)
class GetMessagesQueryHandler(BaseQueryHandler):
    messages_repository: BaseMessagesRepository

    async def handler(self, query: GetMessagesQuery) -> Iterable[Message]:
        return await self.messages_repository.get_messages(chat_oid=query.chat_oid, filters=query.filters)
