from abstracts.repository import BaseRepository
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteUpdateSchema,
)


class TPessoaRepresentanteUpdateRepository(BaseRepository):
    """
    Repositório responsável por atualizar parcialmente registros na tabela T_PESSOA_REPRESENTANTE.
    """

    def execute(
        self, t_pessoa_representante_update_schema: TPessoaRepresentanteUpdateSchema
    ):
        """
        Executa a atualização de um registro da tabela T_PESSOA_REPRESENTANTE.

        Args:
            t_pessoa_representante_update_schema (TPessoaRepresentanteUpdateSchema): Dados enviados para atualização.

        Returns:
            dict: Registro atualizado.

        Raises:
            HTTPException: Caso o registro não exista ou ocorra erro de execução.
        """
        try:
            # Extrai apenas campos enviados
            data = t_pessoa_representante_update_schema.model_dump(exclude_unset=True)
            updates = []
            params = {
                "pessoa_representante_id": t_pessoa_representante_update_schema.pessoa_representante_id
            }

            # Monta dinamicamente os campos que serão atualizados
            for field, value in data.items():
                if field != "pessoa_representante_id" and value is not None:
                    updates.append(f"{field.upper()} = :{field}")
                    params[field] = value

            # Nenhum campo informado
            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Nenhum campo informado para atualização.",
                )

            # SQL dinâmico corrigido
            sql = f"""
                UPDATE T_PESSOA_REPRESENTANTE
                SET {', '.join(updates)}
                WHERE PESSOA_REPRESENTANTE_ID = :pessoa_representante_id
                RETURNING *;
            """

            # Executa e retorna o resultado
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Nenhum registro encontrado com o ID {t_pessoa_representante_update_schema.pessoa_representante_id}.",
                )

            return result

        except HTTPException:
            raise

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o representante/pessoa: {e}",
            )
