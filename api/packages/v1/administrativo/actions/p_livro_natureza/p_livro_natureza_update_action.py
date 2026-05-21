from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_livro_natureza.p_livro_natureza_update_repository import (
    UpdateRepository,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import PLivroNaturezaUpdateSchema


class UpdateAction(BaseAction):
    def execute(self, livro_natureza_id: int, livro_natureza_schema: PLivroNaturezaUpdateSchema):
        return UpdateRepository().execute(livro_natureza_id, livro_natureza_schema)
