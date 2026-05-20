from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa.t_pessoa_get_by_cpf_repository import (
    TPessoaGetByCpfRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaCpfSchema


class TPessoaGetByCpfAction(BaseAction):
    def execute(self, t_pessoa_cpf_schema: TPessoaCpfSchema):
        repository = TPessoaGetByCpfRepository()
        return repository.execute(t_pessoa_cpf_schema)
