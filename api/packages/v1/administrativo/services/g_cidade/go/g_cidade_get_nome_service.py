from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeNomeSchema
from packages.v1.administrativo.actions.g_cidade.g_cidade_get_by_nome_action import GetByNomeAction

class GetByNomeService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_CIDADE pelo nome da cidade (CIDADE_NOME).
    """

    def execute(self, g_cidade_schema: GCidadeNomeSchema, messageValidate: bool):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_cidade_schema (GCidadeNomeSchema): O esquema com o nome da cidade a ser buscada.
            messageValidate (bool): Se True, lança uma exceção HTTP caso o registro não seja encontrado.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento da ação
        show_action = GetByNomeAction()

        # Executa a ação em questão
        data = show_action.execute(g_cidade_schema)

        if messageValidate:
            
            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro de CIDADE'
                )

        # Retorno da informação
        return data