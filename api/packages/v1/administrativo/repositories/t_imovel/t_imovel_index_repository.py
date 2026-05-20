from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelIndexSchema


class TImovelIndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self, t_imovel_index_schema: TImovelIndexSchema):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT TI.*,
                    GTBB.DESCRICAO AS GTBB_DESCRICAO
                FROM T_IMOVEL TI
                LEFT JOIN G_TB_BAIRRO GTBB ON TI.TB_BAIRRO_ID = GTBB.TB_BAIRRO_ID
                WHERE TI.TIPO_CLASSE = :tipoClasse
                ORDER BY imovel_id DESC """

        params = {"tipoClasse": t_imovel_index_schema.tipo_classe}

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
