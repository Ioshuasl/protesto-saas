from packages.v1.administrativo.actions.g_selo_grupo.g_selo_grupo_save_action import (
    GSeloGrupoSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.g_selo_grupo_schema import GSeloGrupoSaveSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class GSeloGrupoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela G_SELO_GRUPO.
    """

    def execute(self, g_selo_grupo_save_schema: GSeloGrupoSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            g_selo_grupo_save_schema (GSeloGrupoSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not g_selo_grupo_save_schema.selo_grupo_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "G_SELO_GRUPO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            g_selo_grupo_save_schema.selo_grupo_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        g_selo_grupo_save_action = GSeloGrupoSaveAction()
        return g_selo_grupo_save_action.execute(g_selo_grupo_save_schema)
