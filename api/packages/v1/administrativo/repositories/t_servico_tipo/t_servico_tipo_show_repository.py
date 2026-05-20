from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoIdSchema # Nome do schema ajustado
from fastapi import HTTPException, status

class ShowRepository(BaseRepository):
    """
    Repositório para a operação de exibição de um registro na tabela T_SERVICO_TIPO.
    """

    def execute(self, servico_tipo_schema: TServicoTipoIdSchema): # Nome do parâmetro ajustado
        """
        Busca um registro específico de T_SERVICO_TIPO pelo ID.

        Args:
            servico_tipo_schema (TServicoTipoIdSchema): O esquema que contém o ID do registro. # Nome do tipo ajustado

        Returns:
            O registro encontrado ou None se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # Montagem do SQL
            # Tabela e coluna da chave primária ajustadas
            sql = "SELECT * FROM T_SERVICO_TIPO WHERE SERVICO_TIPO_ID = :servico_tipo_id"

            # Preenchimento de parâmetros
            params = {
                # Nome do parâmetro ajustado
                'servico_tipo_id': servico_tipo_schema.servico_tipo_id
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
                detail=f"Erro ao buscar registro T_SERVICO_TIPO: {str(e)}"
            )