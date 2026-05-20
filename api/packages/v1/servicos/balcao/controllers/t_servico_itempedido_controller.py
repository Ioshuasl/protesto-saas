from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
    TServicoItemPedidoCertidaoSaveSchema,
    TServicoItemPedidoIdSchema,
    TServicoItemPedidoQuantidadeSchema,
    TServicoItemPedidoSaveSchema,
    TServicoItemPedidoSituacaoSchema,
    TServicoItemPedidoUpdateSchema,
)


class TServicoItemPedidoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.balcao")
        self.dynamic_import.set_table("t_servico_itempedido")

    def index(self, data: TServicoItemIndexSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_index_service", "TServicoItemPedidoIndexService"
        )

        return {
            "message": "Registros de T_SERVICO_ITEMPEDIDO localizados com sucesso.",
            "data": service().execute(data),
        }

    def selos_livres(self, data: TServicoItemIndexSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_selos_livres_service",
            "TServicoItemPedidoSelosLivresService",
        )

        return {
            "message": "Selos livres de T_SERVICO_ITEMPEDIDO localizados com sucesso.",
            "data": service().execute(data),
        }

    def show(self, data: TServicoItemPedidoIdSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_show_service", "TServicoItemPedidoShowService"
        )

        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO localizado com sucesso.",
            "data": service().execute(data),
        }

    def certidao_show(self, data: TServicoItemPedidoIdSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_certidao_show_service",
            "TServicoItemPedidoCertidaoShowService",
        )

        return {
            "message": "Certidao de T_SERVICO_ITEMPEDIDO localizada com sucesso.",
            "data": service().execute(data),
        }

    def certidao_edit(self, data: TServicoItemPedidoIdSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_certidao_edit_service",
            "TServicoItemPedidoCertidaoEditService",
        )

        return {
            "message": "Certidao de T_SERVICO_ITEMPEDIDO preparada com sucesso.",
            "data": service().execute(data),
        }

    def certidao_save(self, data: TServicoItemPedidoCertidaoSaveSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_certidao_save_service",
            "TServicoItemPedidoCertidaoSaveService",
        )

        return service().execute(data)

    def save(self, data: TServicoItemPedidoSaveSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_save_service", "TServicoItemPedidoSaveService"
        )

        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO salvo com sucesso.",
            "data": service().execute(data),
        }

    def cancelar(self, data: TServicoItemPedidoSituacaoSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_cancelar_service", "TServicoItemPedidoCancelarService"
        )

        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO cancelado com sucesso.",
            "data": service().execute(data),
        }

    def ativar(self, data: TServicoItemPedidoSituacaoSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_ativar_service",
            "TServicoItemPedidoAtivarService",
        )

        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO ativado com sucesso.",
            "data": service().execute(data),
        }

    def update(self, data: TServicoItemPedidoUpdateSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_update_service", "TServicoItemPedidoUpdateService"
        )

        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO atualizado com sucesso.",
            "data": service().execute(data),
        }

    def delete(self, data: TServicoItemPedidoIdSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_delete_service", "TServicoItemPedidoDeleteService"
        )

        return {
            "message": "Registro de T_SERVICO_ITEMPEDIDO removido com sucesso.",
            "data": service().execute(data),
        }

    def quantidade_atualizar(self, data: TServicoItemPedidoQuantidadeSchema):
        service = self.dynamic_import.service(
            "t_servico_itempedido_quantidade_atualizar_service",
            "TServicoItemPedidoQuantidadeAtualizarService",
        )

        return {
            "message": "Quantidade de T_SERVICO_ITEMPEDIDO atualizada com sucesso.",
            "data": service().execute(data),
        }
