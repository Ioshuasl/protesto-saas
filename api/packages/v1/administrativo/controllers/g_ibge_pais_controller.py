from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisSaveSchema,
    GIbgePaisUpdateSchema,
    GIbgePaisIdSchema,
)
from packages.v1.administrativo.services.g_ibge_pais.g_ibge_pais_delete_service import (
    GIbgePaisDeleteService,
)
from packages.v1.administrativo.services.g_ibge_pais.g_ibge_pais_index_service import (
    GIbgePaisIndexService,
)
from packages.v1.administrativo.services.g_ibge_pais.g_ibge_pais_save_service import (
    GIbgePaisSaveService,
)
from packages.v1.administrativo.services.g_ibge_pais.g_ibge_pais_show_service import (
    GIbgePaisShowService,
)
from packages.v1.administrativo.services.g_ibge_pais.g_ibge_pais_update_service import (
    GIbgePaisUpdateService,
)


class GIbgePaisController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela G_IBGE_PAIS,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    # ----------------------------------------------------
    # Lista todos os registros de G_IBGE_PAIS
    # ----------------------------------------------------
    def index(self):

        # Instância da classe service
        service = GIbgePaisIndexService()

        # Execução da listagem
        return {
            "message": "Registros de G_IBGE_PAIS localizados com sucesso.",
            "data": service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de G_IBGE_PAIS pelo ID
    # ----------------------------------------------------
    def show(self, data: GIbgePaisIdSchema):

        # Instância da classe service
        service = GIbgePaisShowService()

        # Execução da busca
        return {
            "message": "Registro de G_IBGE_PAIS localizado com sucesso.",
            "data": service.execute(data),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em G_IBGE_PAIS
    # ----------------------------------------------------
    def save(self, data: GIbgePaisSaveSchema):

        # Instância da classe service
        service = GIbgePaisSaveService()

        # Execução do salvamento
        return {
            "message": "Registro de G_IBGE_PAIS salvo com sucesso.",
            "data": service.execute(data),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de G_IBGE_PAIS
    # ----------------------------------------------------
    def update(self, data: GIbgePaisUpdateSchema):

        # Instância da classe service
        service = GIbgePaisUpdateService()

        # Execução da atualização
        return {
            "message": "Registro de G_IBGE_PAIS atualizado com sucesso.",
            "data": service.execute(data),
        }

    # ----------------------------------------------------
    # Exclui um registro de G_IBGE_PAIS
    # ----------------------------------------------------
    def delete(self, data: GIbgePaisIdSchema):

        # Instância da classe service
        service = GIbgePaisDeleteService()

        # Execução da exclusão
        return {
            "message": "Registro de G_IBGE_PAIS removido com sucesso.",
            "data": service.execute(data),
        }
