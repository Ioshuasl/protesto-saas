from packages.v1.administrativo.actions.g_natureza_titulo.g_natureza_titulo_save_action import (
    GNaturezaTituloSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class GNaturezaTituloSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self, g_natureza_titulo_save_schema: GNaturezaTituloSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            g_natureza_titulo_save_schema (GNaturezaTituloSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not g_natureza_titulo_save_schema.natureza_titulo_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "G_NATUREZA_TITULO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            g_natureza_titulo_save_schema.natureza_titulo_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        g_natureza_titulo_save_action = GNaturezaTituloSaveAction()
        return g_natureza_titulo_save_action.execute(g_natureza_titulo_save_schema)
