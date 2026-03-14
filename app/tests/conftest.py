from pytest import fixture

from infra.repositories.messages import BaseChatRepository, MemoryChatRepository
from logic import Mediator, init_mediator


@fixture(scope="package")
def chat_repository():
    return MemoryChatRepository()


@fixture(scope="package")
def mediator(chat_repository: BaseChatRepository) -> Mediator:
    mediator = Mediator()
    init_mediator(mediator, chat_repository=chat_repository)

    return mediator
