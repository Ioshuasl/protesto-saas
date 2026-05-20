from pydantic import BaseModel, field_validator
from typing import List, Optional, Union


# ----------------------------------------------------
# Schema base - representa a tabela T_CENSEC_TIPONATUREZA
# ----------------------------------------------------
class TCensecTipoNaturezaSchema(BaseModel):
    censec_tiponatureza_id: Optional[float] = None
    censec_tipoato_id: Optional[float] = None
    descricao: Optional[str] = None
    possui_ato_anterior: Optional[str] = None
    codigo: Optional[float] = None
    obrigatorio: Optional[str] = None
    tipo_ato_anterior: Optional[str] = None
    situacao_ato_anterior: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema de indexação/listagem (ex: GET /index)
# ----------------------------------------------------
class TCensecTipoNaturezaIndexSchema(BaseModel):
    censec_tiponatureza_id: Optional[float] = None
    censec_tipoato_id: Optional[float] = None
    descricao: Optional[str] = None
    possui_ato_anterior: Optional[str] = None
    codigo: Optional[float] = None
    obrigatorio: Optional[str] = None
    tipo_ato_anterior: Optional[str] = None
    situacao_ato_anterior: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TCensecTipoNaturezaIdSchema(BaseModel):
    censec_tiponatureza_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TCensecTipoNaturezaSaveSchema(BaseModel):
    censec_tiponatureza_id: Optional[float] = None
    censec_tipoato_id: Optional[float] = None
    descricao: Optional[str] = None
    possui_ato_anterior: Optional[str] = None
    codigo: Optional[float] = None
    obrigatorio: Optional[str] = None
    tipo_ato_anterior: Optional[Union[List[float], str]] = None  # aceita lista OU string
    situacao_ato_anterior: Optional[str] = None

    @field_validator("tipo_ato_anterior", mode="before")
    def convert_list_to_str(cls, v):
        """
        Converte lista [0,1,2,3] em string ";0,1,2,3"
        """
        if isinstance(v, list):
            # Converte para ";0,1,2,3"
            return ";" + ",".join(str(int(x)) for x in v)
        return v

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TCensecTipoNaturezaUpdateSchema(BaseModel):
    censec_tiponatureza_id: Optional[float] = None
    censec_tipoato_id: Optional[float] = None
    descricao: Optional[str] = None
    possui_ato_anterior: Optional[str] = None
    codigo: Optional[float] = None
    obrigatorio: Optional[str] = None
    tipo_ato_anterior: Optional[Union[List[float], str]] = None  # aceita lista OU string
    situacao_ato_anterior: Optional[str] = None

    @field_validator("tipo_ato_anterior", mode="before")
    def convert_list_to_str(cls, v):
        """
        Converte lista [0,1,2,3] em string ";0,1,2,3"
        """
        if isinstance(v, list):
            # Converte para ";0,1,2,3"
            return ";" + ",".join(str(int(x)) for x in v)
        return v

    class Config:
        from_attributes = True
