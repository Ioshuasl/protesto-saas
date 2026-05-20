from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIndexSchema,
    TCensecQualidadeAtoSaveSchema,
    TCensecQualidadeAtoUpdateSchema,
    TCensecQualidadeAtoIdSchema
)


class TCensecQualidadeAtoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_CENSEC_QUALIDADEATO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_censec_qualidadeato")

    # ----------------------------------------------------
    # Lista todos os registros de T_CENSEC_QUALIDADEATO
    # ----------------------------------------------------
    def index(self, censec_qualidade_ato_index_schema: TCensecQualidadeAtoIndexSchema):
        # Importação da classe desejada
        index_service = self.dynamic_import.service("t_censec_qualidadeato_index_service", "TCensecQualidadeAtoIndexService")

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_CENSEC_QUALIDADEATO localizados com sucesso.",
            "data": self.index_service.execute(censec_qualidade_ato_index_schema),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_CENSEC_QUALIDADEATO pelo ID
    # ----------------------------------------------------
    def show(self, t_censec_qualidadeato_id_schema: TCensecQualidadeAtoIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service("t_censec_qualidadeato_show_service", "TCensecQualidadeAtoShowService")

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_CENSEC_QUALIDADEATO localizado com sucesso.",
            "data": self.show_service.execute(t_censec_qualidadeato_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_CENSEC_QUALIDADEATO
    # ----------------------------------------------------
    def save(self, t_censec_qualidadeato_save_schema: TCensecQualidadeAtoSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service("t_censec_qualidadeato_save_service", "TCensecQualidadeAtoSaveService")

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_CENSEC_QUALIDADEATO salvo com sucesso.",
            "data": self.save_service.execute(t_censec_qualidadeato_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_CENSEC_QUALIDADEATO
    # ----------------------------------------------------
    def update(self, t_censec_qualidadeato_update_schema: TCensecQualidadeAtoUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service("t_censec_qualidadeato_update_service", "TCensecQualidadeAtoUpdateService")

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_CENSEC_QUALIDADEATO atualizado com sucesso.",
            "data": self.update_service.execute(t_censec_qualidadeato_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_CENSEC_QUALIDADEATO
    # ----------------------------------------------------
    def delete(self, t_censec_qualidadeato_id_schema: TCensecQualidadeAtoIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service("t_censec_qualidadeato_delete_service", "TCensecQualidadeAtoDeleteService")

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_CENSEC_QUALIDADEATO removido com sucesso.",
            "data": self.delete_service.execute(t_censec_qualidadeato_id_schema),
        }
