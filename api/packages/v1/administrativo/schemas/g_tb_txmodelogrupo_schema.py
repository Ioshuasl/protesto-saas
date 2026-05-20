from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# ----------------------------------------------------
# Schema base para G_TB_TXMODELOGRUPO
# ----------------------------------------------------
class GTbTxmodelogrupoSchema(BaseModel):
    tb_txmodelogrupo_id: int  # NUMERIC(10,2)
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None  # NUMERIC(10,2)

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para criação de novo registro (POST) para G_TB_TXMODELOGRUPO
# ----------------------------------------------------
class GTbTxmodelogrupoSaveSchema(BaseModel):
    tb_txmodelogrupo_id: Optional[int] = None  # NUMERIC(10,2)
    descricao: str
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None  # NUMERIC(10,2)

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
        
        # Validação específica para TB_TXMODELOGRUPO_ID se não for fornecido e for obrigatório para criação
        # Se TB_TXMODELOGRUPO_ID é gerado pelo banco, esta validação pode ser removida ou ajustada
        if self.tb_txmodelogrupo_id is None: 
            # Assumindo que TB_TXMODELOGRUPO_ID é gerado pelo DB, caso contrário, descomente e ajuste:
            # errors.append({'input': 'tb_txmodelogrupo_id', 'message': 'O ID do modelo de grupo é obrigatório.'})
            pass

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )
        return self

# ----------------------------------------------------
# Schema para atualização de registro (PUT) para G_TB_TXMODELOGRUPO
# ----------------------------------------------------
class GTbTxmodelogrupoUpdateSchema(BaseModel):
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    sistema_id: Optional[int] = None  # NUMERIC(10,2)

    @field_validator('descricao')
    def validate_descricao_field(cls, v):
        # Permite que a descrição seja None para atualizações parciais
        if v is not None:
            return Text.sanitize_input(v)
        return v

# ----------------------------------------------------
# Schema para localizar um registro específico pelo ID (GET, DELETE) para G_TB_TXMODELOGRUPO
# ----------------------------------------------------
class GTbTxmodelogrupoIdSchema(BaseModel):
    # Campos utilizados
    tb_txmodelogrupo_id: int  # NUMERIC(10,2)

    @field_validator('tb_txmodelogrupo_id')
    def validate_id(cls, v):
        if v is None:
            raise ValueError("O ID do modelo de grupo é obrigatório.")
        # Pode adicionar validação de formato ou valor se necessário
        return v

# ----------------------------------------------------
# Schema para localizar um registro pela descrição (GET) para G_TB_TXMODELOGRUPO
# ----------------------------------------------------
class GTbTxmodelogrupoDescricaoSchema(BaseModel):
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