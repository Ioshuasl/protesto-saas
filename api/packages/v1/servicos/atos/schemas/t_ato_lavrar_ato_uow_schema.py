from typing import Optional

from pydantic import BaseModel
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.administrativo.schemas.g_selo_livro_schema import GSeloLivroUpdateSchema
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoUpdateSchema,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoLavraturaSchema,
    TAtoUpdateSchema,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema


class TAtoLavrarAtoUowSchema(BaseModel):
    lavratura: TAtoLavraturaSchema
    livro_andamento_update: TLivroAndamentoUpdateSchema
    caixa_item: CaixaItemSchema
    selos_update: list[GSeloLivroUpdateSchema]
    historico: THistoricoSaveSchema
    ato_anterior_update: Optional[TAtoUpdateSchema] = None

    class Config:
        from_attributes = True
