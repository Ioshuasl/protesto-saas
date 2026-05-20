from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.actions.t_censec_qualidadeato.t_censec_qualidadeato_save_action import (
    TCensecQualidadeAtoSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TCensecQualidadeAtoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_CENSEC_QUALIDADEATO.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicializa o DynamicImport para permitir injeção dinâmica
        # de pacotes, conforme o padrão do sistema.
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_censec_qualidadeato")

    def execute(self, t_censec_qualidadeato_save_schema: TCensecQualidadeAtoSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            t_censec_qualidadeato_save_schema (TCensecQualidadeAtoSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not t_censec_qualidadeato_save_schema.censec_qualidadeato_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_CENSEC_QUALIDADEATO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            t_censec_qualidadeato_save_schema.censec_qualidadeato_id = (
                sequencia.sequencia
            )

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        t_censec_qualidadeato_save_action = TCensecQualidadeAtoSaveAction()
        return t_censec_qualidadeato_save_action.execute(
            t_censec_qualidadeato_save_schema
        )
