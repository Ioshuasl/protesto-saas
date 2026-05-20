from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroDescricaoSchema
from packages.v1.administrativo.actions.g_tb_tipologradouro.g_tb_tipologradouro_get_by_descricao_action import GetByDescricaoAction

class GetByDescricaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_tipologradouro pela sua descrição.
    """

    def execute(self, tipologradouro_schema: GTbTipoLogradouroDescricaoSchema, messageValidate: bool):
        """
        Executa a operação de busca no banco de dados.

        Args:
            tipologradouro_schema (GTbTipoLogradouroDescricaoSchema): O esquema com a descrição a ser buscada.
            messageValidate (bool): Se True, lança uma exceção HTTP caso o registro não seja encontrado.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento da ação
        show_action = GetByDescricaoAction()

        # Executa a ação em questão
        data = show_action.execute(tipologradouro_schema)

        if messageValidate:
            
            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro de G_TB_TIPOLOGRADOURO'
                )

        # Retorno da informação
        return data