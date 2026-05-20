from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_sinal_publico.t_pessoa_sinal_publico_show_repository import (
    TPessoaSinalPublicoShowRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
)


class TPessoaSinalPublicoShowAction(BaseAction):
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoIdSchema):
        repository = TPessoaSinalPublicoShowRepository()
        return repository.execute(pessoa_sinal_publico_schema)
