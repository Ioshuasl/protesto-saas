from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_livro_natureza.t_livro_natureza_show_modelo_repository import TLivroNaturezaShowModeloRepository
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaIdSchema


class TLivroNaturezaShowModeloAction(BaseAction):
    """Action para buscar um registro específico de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaIdSchema):
        repository = TLivroNaturezaShowModeloRepository()
        return repository.execute(schema)

