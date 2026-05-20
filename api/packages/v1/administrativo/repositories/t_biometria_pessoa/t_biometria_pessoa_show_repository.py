from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIdSchema,
)


class TBiometriaPessoaShowRepository(BaseRepository):
    """
    Repositório responsável pela operação de exibição de um registro
    na tabela G_GRAMATICA.
    """

    def execute(self, t_biometria_pessoa_id_schema: TBiometriaPessoaIdSchema):
        """
        Busca um registro específico de G_GRAMATICA pelo ID.

        Args:
            t_biometria_pessoa_id_schema (TBiometriaPessoaIdSchema):
                Esquema contendo o ID do registro a ser buscado.

        Returns:
            O registro encontrado ou levanta exceção HTTP 404 se não existir.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:
            # ----------------------------------------------------
            # Montagem do SQL
            # ----------------------------------------------------
            sql = """
                SELECT *
                FROM T_BIOMETRIA_PESSOA GG
                WHERE GG.BIOMETRIA_PESSOA_ID = :biometria_pessoa_id
            """

            # ----------------------------------------------------
            # Preenchimento de parâmetros
            # ----------------------------------------------------
            params = t_biometria_pessoa_id_schema.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Execução do SQL
            # ----------------------------------------------------
            result = self.fetch_one(sql, params)

            # ----------------------------------------------------
            # Validação de retorno
            # ----------------------------------------------------
            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro de T_BIOMETRIA_PESSOA não encontrado.",
                )

            return result

        except HTTPException:
            # Repassa exceções HTTP explícitas (como 404)
            raise

        except Exception as e:
            # Captura falhas inesperadas de execução
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao buscar registro em G_GRAMATICA: {e}",
            )
