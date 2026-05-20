from typing import Optional
from fastapi import HTTPException, status
from pydantic import BaseModel, field_validator, model_validator
from actions.validations.text import Text
class TTbCartorioSchema(BaseModel):
    tb_cartorio_id: Optional[float] = None
    descricao: Optional[str] = None
    municipio_id: Optional[float] = None
    descricao_municipio: Optional[str] = None
    cns: Optional[str] = None
    class Config:
        from_attributes = True
class TTbCartorioIdSchema(BaseModel):
    tb_cartorio_id: float
class TTbCartorioSaveSchema(BaseModel):
    tb_cartorio_id: Optional[float] = None
    descricao: str
    municipio_id: float
    descricao_municipio: Optional[str] = None
    cns: str
    @field_validator("descricao", "descricao_municipio", "cns")
    @classmethod
    def sanitize_text(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)
    @model_validator(mode="after")
    def validate_payload(self):
        errors = []
        if not self.descricao or not self.descricao.strip():
            errors.append({"input": "descricao", "message": "A descricao e obrigatoria."})
        if self.municipio_id is None:
            errors.append({"input": "municipio_id", "message": "O municipio_id e obrigatorio."})
        if not self.cns or not self.cns.strip():
            errors.append({"input": "cns", "message": "O CNS e obrigatorio."})
        elif len(self.cns.strip()) != 10:
            errors.append({"input": "cns", "message": "O CNS deve ter exatamente 10 caracteres."})
        if errors:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors)
        return self
class TTbCartorioUpdateSchema(BaseModel):
    descricao: Optional[str] = None
    municipio_id: Optional[float] = None
    descricao_municipio: Optional[str] = None
    cns: Optional[str] = None
    @field_validator("descricao", "descricao_municipio", "cns")
    @classmethod
    def sanitize_text(cls, value: Optional[str]):
        if value is None:
            return value
        return Text.sanitize_input(value)
    @model_validator(mode="after")
    def validate_payload(self):
        errors = []
        if self.descricao is not None and not self.descricao.strip():
            errors.append({"input": "descricao", "message": "A descricao nao pode ser vazia."})
        if self.cns is not None and len(self.cns.strip()) != 10:
            errors.append({"input": "cns", "message": "O CNS deve ter exatamente 10 caracteres."})
        if errors:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors)
        return self
