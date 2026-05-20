from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GNaturezaSchema(BaseModel):
    natureza_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None
    pedir_numero_imovel: Optional[str] = None
    controle_frenteverso: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar uma NATUREZA especifica pelo ID (GET)
# ----------------------------------------------------
class GNaturezaIdSchema(BaseModel):
    natureza_id: int

# ----------------------------------------------------
# Schema para localizar uma NATUREZA especifica pelo ID (GET)
# ----------------------------------------------------
class GNaturezaSistemaIdSchema(BaseModel):
    sistema_id: int

# ----------------------------------------------------
# Schema para localizar uma NATUREZA especifica pela descrição (GET)
# ----------------------------------------------------
class GNaturezaDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de nova NATUREZA (POST)
# ----------------------------------------------------
class GNaturezaSaveSchema(BaseModel):
    natureza_id: Optional[int] = None
    descricao: str
    situacao: str
    sistema_id: Optional[int] = None
    pedir_numero_imovel: Optional[str] = None
    controle_frenteverso: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'situacao', 'pedir_numero_imovel', 'controle_frenteverso')
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
# Schema para atualizar NATUREZA (PUT)
# ----------------------------------------------------
class GNaturezaUpdateSchema(BaseModel):

    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None
    pedir_numero_imovel: Optional[str] = None
    controle_frenteverso: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'situacao', 'pedir_numero_imovel', 'controle_frenteverso')
    def sanitize_fields(cls, v):
        if v:
            return Text.sanitize_input(v)
        return v
    
    # Verifica se os campos obrigatórios foram enviados
    @model_validator(mode='after')
    def validate_all_fields(self):
        errors = []

        # A validação de campos obrigatórios é diferente para atualização, pois os campos são opcionais.
        # A lógica para a validação pode ser mais complexa dependendo das regras de negócio.
        
        # Para este exemplo, não há campos obrigatórios na atualização.
        # Se você precisar de validação de campos obrigatórios, pode adicionar aqui.

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self