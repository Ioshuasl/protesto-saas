from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaDescricaoSchema
from packages.v1.administrativo.actions.t_minuta.t_minuta_get_by_descricao_action import GetByDescricaoAction

class GetByDescricaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_minuta pela sua descrição.
    """

    def execute(self, minuta_schema: TMinutaDescricaoSchema, messageValidate: bool):
        """
        Executa a operação de busca no banco de dados.

        Args:
            minuta_schema (TMinutaDescricaoSchema): O esquema com a descrição a ser buscada.
            messageValidate (bool): Se True, lança uma exceção HTTP caso o registro não seja encontrado.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento da ação
        show_action = GetByDescricaoAction()

        # Executa a ação em questão
        data = show_action.execute(minuta_schema)

        if messageValidate:
            
            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro de MINUTA'
                )

        # Retorno da informação
        return data