from fastapi import HTTPException, status
from abstracts.repository import BaseRepository

# Assumindo que o novo schema de save está no mesmo padrão de importação
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoSaveSchema,
)


class GMarcacaoTipoSaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela G_MARCACAO_TIPO.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            marcacao_tipo_schema (GMarcacaoTipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # Montagem do SQL
            sql = generate_insert_sql("G_MARCACAO_TIPO", marcacao_tipo_schema, True)

            # Preenchimento de parâmetros
            params = marcacao_tipo_schema.model_dump(exclude_unset=True)

            # Execução do sql
            return self.run_and_return(sql, params)

        except Exception as e:

            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar MARCAÇÃO TIPO: {e}",
            )
