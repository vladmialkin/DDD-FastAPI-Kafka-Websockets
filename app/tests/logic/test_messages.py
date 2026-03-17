import pytest
from faker import Faker

from domain.entities.messages import Chat
from domain.values.messages import Title
from infra.repositories.messages import BaseChatRepository
from logic import Mediator, CreateChatCommand
from logic.exceptions.messages import ChatWithThatTitleAlreadyExistsException


@pytest.mark.asyncio
async def test_create_chat_command_success(
        chat_repository: BaseChatRepository,
        mediator: Mediator,
        faker: Faker,
):
    chat: Chat = (await mediator.handle_command(CreateChatCommand(title=faker.text())))[0]

    assert await chat_repository.check_chat_exists_by_title(title=chat.title.as_generic_type())


@pytest.mark.asyncio
async def test_create_chat_command_title_already_exists(
        chat_repository: BaseChatRepository,
        mediator: Mediator,
        faker: Faker,
):
    title_text = faker.text()
    chat = Chat(title=Title(title_text))
    await chat_repository.add_chat(chat)
    with pytest.raises(ChatWithThatTitleAlreadyExistsException):
        await mediator.handle_command(CreateChatCommand(title=title_text))

    assert len(chat_repository._saved_chats) == 1
