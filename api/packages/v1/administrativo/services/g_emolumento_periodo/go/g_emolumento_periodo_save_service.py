from packages.v1.administrativo.actions.g_emolumento_periodo.g_emolumento_periodo_save_action import (
    GEmolumentoPeriodoSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import (
    GenerateService,
)


class GEmolumentoPeriodoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela G_EMOLUMENTO_PERIODO.
    """

    def execute(self, g_emolumento_periodo_save_schema: GEmolumentoPeriodoSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            g_emolumento_periodo_save_schema (GEmolumentoPeriodoSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not g_emolumento_periodo_save_schema.emolumento_periodo_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "G_EMOLUMENTO_PERIODO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            g_emolumento_periodo_save_schema.emolumento_periodo_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        g_emolumento_periodo_save_action = GEmolumentoPeriodoSaveAction()
        return g_emolumento_periodo_save_action.execute(
            g_emolumento_periodo_save_schema
        )
