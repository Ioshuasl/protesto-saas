from decimal import Decimal
from typing import Optional

from packages.v1.servicos.atos.actions.t_ato_vinculovalor.t_ato_vinculovalor_update_action import (
    TAtoVinculoValorUpdateAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorUpdateSchema,
)
from packages.v1.administrativo.schemas.g_calculo_schema import GCalculoServico
from packages.v1.administrativo.services.g_calculo.go.g_calculo_servico_service import (
    GCalculoServicoService,
)


class TAtoVinculoValorUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO_VINCULOVALOR.
    """

    def execute(self, t_ato_vinculovalor_update_schema: TAtoVinculoValorUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_ato_vinculovalor_update_schema (TAtoVinculoValorUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Cálculo de emolumentos antes de atualizar
        # ----------------------------------------------------
        self._preencher_valores_calculados(t_ato_vinculovalor_update_schema)

        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculovalor_update_action = TAtoVinculoValorUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_ato_vinculovalor_update_action.execute(
            t_ato_vinculovalor_update_schema
        )

    def _preencher_valores_calculados(
        self, schema: TAtoVinculoValorUpdateSchema
    ) -> None:
        """
        Chama o serviço de cálculo (G_CALCULO /servico) e preenche os campos
        calculados no schema de T_ATO_VINCULOVALOR antes da atualização.
        """

        sistema_id: Optional[Decimal] = getattr(schema, "sistema_id", None)
        emolumento_id: Optional[Decimal] = schema.emolumento_id
        valor_documento: Optional[Decimal] = schema.valor_documento
        quantidade: Optional[Decimal] = schema.quantidade

        if not all([sistema_id, emolumento_id, valor_documento, quantidade]):
            return

        calculo_service = GCalculoServicoService()

        calculo_schema = GCalculoServico(
            sistema_id=float(sistema_id),
            emolumento_id=float(emolumento_id),
            codigo_tabela=0.0,
            valor_documento=valor_documento,
            quantidade=quantidade,
        )

        resultado = calculo_service.execute(calculo_schema)

        schema.emolumento = resultado.valor_emolumento
        schema.taxa_judiciaria = resultado.valor_taxa_judiciaria
        schema.valor_iss = resultado.valor_iss
        schema.fundesp = resultado.valor_fundos
        schema.valor_total = resultado.valor_total
        schema.emolumento_item_id = resultado.emolumento_item_id
