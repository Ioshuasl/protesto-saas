from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelIndexSchema,
    TAtoParteImovelSaveSchema,
    TAtoParteImovelUpdateSchema,
    TAtoParteImovelIdSchema,
)


class TAtoParteImovelController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_ATO_PARTEIMOVEL,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.atos")
        self.dynamic_import.set_table("t_ato_parteimovel")

    # ----------------------------------------------------
    # Lista todos os registros de T_ATO_PARTEIMOVEL
    # ----------------------------------------------------
    def index(self, data: TAtoParteImovelIndexSchema):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_ato_parteimovel_index_service", "TAtoParteImovelIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_ATO_PARTEIMOVEL localizados com sucesso.",
            "data": self.index_service.execute(data),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_ATO_PARTEIMOVEL pelo ID
    # ----------------------------------------------------
    def show(self, t_ato_parteimovel_id_schema: TAtoParteImovelIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_ato_parteimovel_show_service", "TAtoParteImovelShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_ATO_PARTEIMOVEL localizado com sucesso.",
            "data": self.show_service.execute(t_ato_parteimovel_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_ATO_PARTEIMOVEL
    # ----------------------------------------------------
    def save(self, t_ato_parteimovel_save_schema: TAtoParteImovelSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_ato_parteimovel_save_service", "TAtoParteImovelSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_ATO_PARTEIMOVEL salvo com sucesso.",
            "data": self.save_service.execute(t_ato_parteimovel_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_ATO_PARTEIMOVEL
    # ----------------------------------------------------
    def update(self, t_ato_parteimovel_update_schema: TAtoParteImovelUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_ato_parteimovel_update_service", "TAtoParteImovelUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_ATO_PARTEIMOVEL atualizado com sucesso.",
            "data": self.update_service.execute(t_ato_parteimovel_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_ATO_PARTEIMOVEL
    # ----------------------------------------------------
    def delete(self, t_ato_parteimovel_id_schema: TAtoParteImovelIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_ato_parteimovel_delete_service", "TAtoParteImovelDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_ATO_PARTEIMOVEL removido com sucesso.",
            "data": self.delete_service.execute(t_ato_parteimovel_id_schema),
        }
