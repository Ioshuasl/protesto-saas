from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_update_action import (
    TLivroNaturezaUpdateAction,
)
from packages.v1.administrativo.schemas.t_livro_natureza_schema import (
    TLivroNaturezaUpdateSchema,
)


class TLivroNaturezaUpdateService:
    """Serviço para atualizar registros de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaUpdateSchema):
        action = TLivroNaturezaUpdateAction()
        return action.execute(schema)

