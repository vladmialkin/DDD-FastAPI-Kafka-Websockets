from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Any, Generic


@dataclass(frozen=True)
class BaseQuery(ABC):
    ...


QT = TypeVar("QT", bound=BaseQuery)
QR = TypeVar("QR", bound=Any)


@dataclass(frozen=True)
class BaseQueryHandler(BaseQuery, Generic[QT, QR]):
    @abstractmethod
    async def handler(self, command: QT) -> QR:
        ...
