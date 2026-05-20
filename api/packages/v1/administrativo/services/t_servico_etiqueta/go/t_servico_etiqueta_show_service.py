from fastapi import HTTPException, status

# Importação do Schema ajustada para o de ID
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import (
    TServicoEtiquetaIdSchema,
)

# Importação da Action ajustada para ShowAction
from packages.v1.administrativo.actions.t_servico_etiqueta.t_servico_etiqueta_show_action import (
    ShowAction,
)


class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_SERVICO_ETIQUETA pelo seu ID.
    """

    def execute(
        self, servico_etiqueta_schema: TServicoEtiquetaIdSchema
    ):  # Nome do parâmetro e tipo ajustados
        """
        Executa a operação de busca no banco de dados.

        Args:
            servico_etiqueta_schema (TServicoEtiquetaIdSchema): O esquema com o ID a ser buscado.
            messageValidate (bool): Se True, lança uma exceção HTTP caso o registro não seja encontrado.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento da ação
        show_action = ShowAction()  # Nome da Action ajustado

        # Executa a ação em questão
        data = show_action.execute(servico_etiqueta_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_SERVICO_ETIQUETA",  # Mensagem de erro ajustada
            )

        # Retorno da informação
        return data
