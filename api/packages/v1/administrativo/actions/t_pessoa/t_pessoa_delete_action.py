from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa.t_pessoa_delete_repository import (
    TPessoaDeleteRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema


class TPessoaDeleteAction(BaseAction):

    def execute(self, t_pessoa_id_schema: TPessoaIdSchema):

        # Instanciamento do repositório
        t_pessoa_delete_repository = TPessoaDeleteRepository()

        # Execução do repositório
        return t_pessoa_delete_repository.execute(t_pessoa_id_schema)
