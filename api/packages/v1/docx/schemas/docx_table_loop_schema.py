from typing import Any, Dict, List, Optional

from pydantic import Field
from pydantic.main import BaseModel


class DOCXTableLoopSchema(BaseModel):
    input_docx: Optional[str] = None
    input_content: Optional[bytes] = None
    output_docx: Optional[str] = None
    save_to_disk: bool = False
    collections: Dict[str, List[Any]] = Field(default_factory=dict)
    clear_when_empty: bool = True

    class Config:
        from_attributes = True
