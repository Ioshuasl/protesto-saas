from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_sinal_publico.t_pessoa_sinal_publico_delete_repository import (
    TPessoaSinalPublicoDeleteRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
)


class TPessoaSinalPublicoDeleteAction(BaseAction):
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoIdSchema):
        repository = TPessoaSinalPublicoDeleteRepository()
        return repository.execute(pessoa_sinal_publico_schema)
