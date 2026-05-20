from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
# Supondo que a classe Text esteja disponível e com o método sanitize_input
try:
    from actions.validations.text import Text
except ImportError:
    class Text:
        @staticmethod
        def sanitize_input(value: str) -> str:
            return value.strip()


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GTbRegimebensSchema(BaseModel):
    tb_regimebens_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um tipo especifico pelo ID (GET)
# ----------------------------------------------------
class GTbRegimebensIdSchema(BaseModel):
    tb_regimebens_id: int


# ----------------------------------------------------
# Schema para localizar um tipo especifico pela descrição (GET)
# ----------------------------------------------------
class GTbRegimebensDescricaoSchema(BaseModel):
    descricao: str


# ----------------------------------------------------
# Schema para criação de novo tipo (POST)
# ----------------------------------------------------
class GTbRegimebensSaveSchema(BaseModel):
    tb_regimebens_id: Optional[int] = None
    descricao: str
    situacao: str

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
# Schema para atualizar tipo (PUT)
# ----------------------------------------------------
class GTbRegimebensUpdateSchema(BaseModel):

    descricao: Optional[str] = None
    situacao: Optional[str] = None

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