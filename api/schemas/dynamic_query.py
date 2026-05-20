from pydantic import BaseModel


class DynamicQuery(BaseModel):
    class Config:
        extra = "allow"  # ← permite receber qualquer campo dinamicamente
