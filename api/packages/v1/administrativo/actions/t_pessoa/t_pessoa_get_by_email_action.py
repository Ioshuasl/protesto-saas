from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa.t_pessoa_get_by_email_repository import (
    TPessoaGetByEmailRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaEmailSchema


class TPessoaGetByEmailAction(BaseAction):
    def execute(self, t_pessoa_email_schema: TPessoaEmailSchema):
        repository = TPessoaGetByEmailRepository()
        return repository.execute(t_pessoa_email_schema)
