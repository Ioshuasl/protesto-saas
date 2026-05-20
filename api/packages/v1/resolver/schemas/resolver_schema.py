from decimal import Decimal
from typing import Optional
from pydantic.main import BaseModel


class ResolverSchema(BaseModel):
    id: Decimal = None
    texto: Optional[bytes] = None
    campo_id_valor: Optional[Decimal] = None
    sitema_id: int = None
    gramatica: Optional[dict] = None

    class Config:
        from_attributes = True


class DOCXSdtConvertSchema(BaseModel):
    input_docx: Optional[str] = None
    output_docx: Optional[str] = None
    save_to_disk: Optional[bool] = False

    class Config:
        from_attributes = True


class DOCXSdtExtractSchema(BaseModel):
    input_docx: Optional[str] = None
    input_content: Optional[bytes] = None

    class Config:
        from_attributes = True


class DOCXSdtFillerSchema(BaseModel):
    input_docx: Optional[str] = None
    output_docx: Optional[str] = None
    values: Optional[object] = None
    input_content: Optional[bytes] = None
    save_to_disk: Optional[bool] = False

    class Config:
        from_attributes = True
