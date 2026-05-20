import base64
import os
import time
from io import BytesIO

import qrcode
from qrcode.constants import ERROR_CORRECT_M

from schemas.qrcode_schema import QrCodeSchema


class QRCode:

    @staticmethod
    def _microtime_filename(image_format: str) -> str:
        ext = (image_format or "PNG").lower()
        microtime = int(time.time() * 1_000_000)
        return f"{microtime}.{ext}"

    @staticmethod
    def execute(data: QrCodeSchema):
        qr = qrcode.QRCode(
            version=None,
            error_correction=ERROR_CORRECT_M,
            box_size=data.box_size,
            border=data.border,
        )

        qr.add_data(data.data or "")
        qr.make(fit=True)

        img = qr.make_image(fill_color=data.fill_color, back_color=data.back_color)
        image_format = (data.image_format or "PNG").upper()

        if data.output == "disk":
            base_path = data.file_path or ""
            directory = os.path.dirname(base_path)
            if directory:
                os.makedirs(directory, exist_ok=True)

            file_name = QRCode._microtime_filename(image_format)
            file_path = os.path.join(directory, file_name) if directory else file_name
            img.save(file_path, format=image_format)
            return file_path

        buffer = BytesIO()
        img.save(buffer, format=image_format)
        buffer.seek(0)
        payload = buffer.getvalue()

        if data.output == "binary":
            return payload

        if data.output == "buffer":
            return buffer

        if data.output == "base64":
            return base64.b64encode(payload).decode("utf-8")

        raise ValueError("output invalido. Use: base64, binary, buffer ou disk.")
