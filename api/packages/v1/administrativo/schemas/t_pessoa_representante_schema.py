from pydantic import BaseModel
from typing import Optional

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TPessoaRepresentanteSchema(BaseModel):
    representante_id: Optional[int] = None
    pessoa_representante_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    pessoa_auxiliar_id: Optional[int] = None
    marcacao_tipo_id: Optional[int] = None
    ato_partetipo_id: Optional[int] = None
    assinatura_tipo: Optional[str] = None

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para localizar (GET)
# ----------------------------------------------------
class TPessoaRepresentanteIdSchema(BaseModel):
    pessoa_representante_id: int

# ----------------------------------------------------
# Schema para localizar (GET)
# ----------------------------------------------------
class TPessoaRepresentantePessoaIdSchema(BaseModel):
    pessoa_id: int

# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TPessoaRepresentanteSaveSchema(BaseModel):
    representante_id: Optional[int] = None
    pessoa_representante_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    pessoa_auxiliar_id: Optional[int] = None
    marcacao_tipo_id: Optional[int] = None
    ato_partetipo_id: Optional[int] = None
    assinatura_tipo: Optional[str] = None

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TPessoaRepresentanteUpdateSchema(BaseModel):
    pessoa_representante_id: Optional[int] = None
    pessoa_id: Optional[int] = None
    pessoa_auxiliar_id: Optional[int] = None
    marcacao_tipo_id: Optional[int] = None
    ato_partetipo_id: Optional[int] = None
    assinatura_tipo: Optional[str] = None

    class Config:
        from_attributes = True