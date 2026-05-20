from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GTbTipoLogradouroSchema(BaseModel):
    tb_tipologradouro_id: Optional[float] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[float] = None
    situacao_id: Optional[float] = None
    onr_tipo_logradouro_id: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um g_tb_tipologradouro especifico pelo ID (GET)
# ----------------------------------------------------
class GTbTipoLogradouroIdSchema(BaseModel):
    tb_tipologradouro_id: float


# ----------------------------------------------------
# Schema para localizar um g_tb_tipologradouro especifico pela descrição (GET)
# ----------------------------------------------------
class GTbTipoLogradouroDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de novo g_tb_tipologradouro (POST)
# ----------------------------------------------------
class GTbTipoLogradouroSaveSchema(BaseModel):
    tb_tipologradouro_id: Optional[float] = None
    descricao: str
    situacao: str
    sistema_id: Optional[float] = None
    situacao_id: Optional[float] = None
    onr_tipo_logradouro_id: Optional[float] = None

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
# Schema para atualizar g_tb_tipologradouro (PUT)
# ----------------------------------------------------
class GTbTipoLogradouroUpdateSchema(BaseModel):
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[float] = None
    situacao_id: Optional[float] = None
    onr_tipo_logradouro_id: Optional[float] = None

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