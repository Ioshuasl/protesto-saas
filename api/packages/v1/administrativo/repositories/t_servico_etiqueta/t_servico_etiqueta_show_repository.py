from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import TServicoEtiquetaIdSchema # Schema ajustado para T_SERVICO_ETIQUETA
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela T_SERVICO_ETIQUETA.
    """

    def execute(self, servico_etiqueta_schema: TServicoEtiquetaIdSchema): # Nome do parâmetro e tipo ajustados
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
            sql = "SELECT SERVICO_ETIQUETA_ID, ETIQUETA_MODELO_ID, SERVICO_TIPO_ID FROM T_SERVICO_ETIQUETA WHERE SERVICO_ETIQUETA_ID = :servico_etiqueta_id"

            # Preenchimento de parâmetros
            params = {
                # Nome do parâmetro ajustado para SERVICO_ETIQUETA_ID
                'servico_etiqueta_id': servico_etiqueta_schema.servico_etiqueta_id
            }

            # Execução do SQL
            result = self.fetch_one(sql, params)

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