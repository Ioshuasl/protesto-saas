from packages.v1.administrativo.actions.t_censec_naturezatipo.t_censec_tiponatureza_save_action import (
    TCensecTipoNaturezaSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TCensecTipoNaturezaSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_CENSEC_TIPONATUREZA.
    """

    def execute(self, t_censec_tiponatureza_save_schema: TCensecTipoNaturezaSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            t_censec_tiponatureza_save_schema (TCensecTipoNaturezaSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not t_censec_tiponatureza_save_schema.censec_tiponatureza_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_CENSEC_TIPONATUREZA"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            t_censec_tiponatureza_save_schema.censec_tiponatureza_id = (
                sequencia.sequencia
            )

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        t_censec_tiponatureza_save_action = TCensecTipoNaturezaSaveAction()
        return t_censec_tiponatureza_save_action.execute(
            t_censec_tiponatureza_save_schema
        )
