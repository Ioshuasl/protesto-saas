from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa_representante.t_pessoa_representante_show_action import (
    TPessoaRepresentanteShowAction,
)
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteIdSchema,
)


class TPessoaRepresentanteShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_representante_id_schema: TPessoaRepresentanteIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            regimebens_schema (GTbRegimebensIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        t_pessoa_representante_show_action = TPessoaRepresentanteShowAction()

        # Executa a ação em questão
        data = t_pessoa_representante_show_action.execute(
            t_pessoa_representante_id_schema
        )

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possivel localizar a pessoa desejada",
            )

        # Retorno da informação
        return data
