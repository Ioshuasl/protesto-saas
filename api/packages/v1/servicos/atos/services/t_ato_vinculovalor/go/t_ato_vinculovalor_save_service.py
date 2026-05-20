from datetime import datetime
from decimal import Decimal
from typing import Optional

from packages.v1.servicos.atos.actions.t_ato_vinculovalor.t_ato_vinculovalor_save_action import (
    TAtoVinculoValorSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.atos.schemas.t_historico_schema import THistoricoSaveSchema
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorSaveSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_save_service import (
    THistoricoSaveService,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.administrativo.schemas.g_calculo_schema import GCalculoServico
from packages.v1.administrativo.services.g_calculo.go.g_calculo_servico_service import (
    GCalculoServicoService,
)


class TAtoVinculoValorSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_ATO_VINCULOVALOR.
    """

    def execute(self, t_ato_vinculovalor_save_schema: TAtoVinculoValorSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            t_ato_vinculovalor_save_schema (TAtoVinculoValorSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Cálculo de emolumentos antes de gerar o ID e salvar
        # ----------------------------------------------------
        self._preencher_valores_calculados(t_ato_vinculovalor_save_schema)

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not t_ato_vinculovalor_save_schema.ato_vinculovalor_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_ATO_VINCULOVALOR"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            t_ato_vinculovalor_save_schema.ato_vinculovalor_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        t_ato_vinculovalor_save_action = TAtoVinculoValorSaveAction()
        ato_vinculovalor_response = t_ato_vinculovalor_save_action.execute(
            t_ato_vinculovalor_save_schema
        )

        # ----------------------------------------------------
        # Grava histórico de inclusão do vínculo de valor
        # ----------------------------------------------------
        now = datetime.now()
        now_br = now.strftime("%d/%m/%Y %H:%M:%S")
        usuario_id = t_ato_vinculovalor_save_schema.usuario_id
        ato_vinculovalor_id = getattr(
            ato_vinculovalor_response,
            "ato_vinculovalor_id",
            t_ato_vinculovalor_save_schema.ato_vinculovalor_id,
        )

        historico_schema = THistoricoSaveSchema(
            tabela="T_ATO_VINCULOVALOR",
            campo="Cadastro de vínculo de valor",
            operacao="I",
            new_value=None,
            usuario_id=usuario_id,
            data=now,
            id=ato_vinculovalor_id,
            observacao=f"Vínculo de valor cadastrado pelo usuário({usuario_id}), no dia {now_br}",
            data_registro=None,
            dados_complementares=None,
        )

        t_historico_save_service = THistoricoSaveService()
        t_historico_save_service.execute(historico_schema)

        return ato_vinculovalor_response

    def _preencher_valores_calculados(
        self, schema: TAtoVinculoValorSaveSchema
    ) -> None:
        """
        Chama o serviço de cálculo (G_CALCULO /servico) e preenche os campos
        calculados no schema de T_ATO_VINCULOVALOR.
        """

        # Campos mínimos necessários para o cálculo
        sistema_id: Optional[Decimal] = getattr(schema, "sistema_id", None)
        emolumento_id: Optional[Decimal] = schema.emolumento_id
        valor_documento: Optional[Decimal] = schema.valor_documento
        quantidade: Optional[Decimal] = schema.quantidade

        if not all([sistema_id, emolumento_id, valor_documento, quantidade]):
            # Sem dados suficientes, não aplica cálculo automático
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

        # Preenche campos calculados em T_ATO_VINCULOVALOR
        schema.emolumento = resultado.valor_emolumento
        schema.taxa_judiciaria = resultado.valor_taxa_judiciaria
        schema.valor_iss = resultado.valor_iss
        schema.fundesp = resultado.valor_fundos
        schema.valor_total = resultado.valor_total
        schema.emolumento_item_id = resultado.emolumento_item_id
