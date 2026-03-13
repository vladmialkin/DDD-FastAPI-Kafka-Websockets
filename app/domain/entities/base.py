from dataclasses import dataclass, field
from abc import ABC
from datetime import datetime
from uuid import uuid4


@dataclass(eq=False)
class BaseEntity(ABC):
    oid: str = field(default_factory=lambda: str(uuid4()), kw_only=True)
    created_at: datetime = field(default_factory=datetime.now, kw_only=True)

    def __hash__(self):
        return hash(self.oid)

    def __eq__(self, __value: 'BaseEntity'):
        return self.oid == __value.oid
