from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoDescricaoSchema # Nome do schema ajustado

class GetByDescricaoRepository(BaseRepository):
    """
    Repositório para a operação de busca de um registro na tabela
    T_SERVICO_TIPO por descrição.
    """

    def execute(self, servico_tipo_schema: TServicoTipoDescricaoSchema): # Nome do parâmetro ajustado
        """
        Executa a consulta SQL para buscar um registro pela descrição.

        Args:
            servico_tipo_schema (TServicoTipoDescricaoSchema): O esquema com a descrição a ser buscada. # Nome do tipo ajustado

        Returns:
            Um dicionário contendo os dados do registro ou None se não for encontrado.
        """
        # Montagem do SQL
        # Tabela e coluna ajustadas
        sql = """ SELECT * FROM T_SERVICO_TIPO WHERE DESCRICAO = :descricao """

        # Preenchimento de parâmetros
        params = {
            # Ajuste para usar o atributo 'descricao' do novo schema
            'descricao': servico_tipo_schema.descricao
        }

        # Execução do sql
        return self.fetch_one(sql, params)