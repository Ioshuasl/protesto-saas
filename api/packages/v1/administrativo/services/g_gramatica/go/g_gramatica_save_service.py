from packages.v1.administrativo.actions.g_gramatica.g_gramatica_save_action import (
    GGramaticaSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaSaveSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class GGramaticaSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela G_GRAMATICA.
    """

    def execute(self, g_gramatica_save_schema: GGramaticaSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            g_gramatica_save_schema (GGramaticaSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not g_gramatica_save_schema.gramatica_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "G_GRAMATICA"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            g_gramatica_save_schema.gramatica_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        g_gramatica_save_action = GGramaticaSaveAction()
        return g_gramatica_save_action.execute(g_gramatica_save_schema)
