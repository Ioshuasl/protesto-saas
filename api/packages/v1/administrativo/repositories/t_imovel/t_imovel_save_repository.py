from packages.v1.administrativo.schemas.t_imovel_schema import TImovelSchema
from fastapi import HTTPException, status
from abstracts.repository import BaseRepository


class TImovelSaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_t_imovel_unidade.
    """

    def execute(self, t_imovel_schema: TImovelSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_imovel_schema (TImovelSchema): O esquema com os dados a serem salvos.

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
                INSERT INTO T_IMOVEL (
                    IMOVEL_ID,
                    TIPO_CLASSE,
                    TIPO_REGISTRO,
                    DATA_REGISTRO,
                    NUMERO,
                    NUMERO_LETRA,
                    CIDADE,
                    CEP,
                    UF,
                    TB_BAIRRO_ID,
                    CARTORIO,
                    LIVRO,
                    CNS
                ) VALUES (
                    :imovel_id,
                    :tipo_classe,
                    :tipo_registro,
                    :data_registro,
                    :numero,
                    :numero_letra,
                    :cidade,
                    :cep,
                    :uf,
                    :tb_bairro_id,
                    :cartorio,
                    :livro,
                    :cns
                )
                RETURNING *;
            """

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = {
                "imovel_id": t_imovel_schema.imovel_id,
                "tipo_classe": t_imovel_schema.tipo_classe,
                "tipo_registro": t_imovel_schema.tipo_registro,
                "data_registro": t_imovel_schema.data_registro,
                "numero": t_imovel_schema.numero,
                "numero_letra": t_imovel_schema.numero_letra,
                "cidade": t_imovel_schema.cidade,
                "cep": t_imovel_schema.cep,
                "uf": t_imovel_schema.uf,
                "tb_bairro_id": t_imovel_schema.tb_bairro_id,
                "cartorio": t_imovel_schema.cartorio,
                "livro": t_imovel_schema.livro,
                "cns": t_imovel_schema.cns,
            }

            # Execução do sql
            return self.run_and_return(sql, params)

        except Exception as e:

            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar T_IMOVEL: {e}",
            )
