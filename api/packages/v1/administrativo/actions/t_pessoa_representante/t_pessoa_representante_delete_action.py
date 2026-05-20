from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_representante.t_pessoa_representante_delete_repository import (
    TPessoaRepresentanteDeleteRepository,
)
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteIdSchema,
)


class TPessoaRepresentanteDeleteAction(BaseAction):

    def execute(self, t_pessoa_representante_id_schema: TPessoaRepresentanteIdSchema):

        # Instanciamento do repositório
        t_pessoa_representante_delete_repository = (
            TPessoaRepresentanteDeleteRepository()
        )

        # Execução do repositório
        return t_pessoa_representante_delete_repository.execute(
            t_pessoa_representante_id_schema
        )
