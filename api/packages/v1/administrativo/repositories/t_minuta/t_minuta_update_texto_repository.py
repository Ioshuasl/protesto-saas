from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaUpdateSchema

class TMinutaUpdateTextoRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_MINUTA.
    """

    def execute(self, data: TMinutaUpdateSchema):
        """
        Executa a atualização de um registro na tabela.

        Args:
            minuta_id (int): O ID do registro a ser atualizado.
            minuta_schema (TMinutaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.

        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """

        # Montagem do SQL.
        # run_and_return() espera uma query com retorno de linha, entao este UPDATE
        # precisa expor RETURNING para nao fechar o cursor automaticamente.
        sql = """
            UPDATE T_MINUTA TM
               SET TM.TEXTO = :texto
             WHERE TM.MINUTA_ID = :minuta_id
         RETURNING *;
        """

        # Preenchimento de parâmetros
        params = {
            'minuta_id': data.minuta_id,
            'texto': data.texto,
        }

        # Execução do sql
        return self.run_and_return(sql, params)
