from typing import Optional
from pydantic import BaseModel


class GEDIndexSchema(BaseModel):
    serventia: Optional[int] = None
    pasta: Optional[str] = None
    registro_id: Optional[str] = None
    filename: Optional[str] = None

    class Config:
        from_attributes = True


class GEDSaveSchema(BaseModel):
    serventia: Optional[int] = None
    pasta: Optional[str] = None
    registro_id: Optional[str] = None
    base64: str

    class Config:
        from_attributes = True


class GEDPathSchema(BaseModel):
    serventia: int
    pasta: str
    registro_id: str

    class Config:
        from_attributes = True


class GEDSaveBase64RequestSchema(BaseModel):
    path: GEDPathSchema
    request: object

    class Config:
        arbitrary_types_allowed = True


class GEDSaveMultipartRequestSchema(BaseModel):
    path: GEDPathSchema
    request: object

    class Config:
        arbitrary_types_allowed = True


class GEDMultipartPayloadSchema(BaseModel):
    file_bytes: Optional[bytes] = None
    base64_value: Optional[str] = None
    file_content_type: Optional[str] = None


class GEDDocxPageSetupSchema(BaseModel):
    orientation: str
    page_width_mm: float
    page_height_mm: float
    top_margin_mm: float
    bottom_margin_mm: float
    left_margin_mm: float
    right_margin_mm: float

    class Config:
        from_attributes = True
