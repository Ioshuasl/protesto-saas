from packages.v1.administrativo.schemas.t_pessoa_schema import (
    TPessoaPyrosRepository,
    TPessoaTipoSchema,
)
from packages.v1.pyros.operators.comparison import Equals


class TPessoaIndexRepository:
    """
    Repositório para a operação de listagem de pessoas,
    agora montando e executando SQL via Pyros em cadeia fluente.
    """

    def execute(self, data: TPessoaTipoSchema):

        response = (
            TPessoaPyrosRepository.select(
                [
                    "pessoa_id",
                    "pessoa_tipo",
                    "nome",
                    "cpf_cnpj",
                    "data_nascimento",
                    "sexo",
                    "nacionalidade",
                    "naturalidade",
                    "email",
                    "telefone",
                    "endereco",
                    "numero_end",
                    "bairro",
                    "cidade",
                    "uf",
                    "cep",
                ]
            )
            .where({"pessoa_tipo": Equals(data.pessoa_tipo)})
            .order_by(data.query_params.sort.field, data.query_params.sort.direction)
            .paginate(data.query_params.page, data.query_params.per_page)
            .fetch_all()
        )

        return response
