from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorIndexSchema,
    TAtoVinculoValorSaveSchema,
    TAtoVinculoValorUpdateSchema,
    TAtoVinculoValorIdSchema,
)


class TAtoVinculoValorController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_ATO_VINCULOVALOR,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.atos")
        self.dynamic_import.set_table("t_ato_vinculovalor")

    # ----------------------------------------------------
    # Lista todos os registros de T_ATO_VINCULOVALOR
    # ----------------------------------------------------
    def index(self, data: TAtoVinculoValorIndexSchema):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_ato_vinculovalor_index_service", "TAtoVinculoValorIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_ATO_VINCULOVALOR localizados com sucesso.",
            "data": self.index_service.execute(data),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_ATO_VINCULOVALOR pelo ID
    # ----------------------------------------------------
    def show(self, t_ato_vinculovalor_id_schema: TAtoVinculoValorIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_ato_vinculovalor_show_service", "TAtoVinculoValorShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_ATO_VINCULOVALOR localizado com sucesso.",
            "data": self.show_service.execute(t_ato_vinculovalor_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_ATO_VINCULOVALOR
    # ----------------------------------------------------
    def save(self, t_ato_vinculovalor_save_schema: TAtoVinculoValorSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_ato_vinculovalor_save_service", "TAtoVinculoValorSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_ATO_VINCULOVALOR salvo com sucesso.",
            "data": self.save_service.execute(t_ato_vinculovalor_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_ATO_VINCULOVALOR
    # ----------------------------------------------------
    def update(self, t_ato_vinculovalor_update_schema: TAtoVinculoValorUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_ato_vinculovalor_update_service", "TAtoVinculoValorUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_ATO_VINCULOVALOR atualizado com sucesso.",
            "data": self.update_service.execute(t_ato_vinculovalor_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_ATO_VINCULOVALOR
    # ----------------------------------------------------
    def delete(self, t_ato_vinculovalor_id_schema: TAtoVinculoValorIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_ato_vinculovalor_delete_service", "TAtoVinculoValorDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_ATO_VINCULOVALOR removido com sucesso.",
            "data": self.delete_service.execute(t_ato_vinculovalor_id_schema),
        }
