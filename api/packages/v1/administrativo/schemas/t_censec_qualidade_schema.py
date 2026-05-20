from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TCensecQualidadeSchema(BaseModel):
    censec_qualidade_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    aceita_cnpj: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um CENSEC_QUALIDADE especifico pelo ID (GET)
# ----------------------------------------------------
class TCensecQualidadeIdSchema(BaseModel):
    censec_qualidade_id: int


# ----------------------------------------------------
# Schema para localizar um CENSEC_QUALIDADE especifico pela descrição (GET)
# ----------------------------------------------------
class TCensecQualidadeDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de novo CENSEC_QUALIDADE (POST)
# ----------------------------------------------------
class TCensecQualidadeSaveSchema(BaseModel):
    censec_qualidade_id: Optional[int] = None
    descricao: str
    situacao: str
    aceita_cnpj: str

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'situacao', 'aceita_cnpj')
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
            
        if not self.aceita_cnpj or len(self.aceita_cnpj.strip()) == 0:
            errors.append({'input': 'aceita_cnpj', 'message': 'O campo aceita_cnpj é obrigatório.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para atualizar CENSEC_QUALIDADE (PUT)
# ----------------------------------------------------
class TCensecQualidadeUpdateSchema(BaseModel):

    descricao: Optional[str] = None
    situacao: Optional[str] = None
    aceita_cnpj: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'situacao', 'aceita_cnpj')
    def sanitize_fields(cls, v):
        if v:
            return Text.sanitize_input(v)
        return v
    
    # Verifica se os campos obrigatórios foram enviados
    @model_validator(mode='after')
    def validate_all_fields(self):
        errors = []

        if self.descricao is not None and len(self.descricao.strip()) == 0:
            errors.append({'input': 'descricao', 'message': 'A descrição é obrigatória.'})

        if self.situacao is not None and len(self.situacao.strip()) == 0:
            errors.append({'input': 'situacao', 'message': 'A situação é obrigatória.'})
            
        if self.aceita_cnpj is not None and len(self.aceita_cnpj.strip()) == 0:
            errors.append({'input': 'aceita_cnpj', 'message': 'O campo aceita_cnpj é obrigatório.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self