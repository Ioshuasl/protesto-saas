from pydantic import BaseModel
from typing import Optional

# ----------------------------------------------------
# Schema base - representa a tabela T_CENSEC_TIPOATO
# ----------------------------------------------------
class TCensecTipoAtoSchema(BaseModel):
    censec_tipoato_id: Optional[float] = None
    censec_id: Optional[float] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    tipo_separacao: Optional[str] = None
    tipo_revogacao: Optional[str] = None
    codigo: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema de indexação/listagem (ex: GET /index)
# ----------------------------------------------------
class TCensecTipoAtoIndexSchema(BaseModel):
    censec_tipoato_id: float
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TCensecTipoAtoIdSchema(BaseModel):
    censec_tipoato_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TCensecTipoAtoSaveSchema(BaseModel):
    censec_tipoato_id: Optional[float] = None
    censec_id: Optional[float] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    tipo_separacao: Optional[str] = None
    tipo_revogacao: Optional[str] = None
    codigo: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TCensecTipoAtoUpdateSchema(BaseModel):
    censec_tipoato_id: Optional[float] = None
    censec_id: Optional[float] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    tipo_separacao: Optional[str] = None
    tipo_revogacao: Optional[str] = None
    codigo: Optional[float] = None

    class Config:
        from_attributes = True