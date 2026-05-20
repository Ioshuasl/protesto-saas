from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import (
    TServicoEtiquetaIdSchema,
)


class DeleteRepository(BaseRepository):

    def execute(self, servico_etiqueta_schema: TServicoEtiquetaIdSchema):

        # Montagem do sql
        sql = """ DELETE FROM T_SERVICO_ETIQUETA WHERE SERVICO_ETIQUETA_ID = :servico_etiqueta_id RETURNING servico_etiqueta_id  """

        # Preenchimento de parâmetros
        params = {"servico_etiqueta_id": servico_etiqueta_schema.servico_etiqueta_id}

        # Execução do sql
        response = self.run_and_return(sql, params)

        # Retorna o resultado
        return response
