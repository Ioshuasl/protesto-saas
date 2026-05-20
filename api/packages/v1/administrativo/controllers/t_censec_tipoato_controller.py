from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoSaveSchema,
    TCensecTipoAtoUpdateSchema,
    TCensecTipoAtoIdSchema
)


class TCensecTipoAtoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_CENSEC_TIPOATO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_censec_tipoato")

    # ----------------------------------------------------
    # Lista todos os registros de T_CENSEC_TIPOATO
    # ----------------------------------------------------
    def index(self):
        # Importação da classe desejada
        index_service = self.dynamic_import.service("t_censec_tipoato_index_service", "TCensecTipoAtoIndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_CENSEC_TIPOATO localizados com sucesso.",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_CENSEC_TIPOATO pelo ID
    # ----------------------------------------------------
    def show(self, t_censec_tipoato_id_schema: TCensecTipoAtoIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service("t_censec_tipoato_show_service", "TCensecTipoAtoShowService")

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_CENSEC_TIPOATO localizado com sucesso.",
            "data": self.show_service.execute(t_censec_tipoato_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_CENSEC_TIPOATO
    # ----------------------------------------------------
    def save(self, t_censec_tipoato_save_schema: TCensecTipoAtoSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service("t_censec_tipoato_save_service", "TCensecTipoAtoSaveService")

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_CENSEC_TIPOATO salvo com sucesso.",
            "data": self.save_service.execute(t_censec_tipoato_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_CENSEC_TIPOATO
    # ----------------------------------------------------
    def update(self, t_censec_tipoato_update_schema: TCensecTipoAtoUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service("t_censec_tipoato_update_service", "TCensecTipoAtoUpdateService")

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_CENSEC_TIPOATO atualizado com sucesso.",
            "data": self.update_service.execute(t_censec_tipoato_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_CENSEC_TIPOATO
    # ----------------------------------------------------
    def delete(self, t_censec_tipoato_id_schema: TCensecTipoAtoIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service("t_censec_tipoato_delete_service", "TCensecTipoAtoDeleteService")

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_CENSEC_TIPOATO removido com sucesso.",
            "data": self.delete_service.execute(t_censec_tipoato_id_schema),
        }
