import pytest

from domain.entities.messages import Chat
from infra.repositories.messages import BaseChatRepository
from logic import Mediator, CreateChatCommand


@pytest.mark.asyncio
async def test_create_chat_command_success(
    chat_repository: BaseChatRepository,
    mediator: Mediator,
):
    # TODO: Добавить фейкер для генерации рандомных текстов
    chat: Chat = (await mediator.handle_command(CreateChatCommand(title="TestTitle")))[0]

    assert await chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type())
