from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_sinal_publico.t_pessoa_sinal_publico_index_repository import (
    TPessoaSinalPublicoIndexRepository,
    TPessoaSinalPublicoSchema,
)


class TPessoaSinalPublicoIndexAction(BaseAction):
    def execute(self, data: TPessoaSinalPublicoSchema):
        repository = TPessoaSinalPublicoIndexRepository()
        return repository.execute(data)
