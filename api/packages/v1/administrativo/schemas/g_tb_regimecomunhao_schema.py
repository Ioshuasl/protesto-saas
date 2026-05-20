from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GTbRegimecomunhaoSchema(BaseModel):

    tb_regimecomunhao_id: int
    descricao: Optional[str] = None
    texto: Optional[str] = None
    situacao: Optional[str] = None
    tb_regimebens_id: Optional[int] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação de novo registro (POST)
# ----------------------------------------------------
class GTbRegimecomunhaoSaveSchema(BaseModel):

    tb_regimecomunhao_id: Optional[int] = None
    descricao: str
    texto: Optional[str] = None
    situacao: Optional[str] = None
    tb_regimebens_id: Optional[int] = None

    @field_validator('descricao')
    def validate_descricao(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError("A descrição é obrigatória.")
        return Text.sanitize_input(v)
    
    @model_validator(mode='after')
    def validate_all_fields(self):
        
        errors = []

        if not self.descricao or len(self.descricao.strip()) == 0:
            errors.append({'input': 'descricao', 'message': 'A descrição é obrigatória.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self

# ----------------------------------------------------
# Schema para atualização de registro (PUT)
# ----------------------------------------------------
class GTbRegimecomunhaoUpdateSchema(BaseModel):

    descricao: Optional[str] = None
    texto: Optional[str] = None
    situacao: Optional[str] = None
    tb_regimebens_id: Optional[int] = None

    @field_validator('descricao')
    def validate_descricao_field(cls, v):
        return Text.sanitize_input(v)


# ----------------------------------------------------
# Schema para localizar um registro específico pelo ID (GET, DELETE)
# ----------------------------------------------------
class GTbRegimecomunhaoIdSchema(BaseModel):

    # Campos utilizados
    tb_regimecomunhao_id: int

# ----------------------------------------------------
# Schema para localizar um registro pela descrição (GET)
# ----------------------------------------------------
class GTbRegimecomunhaoDescricaoSchema(BaseModel):

    # Campos utilizados
    descricao: str

    @field_validator('descricao')
    def validar_e_sanitizar_descricao(cls, v):
        if not v:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Informe a descrição'
            )
        return Text.sanitize_input(v)
    
    class Config:
        from_attributes = True