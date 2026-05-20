from datetime import datetime
from packages.v1.servicos.balcao.actions.t_servico_pedido.t_servico_pedido_save_action import (
    TServicoPedidoSaveAction,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import (
    GenerateService,
)


class TServicoPedidoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_SERVICO_PEDIDO.
    """

    def execute(self, t_servico_pedido_save_schema: TServicoPedidoSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            t_servico_pedido_save_schema (TServicoPedidoSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not t_servico_pedido_save_schema.servico_pedido_id:
            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_SERVICO_PEDIDO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            t_servico_pedido_save_schema.servico_pedido_id = sequencia.sequencia

        # ----------------------------------------------------
        # Instanciamento e execução da Action de salvamento
        # ----------------------------------------------------
        t_servico_pedido_save_action = TServicoPedidoSaveAction()

        # Verifica se tem a data do pedido
        if t_servico_pedido_save_schema.data_pedido is None:

            # Obtem a data e hora atual
            t_servico_pedido_save_schema.data_pedido = datetime.now()

        # Obtenho a resposta da operação
        response_pedido = t_servico_pedido_save_action.execute(
            t_servico_pedido_save_schema
        )

        return response_pedido
