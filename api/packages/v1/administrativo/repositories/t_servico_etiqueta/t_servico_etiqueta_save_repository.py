from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import (
    TServicoEtiquetaSaveSchema,
)
from fastapi import HTTPException, status


class SaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela
    T_SERVICO_ETIQUETA.
    """

    def execute(self, servico_etiqueta_schema: TServicoEtiquetaSaveSchema):
        """
        Executa a consulta SQL para inserir um novo registro.

        Args:
            servico_etiqueta_schema (TServicoEtiquetaSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento, geralmente o ID do novo registro ou um status de sucesso.
        """
        try:
            # Montagem do sql. SERVICO_ETIQUETA_ID é a chave primária e presumivelmente auto-gerada.
            sql = """
                INSERT INTO T_SERVICO_ETIQUETA (SERVICO_ETIQUETA_ID, ETIQUETA_MODELO_ID, SERVICO_TIPO_ID)
                VALUES (:servico_etiqueta_id, :etiqueta_modelo_id, :servico_tipo_id) RETURNING *;
            """

            # Preenchimento de parâmetros
            params = {
                "servico_etiqueta_id": servico_etiqueta_schema.servico_etiqueta_id,
                "etiqueta_modelo_id": servico_etiqueta_schema.etiqueta_modelo_id,
                "servico_tipo_id": servico_etiqueta_schema.servico_tipo_id,
            }

            # Execução do sql
            # Assumimos que o self.run lida com a execução do INSERT.
            response = self.run_and_return(sql, params)

            # Retorna o resultado
            return response

        except Exception as e:
            # Informa que houve uma falha no salvamento
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar T_SERVICO_ETIQUETA: {e}",
            )
