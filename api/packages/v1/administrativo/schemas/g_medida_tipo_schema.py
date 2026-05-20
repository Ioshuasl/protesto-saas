from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GMedidaTipoSchema(BaseModel):
    medida_tipo_id: Optional[int] = None
    descricao: Optional[str] = None
    sigla: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um G_MEDIDA_TIPO especifico pelo ID (GET)
# ----------------------------------------------------
class GMedidaTipoIdSchema(BaseModel):
    medida_tipo_id: int


# ----------------------------------------------------
# Schema para localizar um G_MEDIDA_TIPO especifico pela descrição (GET)
# ----------------------------------------------------
class GMedidaTipoDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de novo G_MEDIDA_TIPO (POST)
# ----------------------------------------------------
class GMedidaTipoSaveSchema(BaseModel):
    medida_tipo_id: Optional[int] = None
    descricao: str
    sigla: str

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'sigla')
    def sanitize_fields(cls, v):
        if v:
            return Text.sanitize_input(v)
        return v
    
    # Verifica se os campos obrigatórios foram enviados
    @model_validator(mode='after')
    def validate_all_fields(self):
        errors = []
        if not self.descricao or len(self.descricao.strip()) == 0:
            errors.append({'input': 'descricao', 'message': 'A descrição é obrigatória.'})

        if not self.sigla or len(self.sigla.strip()) == 0:
            errors.append({'input': 'sigla', 'message': 'A sigla é obrigatória.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para atualizar G_MEDIDA_TIPO (PUT)
# ----------------------------------------------------
class GMedidaTipoUpdateSchema(BaseModel):

    descricao: Optional[str] = None
    sigla: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'sigla')
    def sanitize_fields(cls, v):
        if v:
            return Text.sanitize_input(v)
        return v
    
    # Verifica se os campos obrigatórios foram enviados
    @model_validator(mode='after')
    def validate_all_fields(self):
        errors = []

        if not self.descricao and not self.sigla:
            errors.append({'input': 'all', 'message': 'É necessário informar ao menos um campo para alteração.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self