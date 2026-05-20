from fastapi import HTTPException, status

from packages.v1.administrativo.services.g_usuario.go.g_usuario_delete_service import (
    SequenciaDeleteService,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.servicos.balcao.actions.t_pessoa_cartao.t_pessoa_cartao_delete_action import (
    TPessoaCartaoDeleteAction,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIdSchema,
)


class TPessoaCartaoDeleteService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_PESSOA_CARTAO.
    """

    def execute(self, data: TPessoaCartaoIdSchema):
        """
        Executa a operação de exclusão do registro no banco de dados.

        Args:
            data (TPessoaCartaoIdSchema):
                O esquema com o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        delete_action = TPessoaCartaoDeleteAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        response = delete_action.execute(data)

        # 3. Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if response:

            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()

            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=data.usuario_id, tabela="G_USUARIO"
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)

            return response

        # 4. Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe.",
        )
