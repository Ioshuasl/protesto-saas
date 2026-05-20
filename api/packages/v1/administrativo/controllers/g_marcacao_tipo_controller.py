from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoNomeSchema,
    GMarcacaoTipoSaveSchema,
    GMarcacaoTipoUpdateSchema,
    GMarcacaoTipoIdSchema,
    GMarcacaoTipoDescricaoSchema,
    GMarcacaoTipoGrupoSchema,
)
from packages.v1.administrativo.services.g_marcacao_tipo.go.g_marcacao_tipo_delete_service import (
    GMarcacaoTipoDeleteService,
)
from packages.v1.administrativo.services.g_marcacao_tipo.go.g_marcacao_tipo_get_by_descricao_service import (
    GMarcacaoTipoGetByDescricaoService,
)
from packages.v1.administrativo.services.g_marcacao_tipo.go.g_marcacao_tipo_get_by_grupo_service import (
    GMarcacaoTipoGetByGrupoService,
)
from packages.v1.administrativo.services.g_marcacao_tipo.go.g_marcacao_tipo_get_by_nome_service import (
    GMarcacaoTipoGetByNomeService,
)
from packages.v1.administrativo.services.g_marcacao_tipo.go.g_marcacao_tipo_index_service import (
    GMarcacaoTipoIndexService,
)
from packages.v1.administrativo.services.g_marcacao_tipo.go.g_marcacao_tipo_save_service import (
    GMarcacaoTipoSaveService,
)
from packages.v1.administrativo.services.g_marcacao_tipo.go.g_marcacao_tipo_show_service import (
    GMarcacaoTipoShowService,
)
from packages.v1.administrativo.services.g_marcacao_tipo.go.g_marcacao_tipo_update_service import (
    GMarcacaoTipoUpdateService,
)


class GMarcacaoTipoController:

    # Lista todos os registros de marcacao tipo
    def index(self):

        # Instância da classe service
        service = GMarcacaoTipoIndexService()

        # Lista todos os registros de marcacao tipo
        return {
            "message": "Registros de marcação tipo localizados com sucesso",
            "data": service.execute(),
        }

    # Busca um registro de marcacao tipo específico pelo ID
    def show(self, data: GMarcacaoTipoIdSchema):

        # Importação da classe desejada
        service = GMarcacaoTipoShowService()

        # Busca e retorna o registro de marcacao tipo desejado
        return {
            "message": "Registro de marcação tipo localizado com sucesso",
            "data": service.execute(data),
        }

    # Busca um registro de marcacao tipo pela descrição
    def get_by_descricao(self, data: GMarcacaoTipoDescricaoSchema):

        # Importação da classe desejada
        service = GMarcacaoTipoGetByDescricaoService()

        # Busca e retorna o registro de marcacao tipo desejado
        return {
            "message": "Registro de marcação tipo localizado com sucesso",
            "data": service.execute(data, True),
        }

    # Busca um registro de marcacao tipo pela descrição
    def get_by_nome(self, data: GMarcacaoTipoNomeSchema):

        # Importação da classe desejada
        service = GMarcacaoTipoGetByNomeService()

        # Busca e retorna o registro de marcacao tipo desejado
        return {
            "message": "Registro de marcação tipo localizado com sucesso",
            "data": service.execute(data),
        }

    # Cadastra um novo registro de marcacao tipo
    def save(self, data: GMarcacaoTipoSaveSchema):

        # Importação da classe desejada
        service = GMarcacaoTipoSaveService()

        # Busca e retorna o registro de marcacao tipo desejado
        return {
            "message": "Registro de marcação tipo salvo com sucesso",
            "data": service.execute(data),
        }

    # Atualiza os dados de um registro de marcacao tipo
    def update(self, data: GMarcacaoTipoUpdateSchema):

        # Importação da classe desejada
        service = GMarcacaoTipoUpdateService()

        # Busca e retorna o registro de marcacao tipo desejado
        return {
            "message": "Registro de marcação tipo atualizado com sucesso",
            "data": service.execute(data),
        }

    # Exclui um registro de marcacao tipo
    def delete(self, data: GMarcacaoTipoIdSchema):

        # Instância da classe desejada
        service = GMarcacaoTipoDeleteService()

        # Busca e retorna o registro de marcacao tipo desejado
        return {
            "message": "Registro de marcação tipo removido com sucesso",
            "data": service.execute(data),
        }

    # Busca um registro de marcacao tipo por filtro
    def get_by_grupo(self, data: GMarcacaoTipoGrupoSchema):

        # Importação da classe desejada
        service = GMarcacaoTipoGetByGrupoService()

        # Busca e retorna o registro de marcacao tipo desejado
        return {
            "message": "Registro de marcação tipo localizado com sucesso",
            "data": service.execute(data, False),
        }
