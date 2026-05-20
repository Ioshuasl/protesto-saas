from typing import Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, model_validator

from actions.validations.text import Text


class TTbSinalPublicoSchema(BaseModel):
    tb_sinalpublico_id: Optional[int] = None
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    class Config:
        from_attributes = True


class TTbSinalPublicoIdSchema(BaseModel):
    tb_sinalpublico_id: int


class TTbSinalPublicoDescricaoSchema(BaseModel):
    descricao: str

    @field_validator("descricao")
    def sanitize_descricao(cls, value: str) -> str:
        return Text.sanitize_input(value)


class TTbSinalPublicoSaveSchema(BaseModel):
    tb_sinalpublico_id: Optional[int] = None
    descricao: str
    situacao: str

    @field_validator("descricao", "situacao")
    def sanitize_fields(cls, value: str) -> str:
        return Text.sanitize_input(value)

    @model_validator(mode="after")
    def validate_all_fields(self):
        errors = []

        if not self.descricao:
            errors.append({"input": "descricao", "message": "A descricao e obrigatoria."})
        elif len(self.descricao) > 30:
            errors.append(
                {"input": "descricao", "message": "A descricao deve ter no maximo 30 caracteres."}
            )

        if not self.situacao:
            errors.append({"input": "situacao", "message": "A situacao e obrigatoria."})
        elif len(self.situacao) > 1:
            errors.append(
                {"input": "situacao", "message": "A situacao deve ter no maximo 1 caractere."}
            )

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors,
            )

        return self


class TTbSinalPublicoUpdateSchema(BaseModel):
    descricao: Optional[str] = None
    situacao: Optional[str] = None

    @field_validator("descricao", "situacao")
    def sanitize_fields(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return Text.sanitize_input(value)

    @model_validator(mode="after")
    def validate_all_fields(self):
        errors = []

        if self.descricao is None or not self.descricao:
            errors.append({"input": "descricao", "message": "A descricao e obrigatoria."})
        elif len(self.descricao) > 30:
            errors.append(
                {"input": "descricao", "message": "A descricao deve ter no maximo 30 caracteres."}
            )

        if self.situacao is None or not self.situacao:
            errors.append({"input": "situacao", "message": "A situacao e obrigatoria."})
        elif len(self.situacao) > 1:
            errors.append(
                {"input": "situacao", "message": "A situacao deve ter no maximo 1 caractere."}
            )

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors,
            )

        return self
