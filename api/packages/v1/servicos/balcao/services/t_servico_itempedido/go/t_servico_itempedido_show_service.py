from packages.v1.resolver.schemas.resolver_schema import ResolverSchema
from packages.v1.resolver.services.resolver_main_service import ResolverMainService
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_show_action import (
    TServicoItemPedidoShowAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
)
from fastapi import HTTPException, status


class TServicoItemPedidoShowService:

    def execute(self, data: TServicoItemPedidoIdSchema):
        # Execução da ação
        data = TServicoItemPedidoShowAction().execute(data)
        # Verificação de resultado
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_SERVICO_ITEMPEDIDO.",
            )

        if getattr(data, "situacao", None) == "F":

            # Certidão
            if data.etiqueta_texto and data.tipo_item == "C":

                # Executa
                resolver_main_service_response = ResolverMainService().execute(
                    ResolverSchema(
                        id=data.servico_itempedido_id,
                        campo_id_valor=data.servico_itempedido_id,
                        sitema_id=2,
                        texto=data.etiqueta_texto,
                    )
                )

                data.etiqueta_texto = resolver_main_service_response

            # Autenitcação
            if data.etiqueta_texto and data.tipo_item == "A":

                # Executa
                resolver_main_service_response = ResolverMainService().execute(
                    ResolverSchema(
                        id=data.servico_itempedido_id,
                        campo_id_valor=data.servico_itempedido_id,
                        sitema_id=2,
                        texto=data.etiqueta_texto,
                    )
                )

                data.etiqueta_texto = resolver_main_service_response

            # Reconhecimento de firma
            if data.etiqueta_texto and data.tipo_item == "R":

                # Executa
                resolver_main_service_response = ResolverMainService().execute(
                    ResolverSchema(
                        id=data.servico_itempedido_id,
                        campo_id_valor=data.servico_itempedido_id,
                        sitema_id=2,
                        texto=data.etiqueta_texto,
                    )
                )

                data.etiqueta_texto = resolver_main_service_response

            # Abono
            if data.etiqueta_texto and data.tipo_item == "B":

                # Executa
                resolver_main_service_response = ResolverMainService().execute(
                    ResolverSchema(
                        id=data.servico_itempedido_id,
                        campo_id_valor=data.servico_itempedido_id,
                        sitema_id=2,
                        texto=data.etiqueta_texto,
                    )
                )

                data.etiqueta_texto = resolver_main_service_response

            # Cartão de Assinatura
            if data.etiqueta_texto and data.tipo_item == "CA":

                # Executa
                resolver_main_service_response = ResolverMainService().execute(
                    ResolverSchema(
                        id=data.servico_itempedido_id,
                        campo_id_valor=data.pessoa_id,
                        sitema_id=2,
                        texto=data.etiqueta_texto,
                    )
                )

                data.etiqueta_texto = resolver_main_service_response

        else:

            data.etiqueta_texto = None
            data.certidao_texto = None
        return data
