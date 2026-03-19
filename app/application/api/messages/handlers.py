from fastapi import status, Depends
from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from punq import Container

from application.api.dependencies.containers import container
from application.api.messages.schemas import (
    CreateChatRequestSchema,
    CreateChatResponseSchema, CreateMessageRequestSchema, CreateMessageResponseSchema,
)
from application.api.schemas import ErrorSchema
from domain.exceptions.base import ApplicationException
from logic import Mediator, CreateChatCommand, init_container
from logic.commands.messages import CreateMessageCommand

router = APIRouter(tags=["Chat"])


@router.post(
    "/",
    response_model=CreateChatResponseSchema,
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт  создает новый чат, если чат с таким названием существует, то возвращается 400 ошибка.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateChatResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
)
async def create_chat_handler(
        schema: CreateChatRequestSchema,
        container: Container = Depends(init_container)
) -> CreateChatResponseSchema:
    """Создать новый чат"""
    mediator = container.resolve(Mediator)
    try:
        chat, *_ = await mediator.handle_command(CreateChatCommand(title=schema.title))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={"error": exception.message}
        )

    return CreateChatResponseSchema.from_entity(chat)


@router.post(
    '/{chat_oid}/messages',
    status_code=status.HTTP_201_CREATED,
    description="Эндпоинт на добавление нового сообщения в чат с переданным ObjectID.",
    responses={
        status.HTTP_201_CREATED: {"model": CreateMessageRequestSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    }
)
async def create_message_handler(
        chat_oid: str,
        schema: CreateMessageRequestSchema,
        container: Container = Depends((init_container))
) -> CreateMessageResponseSchema:
    """ Добавить новое сообщение в чат """
    mediator = container.resolve(Mediator)
    try:
        message, *_ = await mediator.handle_command(CreateMessageCommand(text=schema.text, chat_oid=chat_oid))
    except ApplicationException as exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail={'error': exception.message}
        )
    return CreateMessageResponseSchema.from_entity(message)
