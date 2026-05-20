from pydantic import BaseModel
from typing import Optional


# ----------------------------------------------------
# Schema base - representa a tabela T_CENSEC_QUALIDADEATO
# ----------------------------------------------------
class TCensecQualidadeAtoSchema(BaseModel):
    censec_qualidadeato_id: Optional[float] = None
    censec_tipoato_id: Optional[float] = None
    censec_qualidade_id: Optional[float] = None
    qtd_minima: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema de indexação/listagem (ex: GET /index)
# ----------------------------------------------------
class TCensecQualidadeAtoIndexSchema(BaseModel):
    censec_qualidadeato_id: Optional[float] = None
    censec_tipoato_id: Optional[float] = None
    censec_qualidade_id: Optional[float] = None
    qtd_minima: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TCensecQualidadeAtoIdSchema(BaseModel):
    censec_qualidadeato_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TCensecQualidadeAtoSaveSchema(BaseModel):
    censec_qualidadeato_id: Optional[float] = None
    censec_tipoato_id: Optional[float] = None
    censec_qualidade_id: Optional[float] = None
    qtd_minima: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TCensecQualidadeAtoUpdateSchema(BaseModel):
    censec_qualidadeato_id: Optional[float] = None
    censec_tipoato_id: Optional[float] = None
    censec_qualidade_id: Optional[float] = None
    qtd_minima: Optional[float] = None

    class Config:
        from_attributes = True