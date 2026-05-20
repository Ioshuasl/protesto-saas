from abstracts.repository import BaseRepository
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
)


class TPessoaCartaoIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, t_pessoa_cartao_index_schema: TPessoaCartaoIndexchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT * FROM T_PESSOA_CARTAO
                    WHERE PESSOA_ID = :pessoa_id
            """

        params = {"pessoa_id": t_pessoa_cartao_index_schema.pessoa_id}

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
