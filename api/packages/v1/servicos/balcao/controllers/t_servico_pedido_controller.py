from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoSaveSchema,
    TServicoPedidoSituacaoSchema,
    TServicoPedidoUpdateSchema,
    TServicoPedidoIdSchema,
)


class TServicoPedidoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_SERVICO_PEDIDO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.balcao")
        self.dynamic_import.set_table("t_servico_pedido")

    # ----------------------------------------------------
    # Lista todos os registros de T_SERVICO_PEDIDO
    # ----------------------------------------------------
    def index(self):
        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_servico_pedido_index_service", "TServicoPedidoIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_SERVICO_PEDIDO localizados com sucesso.",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_SERVICO_PEDIDO pelo ID
    # ----------------------------------------------------
    def show(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_servico_pedido_show_service", "TServicoPedidoShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_SERVICO_PEDIDO localizado com sucesso.",
            "data": self.show_service.execute(t_servico_pedido_id_schema),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_SERVICO_PEDIDO pelo ID
    # ----------------------------------------------------
    def show_recibo(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_servico_pedido_show_recibo_service", "TServicoPedidoShowReciboService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_SERVICO_PEDIDO localizado com sucesso.",
            "data": self.show_service.execute(t_servico_pedido_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_SERVICO_PEDIDO
    # ----------------------------------------------------
    def save(self, t_servico_pedido_save_schema: TServicoPedidoSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_servico_pedido_save_service", "TServicoPedidoSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_SERVICO_PEDIDO salvo com sucesso.",
            "data": self.save_service.execute(t_servico_pedido_save_schema),
        }

    # ----------------------------------------------------
    # Finalizar um pedido
    # ----------------------------------------------------
    def finalizar(self, data: TServicoPedidoIdSchema):

        # Importação da classe desejada
        finalizar_service = self.dynamic_import.service(
            "t_servico_pedido_finalizar_service",
            "TServicoPedidoFinalizarService",
        )

        # Instância da classe service
        self.finalizar_service = finalizar_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO finalizado com sucesso.",
            "data": self.finalizar_service.execute(data),
        }

    # ----------------------------------------------------
    # Cancela um pedido
    # ----------------------------------------------------
    def cancelar(self, data: TServicoPedidoSituacaoSchema):

        # Importação da classe desejada
        cancelar_service = self.dynamic_import.service(
            "t_servico_pedido_cancelar_service",
            "TServicoPedidoCancelarService",
        )

        # Instância da classe service
        self.cancelar_service = cancelar_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO cancelado com sucesso.",
            "data": self.cancelar_service.execute(data),
        }

    # ----------------------------------------------------
    # Ativa um pedido
    # ----------------------------------------------------
    def ativar(self, data: TServicoPedidoSituacaoSchema):

        # Importação da classe desejada
        ativar_service = self.dynamic_import.service(
            "t_servico_pedido_ativar_service",
            "TServicoPedidoAtivarService",
        )

        # Instância da classe service
        self.ativar_service = ativar_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO ativado com sucesso.",
            "data": self.ativar_service.execute(data),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_SERVICO_PEDIDO
    # ----------------------------------------------------
    def update(self, t_servico_pedido_update_schema: TServicoPedidoUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_servico_pedido_update_service", "TServicoPedidoUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_SERVICO_PEDIDO atualizado com sucesso.",
            "data": self.update_service.execute(t_servico_pedido_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_SERVICO_PEDIDO
    # ----------------------------------------------------
    def delete(self, t_servico_pedido_id_schema: TServicoPedidoIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_servico_pedido_delete_service", "TServicoPedidoDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_SERVICO_PEDIDO removido com sucesso.",
            "data": self.delete_service.execute(t_servico_pedido_id_schema),
        }

        # ----------------------------------------------------

    # Exclui um registro de T_SERVICO_PEDIDO
    # ----------------------------------------------------
    def load_params(self):

        # Importação da classe desejada
        load_params_service = self.dynamic_import.service(
            "t_servico_pedido_load_params_service", "TServicoPedidoLoadParamsService"
        )

        # Instância da classe service
        self.load_params_service = load_params_service()

        # Execução da exclusão
        return {
            "message": "Parâmetros de T_SERVICO_PEDIDO localizados com sucesso.",
            "data": self.load_params_service.execute(),
        }
