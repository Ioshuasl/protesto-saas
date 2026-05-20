from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoSaveSchema,
    TAtoTipoUpdateSchema,
    TAtoTipoIdSchema,
)


class TAtoTipoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_ATO_TIPO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.atos")
        self.dynamic_import.set_table("t_ato_tipo")

    # ----------------------------------------------------
    # Lista todos os registros de T_ATO_TIPO
    # ----------------------------------------------------
    def index(self):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_ato_tipo_index_service", "TAtoTipoIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_ATO_TIPO localizados com sucesso.",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_ATO_TIPO pelo ID
    # ----------------------------------------------------
    def show(self, t_ato_tipo_id_schema: TAtoTipoIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_ato_tipo_show_service", "TAtoTipoShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_ATO_TIPO localizado com sucesso.",
            "data": self.show_service.execute(t_ato_tipo_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_ATO_TIPO
    # ----------------------------------------------------
    def save(self, t_ato_tipo_save_schema: TAtoTipoSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_ato_tipo_save_service", "TAtoTipoSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_ATO_TIPO salvo com sucesso.",
            "data": self.save_service.execute(t_ato_tipo_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_ATO_TIPO
    # ----------------------------------------------------
    def update(self, t_ato_tipo_update_schema: TAtoTipoUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_ato_tipo_update_service", "TAtoTipoUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_ATO_TIPO atualizado com sucesso.",
            "data": self.update_service.execute(t_ato_tipo_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_ATO_TIPO
    # ----------------------------------------------------
    def delete(self, t_ato_tipo_id_schema: TAtoTipoIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_ato_tipo_delete_service", "TAtoTipoDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_ATO_TIPO removido com sucesso.",
            "data": self.delete_service.execute(t_ato_tipo_id_schema),
        }
