from packages.v1.administrativo.actions.g_cartorio.g_cartorio_save_action import (
    GCartorioSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioSaveSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class GCartorioSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela G_GRAMATICA.
    """

    def execute(self, g_cartorio_save_schema: GCartorioSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            g_cartorio_save_schema (GCartorioSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not g_cartorio_save_schema.cartorio_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "G_CARTORIO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            g_cartorio_save_schema.cartorio_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        g_cartorio_save_action = GCartorioSaveAction()
        return g_cartorio_save_action.execute(g_cartorio_save_schema)
