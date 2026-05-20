# ----------------------------------------------------
# Schema base - representa a tabela de Biometria
# ----------------------------------------------------
from typing import Any, List
from pydantic.main import BaseModel


class ControllerResponseSchema(BaseModel):
    message: str = None
    data: List[Any]

    class Config:
        from_attributes = True
