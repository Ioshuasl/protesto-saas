from pydantic import BaseModel
from typing import Optional


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GMarcacaoTipoSchema(BaseModel):
    marcacao_tipo_id: Optional[int] = None  # NUMERIC(10,2) PK
    descricao: Optional[str] = None  # VARCHAR(120)
    texto: Optional[bytes] = None
    nome: Optional[str] = None  # VARCHAR(30)
    grupo: Optional[str] = None  # VARCHAR(30)
    situacao: Optional[str] = None  # VARCHAR(1)
    sistema_id: Optional[int] = None  # NUMERIC(10,2)
    grupo_tipo: Optional[str] = None  # VARCHAR(1)
    tipo_qualificacao: Optional[str] = None  # VARCHAR(3)
    condicao_sql: Optional[str] = None  # VARCHAR(260)
    separador_1: Optional[str] = None  # VARCHAR(10)
    separador_2: Optional[str] = None  # VARCHAR(10)
    separador_3: Optional[str] = None  # VARCHAR(10)
    tipo_valor: Optional[str] = None  # VARCHAR(1)
    atualizar: Optional[str] = None  # VARCHAR(1)
    protegida: Optional[str] = None  # VARCHAR(1)
    ativar_separador: Optional[str] = None  # VARCHAR(1)
    sql_completo: Optional[str] = None  # VARCHAR(1000)

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET)
# ----------------------------------------------------
class GMarcacaoTipoIdSchema(BaseModel):
    marcacao_tipo_id: int


# ----------------------------------------------------
# Schema para localizar um registro pela descrição (GET)
# ----------------------------------------------------
class GMarcacaoTipoDescricaoSchema(BaseModel):
    descricao: str

    class Config:
        from_attributes = True


class GMarcacaoTipoNomeSchema(BaseModel):
    nome: str
    sistema_id: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro por filtro (GET)
# ----------------------------------------------------
class GMarcacaoTipoGrupoSchema(BaseModel):
    grupo: str
    sistema_id: int
    situacao: str

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação de novo registro (POST)
# ----------------------------------------------------
class GMarcacaoTipoSaveSchema(GMarcacaoTipoSchema):

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização de registro (PUT)
# ----------------------------------------------------
class GMarcacaoTipoUpdateSchema(GMarcacaoTipoSchema):

    class Config:
        from_attributes = True
