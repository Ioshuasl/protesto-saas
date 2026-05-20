from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Assumindo que esta importação de validação está disponível no ambiente
from actions.validations.text import Text


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GCidadeSchema(BaseModel):
    """
    Schema base para a tabela G_CIDADE.
    Representa a estrutura completa do registro.
    """

    cidade_id: int
    uf: Optional[str] = None
    cidade_nome: Optional[str] = None
    codigo_ibge: Optional[str] = None
    codigo_gyn: Optional[str] = None

    class Config:
        from_attributes = True


class GCidadeIndexSchema(BaseModel):
    uf: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um G_CIDADE especifico pelo ID (GET/DELETE)
# ----------------------------------------------------
class GCidadeIdSchema(BaseModel):
    """
    Schema para busca (SHOW) ou exclusão (DELETE) de registro por ID (CIDADE_ID).
    """

    cidade_id: int


# ----------------------------------------------------
# Schema para localizar um G_CIDADE especifico pelo nome (GET)
# ----------------------------------------------------
class GCidadeNomeSchema(BaseModel):
    """
    Schema para busca de registro por nome (CIDADE_NOME).
    """

    cidade_nome: str


# ----------------------------------------------------
# Schema para criação de novo G_CIDADE (POST)
# ----------------------------------------------------
class GCidadeSaveSchema(BaseModel):
    """
    Schema para salvar (POST) um novo registro de G_CIDADE.
    Os campos CIDADE_ID, UF e CIDADE_NOME são considerados obrigatórios.
    """

    cidade_id: Optional[int] = None
    uf: str
    cidade_nome: str
    codigo_ibge: Optional[str] = None
    codigo_gyn: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator("uf", "cidade_nome", "codigo_ibge", "codigo_gyn")
    def sanitize_fields(cls, v):
        if v:
            return Text.sanitize_input(v)
        return v

    # Verifica se os campos obrigatórios (UF, CIDADE_NOME) foram enviados
    @model_validator(mode="after")
    def validate_all_fields(self):
        errors = []

        # O campo 'cidade_id' é checado pela tipagem do Pydantic

        if not self.uf or len(self.uf.strip()) == 0:
            errors.append({"input": "uf", "message": "O campo UF é obrigatório."})

        if not self.cidade_nome or len(self.cidade_nome.strip()) == 0:
            errors.append(
                {"input": "cidade_nome", "message": "O nome da cidade é obrigatório."}
            )

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para atualizar G_CIDADE (PUT)
# ----------------------------------------------------
class GCidadeUpdateSchema(BaseModel):
    """
    Schema para atualizar (PUT) um registro de G_CIDADE.
    Todos os campos são opcionais, exceto o ID que virá na rota.
    """

    uf: Optional[str] = None
    cidade_nome: Optional[str] = None
    codigo_ibge: Optional[str] = None
    codigo_gyn: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator("uf", "cidade_nome", "codigo_ibge", "codigo_gyn")
    def sanitize_fields(cls, v):
        if v:
            return Text.sanitize_input(v)
        return v

    # Valida se os campos que foram enviados não estão vazios
    @model_validator(mode="after")
    def validate_all_fields(self):
        errors = []

        # Verifica se o campo foi enviado (self.uf is not None) e se a string está vazia após strip
        if self.uf is not None and len(self.uf.strip()) == 0:
            errors.append({"input": "uf", "message": "O campo UF não pode ser vazio."})

        if self.cidade_nome is not None and len(self.cidade_nome.strip()) == 0:
            errors.append(
                {
                    "input": "cidade_nome",
                    "message": "O nome da cidade não pode ser vazio.",
                }
            )

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
            )

        return self
