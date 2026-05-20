from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoIndexSchema,
    TAtoAndamentoSaveSchema,
    TAtoAndamentoUpdateSchema,
    TAtoAndamentoIdSchema,
)


class TAtoAndamentoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_ATO_ANDAMENTO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.atos")
        self.dynamic_import.set_table("t_ato_andamento")

    # ----------------------------------------------------
    # Lista todos os registros de T_ATO_ANDAMENTO
    # ----------------------------------------------------
    def index(self, data: TAtoAndamentoIndexSchema):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_ato_andamento_index_service", "TAtoAndamentoIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_ATO_ANDAMENTO localizados com sucesso.",
            "data": self.index_service.execute(data),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_ATO_ANDAMENTO pelo ID
    # ----------------------------------------------------
    def show(self, t_ato_andamento_id_schema: TAtoAndamentoIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_ato_andamento_show_service", "TAtoAndamentoShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_ATO_ANDAMENTO localizado com sucesso.",
            "data": self.show_service.execute(t_ato_andamento_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_ATO_ANDAMENTO
    # ----------------------------------------------------
    def save(self, t_ato_andamento_save_schema: TAtoAndamentoSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_ato_andamento_save_service", "TAtoAndamentoSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_ATO_ANDAMENTO salvo com sucesso.",
            "data": self.save_service.execute(t_ato_andamento_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_ATO_ANDAMENTO
    # ----------------------------------------------------
    def update(self, t_ato_andamento_update_schema: TAtoAndamentoUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_ato_andamento_update_service", "TAtoAndamentoUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_ATO_ANDAMENTO atualizado com sucesso.",
            "data": self.update_service.execute(t_ato_andamento_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_ATO_ANDAMENTO
    # ----------------------------------------------------
    def delete(self, t_ato_andamento_id_schema: TAtoAndamentoIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_ato_andamento_delete_service", "TAtoAndamentoDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_ATO_ANDAMENTO removido com sucesso.",
            "data": self.delete_service.execute(t_ato_andamento_id_schema),
        }
