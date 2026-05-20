from abstracts.repository import BaseRepository


class TImovelUnidadeAllRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela t_censec_qualidade.
    """

    def execute(self):
        """
        Executa a consulta SQL para buscar todos os registros.

        Returns:
            Uma lista de dicionários contendo os dados dos registros.
        """
        # Montagem do SQL
        sql = """ SELECT
                        TI.*,
                        TIU.IMOVEL_UNIDADE_ID,
                        TIU.IMOVEL_ID,
                        TIU.NUMERO_UNIDADE,
                        TIU.QUADRA,
                        TIU.AREA,
                        TIU.SUPERQUADRA,
                        TIU.CONJUNTO,
                        TIU.BLOCO,
                        TIU.AREA_DESCRITIVA,
                        TIU.CARACTERISTICA,
                        TIU.RESERVA_FLORESTAL,
                        TIU.GEO_REFERENCIAMENTO,
                        TIU.LOGRADOURO,
                        TIU.TB_TIPOLOGRADOURO_ID,
                        TIU.SELECIONADO,
                        TIU.COMPLEMENTO,
                        TIU.TIPO_IMOVEL,
                        TIU.TIPO_CONSTRUCAO,
                        TIU.NUMERO_EDIFICACAO,
                        TIU.IPTU,
                        TIU.CCIR,
                        TIU.NIRF,
                        TIU.LOTE,
                        TIU.TORRE,
                        TIU.NOMELOTEAMENTO,
                        TIU.NOMECONDOMINIO,
                        TIU.NUMERO,
                        TIU.CNM_NUMERO,
                        TIU.IMOVEL_PUBLICO_UNIAO,
                        TIU.SPU_RIP,
                        TIU.CAT,
                        TIU.INSCRICAO_MUNICIPAL,
                        TIU.CIB,
                        TIU.AREA_CONSTRUIDA
                    FROM T_IMOVEL_UNIDADE TIU
                    JOIN T_IMOVEL TI ON TIU.IMOVEL_ID = TI.IMOVEL_ID """

        # Execução do sql
        response = self.fetch_all(sql)

        # Retorna os dados localizados
        return response
