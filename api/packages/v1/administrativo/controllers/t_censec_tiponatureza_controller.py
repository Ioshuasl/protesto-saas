from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaSaveSchema,
    TCensecTipoNaturezaUpdateSchema,
    TCensecTipoNaturezaIdSchema
)


class TCensecTipoNaturezaController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_CENSEC_TIPONATUREZA,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_censec_tiponatureza")

    # ----------------------------------------------------
    # Lista todos os registros de T_CENSEC_TIPONATUREZA
    # ----------------------------------------------------
    def index(self):
        # Importação da classe desejada
        index_service = self.dynamic_import.service("t_censec_tiponatureza_index_service", "TCensecTipoNaturezaIndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_CENSEC_TIPONATUREZA localizados com sucesso.",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_CENSEC_TIPONATUREZA pelo ID
    # ----------------------------------------------------
    def show(self, t_censec_tiponatureza_id_schema: TCensecTipoNaturezaIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service("t_censec_tiponatureza_show_service", "TCensecTipoNaturezaShowService")

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_CENSEC_TIPONATUREZA localizado com sucesso.",
            "data": self.show_service.execute(t_censec_tiponatureza_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_CENSEC_TIPONATUREZA
    # ----------------------------------------------------
    def save(self, t_censec_tiponatureza_save_schema: TCensecTipoNaturezaSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service("t_censec_tiponatureza_save_service", "TCensecTipoNaturezaSaveService")

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_CENSEC_TIPONATUREZA salvo com sucesso.",
            "data": self.save_service.execute(t_censec_tiponatureza_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_CENSEC_TIPONATUREZA
    # ----------------------------------------------------
    def update(self, t_censec_tiponatureza_update_schema: TCensecTipoNaturezaUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service("t_censec_tiponatureza_update_service", "TCensecTipoNaturezaUpdateService")

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_CENSEC_TIPONATUREZA atualizado com sucesso.",
            "data": self.update_service.execute(t_censec_tiponatureza_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_CENSEC_TIPONATUREZA
    # ----------------------------------------------------
    def delete(self, t_censec_tiponatureza_id_schema: TCensecTipoNaturezaIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service("t_censec_tiponatureza_delete_service", "TCensecTipoNaturezaDeleteService")

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_CENSEC_TIPONATUREZA removido com sucesso.",
            "data": self.delete_service.execute(t_censec_tiponatureza_id_schema),
        }
