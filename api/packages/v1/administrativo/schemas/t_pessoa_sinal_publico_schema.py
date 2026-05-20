from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, model_validator

from actions.validations.text import Text


class TPessoaSinalPublicoSchema(BaseModel):
    pessoa_sinalpublico_id: Optional[int] = None
    nome: Optional[str] = None
    tb_sinalpublico_id: Optional[int] = None
    pessoa_id: Optional[int] = None

    class Config:
        from_attributes = True


class TPessoaSinalPublicoIdSchema(BaseModel):
    pessoa_sinalpublico_id: int


class TPessoaSinalPublicoSaveSchema(BaseModel):
    pessoa_sinalpublico_id: Optional[int] = None
    nome: str
    tb_sinalpublico_id: int
    pessoa_id: int

    @field_validator("nome")
    def sanitize_nome(cls, value: str) -> str:
        return Text.sanitize_input(value)

    @model_validator(mode="after")
    def validate_all_fields(self):
        errors = []

        if not self.nome:
            errors.append({"input": "nome", "message": "O nome e obrigatorio."})
        elif len(self.nome) > 150:
            errors.append(
                {
                    "input": "nome",
                    "message": "O nome deve ter no maximo 150 caracteres.",
                }
            )

        if not self.tb_sinalpublico_id or self.tb_sinalpublico_id <= 0:
            errors.append(
                {
                    "input": "tb_sinalpublico_id",
                    "message": "O id do sinal publico e obrigatorio.",
                }
            )

        if not self.pessoa_id or self.pessoa_id <= 0:
            errors.append(
                {"input": "pessoa_id", "message": "O id da pessoa e obrigatorio."}
            )

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors,
            )

        return self


class TPessoaSinalPublicoUpdateSchema(BaseModel):
    nome: Optional[str] = None
    tb_sinalpublico_id: Optional[int] = None
    pessoa_id: Optional[int] = None

    @field_validator("nome")
    def sanitize_nome(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return Text.sanitize_input(value)

    @model_validator(mode="after")
    def validate_all_fields(self):
        errors = []

        if self.nome is None or not self.nome:
            errors.append({"input": "nome", "message": "O nome e obrigatorio."})
        elif len(self.nome) > 150:
            errors.append(
                {
                    "input": "nome",
                    "message": "O nome deve ter no maximo 150 caracteres.",
                }
            )

        if self.tb_sinalpublico_id is None or self.tb_sinalpublico_id <= 0:
            errors.append(
                {
                    "input": "tb_sinalpublico_id",
                    "message": "O id do sinal publico e obrigatorio.",
                }
            )

        if self.pessoa_id is None or self.pessoa_id <= 0:
            errors.append(
                {"input": "pessoa_id", "message": "O id da pessoa e obrigatorio."}
            )

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors,
            )

        return self
