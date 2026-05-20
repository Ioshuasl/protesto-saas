from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIndexSchema,
    TAtoVinculoParteSaveSchema,
    TAtoVinculoParteUpdateSchema,
    TAtoVinculoParteIdSchema,
    TAtoVinculoParteTextoQualificacaoUpdateSchema,
)


class TAtoVinculoParteController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_ATO_VINCULOPARTE,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.atos")
        self.dynamic_import.set_table("t_ato_vinculoparte")

    # ----------------------------------------------------
    # Lista todos os registros de T_ATO_VINCULOPARTE
    # ----------------------------------------------------
    def index(self, data: TAtoVinculoParteIndexSchema):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_ato_vinculoparte_index_service", "TAtoVinculoParteIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_ATO_VINCULOPARTE localizados com sucesso.",
            "data": self.index_service.execute(data),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_ATO_VINCULOPARTE pelo ID
    # ----------------------------------------------------
    def show(self, t_ato_vinculoparte_id_schema: TAtoVinculoParteIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_ato_vinculoparte_show_service", "TAtoVinculoParteShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_ATO_VINCULOPARTE localizado com sucesso.",
            "data": self.show_service.execute(t_ato_vinculoparte_id_schema),
        }

    def show_texto_qualificacao(self, t_ato_vinculoparte_id_schema: TAtoVinculoParteIdSchema):
        show_service = self.dynamic_import.service(
            "t_ato_vinculoparte_show_texto_qualificacao_service",
            "TAtoVinculoParteShowTextoQualificacaoService",
        )
        self.show_service = show_service()
        return {
            "message": "Texto de qualificação localizado com sucesso.",
            "data": self.show_service.execute(t_ato_vinculoparte_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_ATO_VINCULOPARTE
    # ----------------------------------------------------
    def save(self, t_ato_vinculoparte_save_schema: TAtoVinculoParteSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_ato_vinculoparte_save_service", "TAtoVinculoParteSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_ATO_VINCULOPARTE salvo com sucesso.",
            "data": self.save_service.execute(t_ato_vinculoparte_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_ATO_VINCULOPARTE
    # ----------------------------------------------------
    def update(self, t_ato_vinculoparte_update_schema: TAtoVinculoParteUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_ato_vinculoparte_update_service", "TAtoVinculoParteUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_ATO_VINCULOPARTE atualizado com sucesso.",
            "data": self.update_service.execute(t_ato_vinculoparte_update_schema),
        }

    def update_texto_qualificacao(
        self, t_ato_vinculoparte_update_schema: TAtoVinculoParteTextoQualificacaoUpdateSchema
    ):
        update_service = self.dynamic_import.service(
            "t_ato_vinculoparte_update_texto_qualificacao_service",
            "TAtoVinculoParteUpdateTextoQualificacaoService",
        )
        self.update_service = update_service()
        return {
            "message": "Texto de qualificação atualizado com sucesso.",
            "data": self.update_service.execute(t_ato_vinculoparte_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_ATO_VINCULOPARTE
    # ----------------------------------------------------
    def delete(self, t_ato_vinculoparte_id_schema: TAtoVinculoParteIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_ato_vinculoparte_delete_service", "TAtoVinculoParteDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_ATO_VINCULOPARTE removido com sucesso.",
            "data": self.delete_service.execute(t_ato_vinculoparte_id_schema),
        }
