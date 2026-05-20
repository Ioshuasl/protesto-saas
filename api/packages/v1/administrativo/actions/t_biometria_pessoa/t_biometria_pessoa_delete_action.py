from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_biometria_pessoa.t_biometria_pessoa_delete_repository import (
    TBiometriaPessoaDeleteRepository,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIdSchema,
)


class TBiometriaPessoaDeleteAction(BaseAction):

    def execute(self, t_biometria_pessoa_id_schema: TBiometriaPessoaIdSchema):
        
        # Instanciamento do repositório        
        t_biometria_pessoa_delete_repository = TBiometriaPessoaDeleteRepository()
        
        # Execução da exclusão        
        response = t_biometria_pessoa_delete_repository.execute(
            t_biometria_pessoa_id_schema
        )

        return response
