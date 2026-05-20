from __future__ import annotations

from decimal import Decimal
from typing import Optional

from actions.values.values import Values
from packages.v1.administrativo.actions.g_emolumento_item.g_emolumento_item_get_faixa_valor_action import (
    GEmolumentoItemGetFaixaValorAction,
)
from packages.v1.administrativo.schemas.g_calculo_schema import (
    GCalculoRapidoSchema,
    ResponseGCalculoRapidoSchema,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemIndexSchema,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import GEmolumentoIdSchema
from packages.v1.administrativo.services.g_emolumento.go.g_emolumento_show_service import (
    GEmolumentoShowService,
)
from packages.v1.administrativo.services.g_emolumento_item.go.g_emolumento_item_index_service import (
    GEmolumentoItemIndexService,
)
from packages.v1.parametros.schemas.g_config_schema import GConfigNomeSchema
from packages.v1.parametros.services.g_config.g_config_show_by_nome_service import (
    GConfigShowByNomeService,
)


class GCalculoRapidoService:
    """
    Cálculo rápido de emolumentos + taxas.
    - Usa DI para serviços (facilita teste/mocks).
    - Centraliza leitura de configs/percentuais.
    - Normaliza moeda com quantize (por padrão 3 casas, conforme NUMERIC(14,3)).
    """

    def __init__(
        self,
        config_service: Optional[GConfigShowByNomeService] = None,
        emolumento_show_service: Optional[GEmolumentoShowService] = None,
        emolumento_item_index_service: Optional[GEmolumentoItemIndexService] = None,
        emolumento_item_get_faixa_valor_action: Optional[
            GEmolumentoItemGetFaixaValorAction
        ] = None,
        scale: str = "0.01",  # 3 casas decimais (ex.: Firebird NUMERIC(14,3))
    ) -> None:
        self._config_service = config_service or GConfigShowByNomeService()
        self._emolumento_show_service = (
            emolumento_show_service or GEmolumentoShowService()
        )
        self._emolumento_item_index_service = (
            emolumento_item_index_service or GEmolumentoItemIndexService()
        )
        self._emolumento_item_get_faixa_valor_action = (
            emolumento_item_get_faixa_valor_action
            or GEmolumentoItemGetFaixaValorAction()
        )
        self._scale = Decimal(scale)

    def execute(self, data: GCalculoRapidoSchema) -> ResponseGCalculoRapidoSchema:

        # Busca os parâmetros da aplicação
        periodo_id = float(
            self._config_service.execute(
                GConfigNomeSchema(nome="PERIODO_PADRAO", sistema_id=2)
            ).valor
        )

        # Gerar o percentual do iss de acordo com o parâmetro
        percentual_iss = Values.percent(
            Decimal(
                self._config_service.execute(
                    GConfigNomeSchema(nome="PERCENTUAL_ISS", sistema_id=5)
                ).valor
            ),
            100,
        )

        # Gerar o percentual do iss de acordo com o parâmetro
        percentual_fundos = Values.percent(
            Decimal(
                self._config_service.execute(
                    GConfigNomeSchema(nome="PERCENTUAL_FUNDOS_ESTADUAIS", sistema_id=5)
                ).valor
            ),
            100,
        )

        # Busca o emolumento desejado
        emolumento = self._emolumento_show_service.execute(
            GEmolumentoIdSchema(emolumento_id=data.emolumento_id)
        )

        # Busca os itens do emolumento
        emolumento_itens = self._emolumento_item_index_service.execute(
            GEmolumentoItemIndexSchema(
                emolumento_id=float(emolumento.emolumento_id),
                emolumento_periodo_id=periodo_id,
            )
        )

        # Se vier lista, usa o primeiro (ou ajuste a regra aqui, se necessário)
        emolumento_item = self._emolumento_item_get_faixa_valor_action.execute(
            emolumento_itens, Decimal(data.valor_documento)
        )

        # Converter o valor para decimal
        quantidade = Decimal(data.quantidade)

        # Cálculos
        emolumento_total = Values.money(
            self._scale, (emolumento_item.valor_emolumento * quantidade)
        )

        taxa_judiciaria_total = Values.money(
            self._scale, (emolumento_item.valor_taxa_judiciaria * quantidade)
        )

        iss_total = Values.money(
            self._scale,
            (emolumento_item.valor_emolumento * percentual_iss * quantidade),
        )

        fundos_total = Values.money(
            self._scale,
            (emolumento_item.valor_emolumento * percentual_fundos * quantidade),
        )

        total = Values.money(
            self._scale,
            (emolumento_total + taxa_judiciaria_total + iss_total + fundos_total),
        )

        # Resposta
        return ResponseGCalculoRapidoSchema(
            apresentante=data.apresentante,
            observacao=data.observacao,
            emolumento_id=float(data.emolumento_id),
            valor_documento=float(data.valor_documento),
            valor_emolumento=emolumento_total,
            valor_taxa_judiciaria=taxa_judiciaria_total,
            valor_iss=iss_total,
            valor_fundos=fundos_total,
            valor_total=total,
        )
