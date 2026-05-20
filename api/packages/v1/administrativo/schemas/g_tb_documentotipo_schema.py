from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GTbDocumentoTipoSchema(BaseModel):
    tb_documentotipo_id: Optional[int] = None
    descricao: Optional[str] = None
    texto: Optional[bytes] = None
    situacao: Optional[str] = None
    possui_numeracao: Optional[str] = None
    orgao_padrao: Optional[str] = None
    descricao_simplificada: Optional[str] = None
    tipo: Optional[str] = None
    descricao_sinter: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um G_TB_DOCUMENTOTIPO especifico pelo ID (GET)
# ----------------------------------------------------
class GTbDocumentoTipoIdSchema(BaseModel):
    tb_documentotipo_id: int


# ----------------------------------------------------
# Schema para localizar um G_TB_DOCUMENTOTIPO especifico pela descrição (GET)
# ----------------------------------------------------
class GTbDocumentoTipoDescricaoSchema(BaseModel):
    descricao: str    


# ----------------------------------------------------
# Schema para criação de novo G_TB_DOCUMENTOTIPO (POST)
# ----------------------------------------------------
class GTbDocumentoTipoSaveSchema(BaseModel):
    tb_documentotipo_id: Optional[int] = None
    descricao: str
    texto: Optional[bytes] = None
    situacao: str
    possui_numeracao: str
    orgao_padrao: str
    descricao_simplificada: str
    tipo: str
    descricao_sinter: str

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'situacao', 'possui_numeracao', 'orgao_padrao', 'descricao_simplificada', 'tipo', 'descricao_sinter')
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

        if not self.possui_numeracao or len(self.possui_numeracao.strip()) == 0:
            errors.append({'input': 'possui_numeracao', 'message': 'A informação se possui numeração é obrigatória.'})

        if not self.orgao_padrao or len(self.orgao_padrao.strip()) == 0:
            errors.append({'input': 'orgao_padrao', 'message': 'O orgão padrão é obrigatório.'})

        if not self.descricao_simplificada or len(self.descricao_simplificada.strip()) == 0:
            errors.append({'input': 'descricao_simplificada', 'message': 'A descrição simplificada é obrigatória.'})

        if not self.tipo or len(self.tipo.strip()) == 0:
            errors.append({'input': 'tipo', 'message': 'O tipo é obrigatório.'})

        if not self.descricao_sinter or len(self.descricao_sinter.strip()) == 0:
            errors.append({'input': 'descricao_sinter', 'message': 'A descrição do SINTER é obrigatória.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para atualizar G_TB_DOCUMENTOTIPO (PUT)
# ----------------------------------------------------
class GTbDocumentoTipoUpdateSchema(BaseModel):
    descricao: Optional[str] = None
    texto: Optional[bytes] = None
    situacao: Optional[str] = None
    possui_numeracao: Optional[str] = None
    orgao_padrao: Optional[str] = None
    descricao_simplificada: Optional[str] = None
    tipo: Optional[str] = None
    descricao_sinter: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator('descricao', 'situacao', 'possui_numeracao', 'orgao_padrao', 'descricao_simplificada', 'tipo', 'descricao_sinter')
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

        if self.possui_numeracao is not None and len(self.possui_numeracao.strip()) == 0:
            errors.append({'input': 'possui_numeracao', 'message': 'A informação se possui numeração é obrigatória.'})

        if self.orgao_padrao is not None and len(self.orgao_padrao.strip()) == 0:
            errors.append({'input': 'orgao_padrao', 'message': 'O orgão padrão é obrigatório.'})

        if self.descricao_simplificada is not None and len(self.descricao_simplificada.strip()) == 0:
            errors.append({'input': 'descricao_simplificada', 'message': 'A descrição simplificada é obrigatória.'})

        if self.tipo is not None and len(self.tipo.strip()) == 0:
            errors.append({'input': 'tipo', 'message': 'O tipo é obrigatório.'})

        if self.descricao_sinter is not None and len(self.descricao_sinter.strip()) == 0:
            errors.append({'input': 'descricao_sinter', 'message': 'A descrição do SINTER é obrigatória.'})
        
        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self