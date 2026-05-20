from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GTbBairroSchema(BaseModel):
    tb_bairro_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um Bairro especifico pelo ID (GET)
# ----------------------------------------------------
class GTbBairroIdSchema(BaseModel):
    tb_bairro_id: int


# ----------------------------------------------------
# Schema para localizar um Bairro especifico pela descrição (GET)
# ----------------------------------------------------
class GTbBairroDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de novo Bairro (POST)
# ----------------------------------------------------
class GTbBairroSaveSchema(BaseModel):
    tb_bairro_id: Optional[int] = None
    descricao: str
    situacao: str
    sistema_id: Optional[int] = None

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'situacao')
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

        if not self.situacao or len(self.situacao.strip()) == 0:
            errors.append({'input': 'situacao', 'message': 'A situação é obrigatória.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para atualizar Bairro (PUT)
# ----------------------------------------------------
class GTbBairroUpdateSchema(BaseModel):

    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'situacao')
    def sanitize_fields(cls, v):
        if v:
            return Text.sanitize_input(v)
        return v
    
    # Verifica se os campos obrigatórios foram enviados
    @model_validator(mode='after')
    def validate_all_fields(self):
        errors = []

        if not self.descricao and not self.situacao:
            errors.append({'input': 'descricao', 'message': 'A descrição é obrigatória para a atualização.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self