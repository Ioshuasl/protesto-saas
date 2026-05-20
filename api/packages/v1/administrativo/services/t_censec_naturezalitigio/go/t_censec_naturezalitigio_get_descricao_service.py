from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioDescricaoSchema
from packages.v1.administrativo.actions.t_censec_naturezalitigio.t_censec_naturezalitigio_get_by_descricao_action import GetByDescricaoAction

class GetByDescricaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec_naturezalitigio pela sua descrição.
    """

    def execute(self, censec_naturezalitigio_schema: TCensecNaturezalitigioDescricaoSchema, messageValidate: bool):
        """
        Executa a operação de busca no banco de dados.

        Args:
            censec_naturezalitigio_schema (TCensecNaturezalitigioDescricaoSchema): O esquema com a descrição a ser buscada.
            messageValidate (bool): Se True, lança uma exceção HTTP caso o registro não seja encontrado.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento da ação
        show_action = GetByDescricaoAction()

        # Executa a ação em questão
        data = show_action.execute(censec_naturezalitigio_schema)

        if messageValidate:
            
            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro de CENSEC_NATUREZALITIGIO'
                )

        # Retorno da informação
        return data