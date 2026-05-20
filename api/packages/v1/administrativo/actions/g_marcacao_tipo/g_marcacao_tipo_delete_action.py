from abstracts.action import BaseAction

# O schema TServicoTipoIdSchema deve ser substituído por GMarcacaoTipoIdSchema
# que contém o campo-chave MARCACAO_TIPO_ID.
from packages.v1.administrativo.repositories.g_marcacao_tipo.g_marcacao_tipo_delete_repository import (
    GMarcacaoTipoDeleteRepository,
)
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoIdSchema,
)


class GMarcacaoTipoDeleteAction(BaseAction):

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoIdSchema):

        # Instanciamento do repositório
        delete_repository = GMarcacaoTipoDeleteRepository()

        # Execução do repositório
        return delete_repository.execute(marcacao_tipo_schema)
