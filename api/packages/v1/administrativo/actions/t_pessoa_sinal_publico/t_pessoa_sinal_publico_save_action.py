from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_sinal_publico.t_pessoa_sinal_publico_save_repository import (
    TPessoaSinalPublicoSaveRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoSaveSchema,
)


class TPessoaSinalPublicoSaveAction(BaseAction):
    def execute(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoSaveSchema):
        repository = TPessoaSinalPublicoSaveRepository()
        return repository.execute(pessoa_sinal_publico_schema)
