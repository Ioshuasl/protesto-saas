from typing import Optional
from pydantic.main import BaseModel
from pydantic.v1.config import Extra


class DOCXSchemaCallback(BaseModel):

    registro_id: Optional[int] = None
    servico: Optional[str] = None
    data: Optional[object] = None

    class Config:
        extra = Extra.allow
