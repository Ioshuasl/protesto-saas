from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text


# ----------------------------------------------------
# Schema base para G_TB_PROFISSAO
# ----------------------------------------------------
class GTbProfissaoSchema(BaseModel):
    tb_profissao_id: Optional[float] = None  # Numeric(10,2) pode ser representado por float em Python
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    cod_cbo: Optional[str] = None

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para localizar uma profissão específica pelo ID (GET)
# ----------------------------------------------------
class GTbProfissaoIdSchema(BaseModel):
    tb_profissao_id: float

# ----------------------------------------------------
# Schema para localizar uma profissão específica pela descrição (GET)
# ----------------------------------------------------
class GTbProfissaoDescricaoSchema(BaseModel):
    descricao: str

# ----------------------------------------------------
# Schema para criação de nova profissão (POST)
# ----------------------------------------------------
class GTbProfissaoSaveSchema(BaseModel):
    tb_profissao_id: Optional[float] = None
    descricao: str
    situacao: str
    cod_cbo: Optional[str] = None

    @field_validator('descricao', 'situacao', 'cod_cbo')
    def sanitize_fields(cls, v):
        if v is not None:
            return Text.sanitize_input(v)
        return v

    @model_validator(mode='after')
    def validate_all_fields(self):
        errors = []

        if not self.descricao or len(self.descricao.strip()) == 0:
            errors.append({'input': 'descricao', 'message': 'A descrição é obrigatória.'})

        if not self.situacao or len(self.situacao.strip()) == 0:
            errors.append({'input': 'situacao', 'message': 'A situação é obrigatória.'})
        elif len(self.situacao) != 1: # Validação adicional para o campo SITUACAO ser de 1 caractere
             errors.append({'input': 'situacao', 'message': 'A situação deve conter apenas um caractere.'})


        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )
        return self

# ----------------------------------------------------
# Schema para atualizar profissão (PUT)
# ----------------------------------------------------
class GTbProfissaoUpdateSchema(BaseModel):
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    cod_cbo: Optional[str] = None

    @field_validator('descricao', 'situacao', 'cod_cbo')
    def sanitize_fields(cls, v):
        if v is not None:
            return Text.sanitize_input(v)
        return v

    @model_validator(mode='after')
    def validate_all_fields(self):
        errors = []

        # Ao atualizar, os campos não são estritamente obrigatórios,
        # mas se forem preenchidos, devem ser válidos.
        if self.descricao is not None and len(self.descricao.strip()) == 0:
            errors.append({'input': 'descricao', 'message': 'A descrição não pode ser vazia se informada.'})

        if self.situacao is not None and len(self.situacao.strip()) == 0:
            errors.append({'input': 'situacao', 'message': 'A situação não pode ser vazia se informada.'})
        elif self.situacao is not None and len(self.situacao) != 1:
            errors.append({'input': 'situacao', 'message': 'A situação deve conter apenas um caractere se informada.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )
        return self