from fastapi import HTTPException, status

# Importação do Schema ajustada
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIdSchema,
)

# Importação da Action ajustada
from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_show_action import (
    ShowAction,
)


class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_SERVICO_TIPO.
    """

    def execute(
        self, servico_tipo_schema: TServicoTipoIdSchema
    ):  # Nome do parâmetro e tipo ajustados
        """
        Executa a operação de busca no banco de dados.

        Args:
            servico_tipo_schema (TServicoTipoIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(servico_tipo_schema)  # Parâmetro ajustado

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_SERVICO_TIPO",  # Mensagem de erro ajustada
            )

        # Retorno da informação
        return data
