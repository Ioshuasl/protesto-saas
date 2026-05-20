from typing import Literal, Optional

from pydantic.main import BaseModel


class QrCodeSchema(BaseModel):

    data: str = None
    box_size: int = 10
    border: int = 4
    output: Literal["base64", "binary", "buffer", "disk"] = "base64"
    file_path: Optional[str] = "qrcode.png"
    image_format: str = "PNG"
    fill_color: str = "black"
    back_color: str = "white"

    class Config:
        from_attributes = True
