from typing import Optional

from pydantic import BaseModel


class GSequenciaSchema(BaseModel):
    tabela: Optional[str] = None
    sequencia: Optional[int] = None
    contador: Optional[bool] = False

    class Config:
        from_attributes = True


# Schema para retornar o id da sequencia
class GSequenciaDeleteSchema(BaseModel):
    tabela: Optional[str] = None
    sequencia: Optional[int] = None
    contador: Optional[bool] = False

    class Config:
        from_attributes = True