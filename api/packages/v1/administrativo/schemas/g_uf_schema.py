from pydantic import BaseModel
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GUfSchema(BaseModel):
    g_uf_id: Optional[int] = None
    sigla: Optional[str] = None
    nome: Optional[str] = None
    cod_uf_ibge: Optional[str] = None

    class Config:
        from_attributes = True
