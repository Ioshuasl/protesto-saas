from datetime import datetime
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.balcao.actions.t_pessoa_cartao.t_pessoa_cartao_show_ultimo_pedido_action import (
    TPessoaCartaoShoUltimoPedidoAction,
)
from packages.v1.servicos.balcao.actions.t_pessoa_cartao.t_pessoa_cartao_update_action import (
    TPessoaCartaoUpdateAction,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
    TPessoaCartaoUpdateSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import (
    GenerateService,
)


class TPessoaCartaoFinalizarService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_PESSOA_CARTAO.
    """

    def execute(self, data: TPessoaCartaoUpdateSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            data (TPessoaCartaoSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # localiza o ultimo pedido de cartao da pessoa
        data = TPessoaCartaoShoUltimoPedidoAction().execute(
            TPessoaCartaoIndexchema(pessoa_id=data.pessoa_id)
        )

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not data.numero:

            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_CARTAO_NUMERO"
            sequencia_schema.contador = True

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            data.numero = sequencia.sequencia

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not data.data_abertura:

            # Atualiza o ID no schema
            data.data_abertura = datetime.now()

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not data.situacao:

            # Atualiza o ID no schema
            data.situacao = "A"

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        return TPessoaCartaoUpdateAction().execute(
            TPessoaCartaoUpdateSchema(
                situacao=data.situacao,
                data_abertura=data.data_abertura,
                pessoa_cartao_id=data.pessoa_cartao_id,
                numero=data.numero,
            )
        )
