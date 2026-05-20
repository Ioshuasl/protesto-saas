from packages.v1.servicos.balcao.actions.t_pessoa_cartao.t_pessoa_cartao_save_action import (
    TPessoaCartaoSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import (
    GenerateService,
)


class TPessoaCartaoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_PESSOA_CARTAO.
    """

    def execute(self, data: TPessoaCartaoSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            data (TPessoaCartaoSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not data.pessoa_cartao_id:

            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_PESSOA_CARTAO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            data.pessoa_cartao_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        save_action = TPessoaCartaoSaveAction()
        return save_action.execute(data)
