from packages.v1.administrativo.actions.g_ibge_pais.g_ibge_pais_save_action import (
    GIbgePaisSaveAction,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class GIbgePaisSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela {{ entity_upper }}.
    """

    def execute(self, g_ibge_pais_save_schema: GIbgePaisSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            g_ibge_pais_save_schema (GIbgePaisSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not g_ibge_pais_save_schema.ibge_pais_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "G_IBGE_PAIS"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            g_ibge_pais_save_schema.ibge_pais_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        g_ibge_pais_save_action = GIbgePaisSaveAction()
        return g_ibge_pais_save_action.execute(g_ibge_pais_save_schema)
