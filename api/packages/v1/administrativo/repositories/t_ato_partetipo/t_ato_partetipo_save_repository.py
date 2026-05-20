from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoSaveSchema,
)


class TAtoParteTipoSaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_t_ato_partetipo_unidade.
    """

    def execute(self, t_ato_partetipo_save_schema: TAtoParteTipoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_ato_partetipo_schema (TAtoParteTipoSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Montagem do SQL
            # ----------------------------------------------------
            sql = """
                INSERT INTO T_ATO_PARTETIPO (
                    ATO_PARTETIPO_ID,
                    DESCRICAO,
                    TIPO_PARTE,
                    AUTO_QUALIFICA,
                    DECLARA_DOI,
                    POSSUI_DOCUMENTO_EXT,
                    SITUACAO,
                    CENSEC_QUALIDADE_ID
                ) VALUES (
                    :ato_partetipo_id,
                    :descricao,
                    :tipo_parte,
                    :auto_qualifica,
                    :declara_doi,
                    :possui_documento_ext,
                    :situacao,
                    :censec_qualidade_id
                )
                RETURNING  ATO_PARTETIPO_ID,
                           DESCRICAO,
                           TIPO_PARTE,
                           AUTO_QUALIFICA,
                           DECLARA_DOI,
                           POSSUI_DOCUMENTO_EXT,
                           SITUACAO,
                           CENSEC_QUALIDADE_ID
                ;
            """

            # ----------------------------------------------------
            # Preenchimento dos parâmetros de acordo com o schema
            # ----------------------------------------------------
            params = t_ato_partetipo_save_schema.model_dump(exclude_unset=True)

            # Execução do sql
            return self.run_and_return(sql, params)

        except Exception as e:

            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar T_IMOVEL: {e}",
            )
