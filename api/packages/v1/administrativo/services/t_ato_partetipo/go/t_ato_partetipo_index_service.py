from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_ato_partetipo.t_ato_partetipo_index_action import (
    TAtoParteTipoIndexAction,
)


class TAtoParteTipoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela t_censec_qualidade.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        t_ato_partetipo_index_action = TAtoParteTipoIndexAction()

        # Executa a busca de todas as ações
        data = t_ato_partetipo_index_action.execute()

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar os registros de T_IMOVEL_UNIDADE",
            )

        # Retorna as informações localizadas
        return data
