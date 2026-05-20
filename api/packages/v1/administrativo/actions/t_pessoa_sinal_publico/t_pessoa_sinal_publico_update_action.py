from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_sinal_publico.t_pessoa_sinal_publico_update_repository import (
    TPessoaSinalPublicoUpdateRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoUpdateSchema,
)


class TPessoaSinalPublicoUpdateAction(BaseAction):
    def execute(
        self,
        pessoa_sinalpublico_id: int,
        pessoa_sinal_publico_schema: TPessoaSinalPublicoUpdateSchema,
    ):
        repository = TPessoaSinalPublicoUpdateRepository()
        return repository.execute(pessoa_sinalpublico_id, pessoa_sinal_publico_schema)
