from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GTbEstadoCivilSchema(BaseModel):
    tb_estadocivil_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None
    tipo: Optional[int] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um Estado Civil especifico pelo ID (GET)
# ----------------------------------------------------
class GTbEstadoCivilIdSchema(BaseModel):
    tb_estadocivil_id: int


# ----------------------------------------------------
# Schema para localizar um Estado Civil especifico pela descrição (GET)
# ----------------------------------------------------
class GTbEstadoCivilDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de novo Estado Civil (POST)
# ----------------------------------------------------
class GTbEstadoCivilSaveSchema(BaseModel):
    tb_estadocivil_id: Optional[int] = None
    descricao: str
    situacao: str
    sistema_id: int
    tipo: int

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

        if self.sistema_id is None:
            errors.append({'input': 'sistema_id', 'message': 'O sistema_id é obrigatório.'})

        if self.tipo is None:
            errors.append({'input': 'tipo', 'message': 'O tipo é obrigatório.'})


        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para atualizar Estado Civil (PUT)
# ----------------------------------------------------
class GTbEstadoCivilUpdateSchema(BaseModel):

    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None
    tipo: Optional[int] = None

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