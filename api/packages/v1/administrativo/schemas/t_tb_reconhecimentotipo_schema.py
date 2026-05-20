from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TTbReconhecimentotipoSchema(BaseModel):
    tb_reconhecimentotipo_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um tipo especifico pelo ID (GET)
# ----------------------------------------------------
class TTbReconhecimentotipoIdSchema(BaseModel):
    tb_reconhecimentotipo_id: int


# ----------------------------------------------------
# Schema para localizar um tipo especifico pela descrição (GET)
# ----------------------------------------------------
class TTbReconhecimentotipoDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de novo tipo (POST)
# ----------------------------------------------------
class TTbReconhecimentotipoSaveSchema(BaseModel):
    tb_reconhecimentotipo_id: Optional[int] = None
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
class TTbReconhecimentotipoUpdateSchema(BaseModel):

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
