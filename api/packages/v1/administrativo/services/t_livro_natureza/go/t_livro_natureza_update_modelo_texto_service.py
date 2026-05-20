from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_update_modelo_texto_action import TLivroNaturezaUpdateModeloTextoAction
from packages.v1.administrativo.schemas.t_livro_natureza_schema import (
    TLivroNaturezaUpdateModeloSchema,
)


class TLivroNaturezaUpdateModeloTextoService:
    """Serviço para atualizar registros de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaUpdateModeloSchema):
        return TLivroNaturezaUpdateModeloTextoAction().execute(schema)

