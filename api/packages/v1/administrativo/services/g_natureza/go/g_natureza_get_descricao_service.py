from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaDescricaoSchema
from packages.v1.administrativo.actions.g_natureza.g_natureza_get_by_descricao_action import GetByDescricaoAction

class GetByDescricaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_natureza pela sua descrição.
    """

    def execute(self, natureza_schema: GNaturezaDescricaoSchema, messageValidate: bool):
        """
        Executa a operação de busca no banco de dados.

        Args:
            natureza_schema (GNaturezaDescricaoSchema): O esquema com a descrição a ser buscada.
            messageValidate (bool): Se True, lança uma exceção HTTP caso o registro não seja encontrado.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento da ação
        show_action = GetByDescricaoAction()

        # Executa a ação em questão
        data = show_action.execute(natureza_schema)

        if messageValidate:
            
            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro de Natureza'
                )

        # Retorno da informação
        return data