from abstracts.repository import BaseRepository
from packages.v1.administrativo.controllers.t_servico_tipo_controller import (
    TServicoTipoIndexSchema,
)


class IndexRepository(BaseRepository):
    """
    Repositório para a operação de listagem de todos os registros
    na tabela T_SERVICO_TIPO.
    """

    def execute(self, t_servico_tipo_index_schema: TServicoTipoIndexSchema):

        # Montagem do sql
        sql = "SELECT TST.* FROM T_SERVICO_TIPO TST"

        # lista de condições
        where = []

        # Verifica se deve filtrar a pesquisa
        if getattr(t_servico_tipo_index_schema, "situacao", None):

            where.append("TST.SITUACAO LIKE :situacao")

        if where:
            sql += " WHERE " + " AND ".join(where)

        # Preenchimento de valores
        params = t_servico_tipo_index_schema.model_dump(exclude_unset=True)

        # Execução do sql
        response = self.fetch_all(sql, params)

        # Retorna os dados localizados
        return response
