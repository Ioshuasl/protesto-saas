# utils/base64_codec.py

import base64
import binascii
from typing import Union


class Base64Error(ValueError):
    """Erro de dominio para problemas de Base64."""

    pass


class Base64:
    """
    Utilitario robusto para encoding/decoding Base64.

    Trata:
    - padding ausente (=)
    - Base64 URL-safe (-, _)
    - data URLs (data:*;base64,...)
    - quebras de linha
    - validacao estrita
    """

    @staticmethod
    def encode(data: Union[bytes, str], *, urlsafe: bool = False) -> str:
        """
        Encode bytes ou string para Base64.

        :param data: bytes ou str
        :param urlsafe: usa Base64 URL-safe
        """
        if isinstance(data, str):
            data = data.encode("utf-8")

        if not isinstance(data, (bytes, bytearray)):
            raise Base64Error("Encode aceita apenas bytes ou str.")

        encoded = base64.urlsafe_b64encode(data) if urlsafe else base64.b64encode(data)

        return encoded.decode("ascii")

    @staticmethod
    def decode(data: object, *, urlsafe: bool | None = None):
        """
        Decode seguro de Base64.

        :param data: string Base64
        :param urlsafe:
            - True  -> forca Base64 URL-safe
            - False -> forca Base64 padrao
            - None  -> autodetecta
        """
        original = data
        if isinstance(data, (bytes, bytearray)):
            try:
                data = data.decode("utf-8")
            except Exception:
                data = str(data)
        else:
            data = str(data)

        # Normalizacao basica
        data = data.strip().replace("\n", "").replace("\r", "")

        # Remove data URL se existir
        if data.startswith("data:") and "," in data:
            data = data.split(",", 1)[1]

        # Autodetecta URL-safe
        if urlsafe is None:
            urlsafe = "-" in data or "_" in data

        if urlsafe:
            data = data.replace("-", "+").replace("_", "/")

        # Corrige padding
        padding = len(data) % 4
        if padding:
            data += "=" * (4 - padding)

        try:
            return base64.b64decode(data, validate=True)
        except binascii.Error:
            return original

    @staticmethod
    def is_valid(data: object) -> bool:
        """
        Valida se uma string e Base64 valido.
        """
        if isinstance(data, (bytes, bytearray)):
            try:
                data = data.decode("utf-8")
            except Exception:
                data = str(data)
        else:
            data = str(data)

        data = data.strip().replace("\n", "").replace("\r", "")

        if data.startswith("data:") and "," in data:
            data = data.split(",", 1)[1]

        urlsafe = "-" in data or "_" in data
        if urlsafe:
            data = data.replace("-", "+").replace("_", "/")

        padding = len(data) % 4
        if padding:
            data += "=" * (4 - padding)

        try:
            base64.b64decode(data, validate=True)
            return True
        except binascii.Error:
            return False
