from pydantic import BaseModel
from typing import Optional


# ----------------------------------------------------
# Schema base - representa a tabela G_SELO_GRUPO
# ----------------------------------------------------
class GSeloGrupoSchema(BaseModel):
    selo_grupo_id: Optional[float] = None
    descricao: Optional[str] = None
    numero: Optional[float] = None
    situacao: Optional[str] = None
    controle_automatico: Optional[str] = None
    sistema_id: Optional[float] = None
    valor: Optional[float] = None
    tipo_cartorio: Optional[str] = None
    descricao_completa: Optional[str] = None
    agrupador: Optional[str] = None
    um_por_protocolo: Optional[str] = None
    numero_principal_ini: Optional[float] = None
    numero_principal_fim: Optional[float] = None
    selo_grupo_id_principal: Optional[float] = None
    envio_automatico: Optional[str] = None
    selo_grupo_id_agrupador: Optional[float] = None
    codigo_conta: Optional[float] = None
    id_tipo_ato_antigo: Optional[float] = None
    grupos_principal: Optional[str] = None
    sigla: Optional[str] = None
    tipo_selo: Optional[str] = None
    natureza: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class GSeloGrupoIdSchema(BaseModel):
    selo_grupo_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class GSeloGrupoSaveSchema(BaseModel):
    selo_grupo_id: Optional[float] = None
    descricao: Optional[str] = None
    numero: Optional[float] = None
    situacao: Optional[str] = None
    controle_automatico: Optional[str] = None
    sistema_id: Optional[float] = None
    valor: Optional[float] = None
    tipo_cartorio: Optional[str] = None
    descricao_completa: Optional[str] = None
    agrupador: Optional[str] = None
    um_por_protocolo: Optional[str] = None
    numero_principal_ini: Optional[float] = None
    numero_principal_fim: Optional[float] = None
    selo_grupo_id_principal: Optional[float] = None
    envio_automatico: Optional[str] = None
    selo_grupo_id_agrupador: Optional[float] = None
    codigo_conta: Optional[float] = None
    id_tipo_ato_antigo: Optional[float] = None
    grupos_principal: Optional[str] = None
    sigla: Optional[str] = None
    tipo_selo: Optional[str] = None
    natureza: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class GSeloGrupoUpdateSchema(GSeloGrupoSaveSchema):
    selo_grupo_id: Optional[float] = None

    class Config:
        from_attributes = True
