from pydantic import BaseModel
from typing import Optional


# ----------------------------------------------------
# Schema base - representa a tabela G_GRAMATICA
# ----------------------------------------------------
class GGramaticaSchema(BaseModel):
    gramatica_id: Optional[float] = None
    palavra: Optional[str] = None
    prefixo: Optional[str] = None
    sufixo_ms: Optional[str] = None
    sufixo_mp: Optional[str] = None
    sufixo_fs: Optional[str] = None
    sufixo_fp: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class GGramaticaIdSchema(BaseModel):
    gramatica_id: float

    class Config:
        from_attributes = True


class GGramaticaPalavraSchema(BaseModel):
    palavra: str

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class GGramaticaSaveSchema(BaseModel):
    gramatica_id: Optional[float] = None
    palavra: Optional[str] = None
    prefixo: Optional[str] = None
    sufixo_ms: Optional[str] = None
    sufixo_mp: Optional[str] = None
    sufixo_fs: Optional[str] = None
    sufixo_fp: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class GGramaticaUpdateSchema(BaseModel):
    gramatica_id: Optional[float] = None
    palavra: Optional[str] = None
    prefixo: Optional[str] = None
    sufixo_ms: Optional[str] = None
    sufixo_mp: Optional[str] = None
    sufixo_fs: Optional[str] = None
    sufixo_fp: Optional[str] = None

    class Config:
        from_attributes = True
