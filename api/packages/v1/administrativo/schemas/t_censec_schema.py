from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TCensecSchema(BaseModel):
    censec_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um CENSEC especifico pelo ID (GET)
# ----------------------------------------------------
class TCensecIdSchema(BaseModel):
    censec_id: int


# ----------------------------------------------------
# Schema para localizar um CENSEC especifico pela descrição (GET)
# ----------------------------------------------------
class TCensecDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de novo CENSEC (POST)
# ----------------------------------------------------
class TCensecSaveSchema(BaseModel):
    censec_id: Optional[int] = None
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
# Schema para atualizar CENSEC (PUT)
# ----------------------------------------------------
class TCensecUpdateSchema(BaseModel):

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