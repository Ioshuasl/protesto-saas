from typing import Any, List
from pydantic.main import BaseModel


class EndpointResponseSchema(BaseModel):
    message: str = None
    data: List[Any]

    class Config:
        from_attributes = True
