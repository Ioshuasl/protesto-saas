from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIndexSchema,
    TAtoVinculoImovelSaveSchema,
    TAtoVinculoImovelUpdateSchema,
    TAtoVinculoImovelIdSchema,
)


class TAtoVinculoImovelController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_ATO_VINCULOIMOVEL,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.atos")
        self.dynamic_import.set_table("t_ato_vinculoimovel")

    # ----------------------------------------------------
    # Lista todos os registros de T_ATO_VINCULOIMOVEL
    # ----------------------------------------------------
    def index(self, data: TAtoVinculoImovelIndexSchema):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_ato_vinculoimovel_index_service", "TAtoVinculoImovelIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_ATO_VINCULOIMOVEL localizados com sucesso.",
            "data": self.index_service.execute(data),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_ATO_VINCULOIMOVEL pelo ID
    # ----------------------------------------------------
    def show(self, t_ato_vinculoimovel_id_schema: TAtoVinculoImovelIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_ato_vinculoimovel_show_service", "TAtoVinculoImovelShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_ATO_VINCULOIMOVEL localizado com sucesso.",
            "data": self.show_service.execute(t_ato_vinculoimovel_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_ATO_VINCULOIMOVEL
    # ----------------------------------------------------
    def save(self, t_ato_vinculoimovel_save_schema: TAtoVinculoImovelSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_ato_vinculoimovel_save_service", "TAtoVinculoImovelSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_ATO_VINCULOIMOVEL salvo com sucesso.",
            "data": self.save_service.execute(t_ato_vinculoimovel_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_ATO_VINCULOIMOVEL
    # ----------------------------------------------------
    def update(self, t_ato_vinculoimovel_update_schema: TAtoVinculoImovelUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_ato_vinculoimovel_update_service", "TAtoVinculoImovelUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_ATO_VINCULOIMOVEL atualizado com sucesso.",
            "data": self.update_service.execute(t_ato_vinculoimovel_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_ATO_VINCULOIMOVEL
    # ----------------------------------------------------
    def delete(self, t_ato_vinculoimovel_id_schema: TAtoVinculoImovelIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_ato_vinculoimovel_delete_service", "TAtoVinculoImovelDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_ATO_VINCULOIMOVEL removido com sucesso.",
            "data": self.delete_service.execute(t_ato_vinculoimovel_id_schema),
        }
