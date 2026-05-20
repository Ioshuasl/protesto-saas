from typing import Optional
from pydantic.main import BaseModel


class ProcessDocumentSchema(BaseModel):

    id: str = None
    texto: Optional[bytes] = None
    save_disk: bool = True
    decompress: bool = False
    return_type: str = None

    class Config:
        from_attributes = True
