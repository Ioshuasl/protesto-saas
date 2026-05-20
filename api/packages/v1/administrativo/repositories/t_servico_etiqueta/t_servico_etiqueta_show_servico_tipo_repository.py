from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import TServicoEtiquetaServicoTipoIdSchema # Schema ajustado para T_SERVICO_ETIQUETA
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela T_SERVICO_ETIQUETA.
    """

    def execute(self, servico_tipo_schema: TServicoEtiquetaServicoTipoIdSchema): # Nome do parâmetro e tipo ajustados
        """
        Busca um registro específico de T_SERVICO_ETIQUETA pelo ID.

        Args:
            servico_etiqueta_schema (TServicoEtiquetaIdSchema): O esquema que contém o ID do registro. # Nome do tipo ajustado

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            # Tabela e coluna da chave primária ajustadas para T_SERVICO_ETIQUETA
            sql = """ SELECT E.SERVICO_ETIQUETA_ID, 
                             E.ETIQUETA_MODELO_ID, 
                             E.SERVICO_TIPO_ID,
                             T.DESCRICAO 
                      FROM T_SERVICO_ETIQUETA E
                      LEFT JOIN G_MARCACAO_TIPO T ON E.ETIQUETA_MODELO_ID = T.MARCACAO_TIPO_ID
                      WHERE E.SERVICO_TIPO_ID = :servico_tipo_id """

            # Preenchimento de parâmetros
            params = {
                # Nome do parâmetro ajustado para SERVICO_TIPO_ID
                'servico_tipo_id': servico_tipo_schema.servico_tipo_id
            }

            # Execução do SQL
            result = self.fetch_all(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado"
                )

            return result
        except Exception as e:
            # Tratamento de erro ajustado
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar registro T_SERVICO_ETIQUETA: {str(e)}"
            )