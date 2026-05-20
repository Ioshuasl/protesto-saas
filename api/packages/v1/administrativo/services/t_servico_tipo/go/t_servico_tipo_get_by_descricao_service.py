from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoDescricaoSchema # Importação do Schema ajustada
from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_get_by_descricao_action import GetByDescricaoAction # Importação da Action ajustada

class GetByDescricaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_SERVICO_TIPO pela sua descrição. # Nome da tabela ajustado
    """

    def execute(self, servico_tipo_schema: TServicoTipoDescricaoSchema, messageValidate: bool): # Nome do parâmetro e tipo ajustados
        """
        Executa a operação de busca no banco de dados.

        Args:
            servico_tipo_schema (TServicoTipoDescricaoSchema): O esquema com a descrição a ser buscada. # Nome do tipo ajustado
            messageValidate (bool): Se True, lança uma exceção HTTP caso o registro não seja encontrado.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento da ação
        show_action = GetByDescricaoAction()

        # Executa a ação em questão
        data = show_action.execute(servico_tipo_schema) # Nome do parâmetro ajustado

        if messageValidate:
            
            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro de T_SERVICO_TIPO' # Mensagem de erro ajustada
                )

        # Retorno da informação
        return data