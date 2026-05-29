from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from actions.validations.text import Text


def _sanitize_optional_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    sanitized = Text.sanitize_input(str(value)).strip()
    return sanitized or None


class PTemplateSchema(BaseModel):
    template_id: Optional[int] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class PTemplateIdSchema(BaseModel):
    template_id: int


class PTemplateIndexSchema(BaseModel):
    template_id: Optional[int] = None
    descricao: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("descricao", mode="before")
    @classmethod
    def sanitize_descricao(cls, value: Optional[str]) -> Optional[str]:
        return _sanitize_optional_text(value)


class PTemplateSaveSchema(BaseModel):
    template_id: Optional[int] = None
    descricao: str

    model_config = ConfigDict(extra="forbid")

    @field_validator("descricao", mode="before")
    @classmethod
    def sanitize_descricao(cls, value: str) -> str:
        sanitized = _sanitize_optional_text(value)
        if sanitized is None:
            raise ValueError("A descrição é obrigatória.")
        return sanitized

    @model_validator(mode="after")
    def validate_required_fields(self):
        if not self.descricao or not self.descricao.strip():
            raise ValueError("A descrição é obrigatória.")
        return self


class PTemplateUpdateSchema(BaseModel):
    descricao: Optional[str] = None

    model_config = ConfigDict(extra="forbid")

    @field_validator("descricao", mode="before")
    @classmethod
    def sanitize_descricao(cls, value: Optional[str]) -> Optional[str]:
        return _sanitize_optional_text(value)


class PTemplateUpdateTextoSchema(BaseModel):
    template_id: int
    texto: bytes


class PTemplateEditorOpenSchema(BaseModel):
    mode: str = "edit"
    highlight_markers: bool = True

    model_config = ConfigDict(extra="forbid")

    @field_validator("mode", mode="before")
    @classmethod
    def sanitize_mode(cls, value: Optional[str]) -> str:
        normalized = (value or "edit").strip().lower()
        if normalized not in {"edit", "view"}:
            raise ValueError("mode deve ser 'edit' ou 'view'.")
        return normalized


class PTemplateEditorCallbackSchema(BaseModel):
    template_id: int
    data: dict
    callback_token: Optional[str] = None

    model_config = ConfigDict(extra="forbid")
