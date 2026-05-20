from packages.v1.servicos.atos.actions.t_ato_tipo.t_ato_tipo_save_action import (
    TAtoTipoSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TAtoTipoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_ATO_TIPO.
    """

    def execute(self, t_ato_tipo_save_schema: TAtoTipoSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            t_ato_tipo_save_schema (TAtoTipoSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not t_ato_tipo_save_schema.ato_tipo_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_ATO_TIPO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            t_ato_tipo_save_schema.ato_tipo_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        t_ato_tipo_save_action = TAtoTipoSaveAction()
        return t_ato_tipo_save_action.execute(t_ato_tipo_save_schema)
