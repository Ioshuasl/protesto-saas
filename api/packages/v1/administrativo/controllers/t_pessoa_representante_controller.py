from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteIdSchema,
    TPessoaRepresentantePessoaIdSchema,
    TPessoaRepresentanteSaveSchema,
    TPessoaRepresentanteUpdateSchema,
)


class TPessoaRepresentanteController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_pessoa_representante")
        pass

    # Lista todos os regimes de bens
    def index(
        self,
        t_pessoa_representante_pessoa_id_schema: TPessoaRepresentantePessoaIdSchema,
    ):

        # Importação da classe desejada
        t_pessoa_representante_index_service = self.dynamic_import.service(
            "t_pessoa_representante_index_service", "TPessoaRepresentanteIndexService"
        )

        # Instância da classe service
        self.t_pessoa_representante_index_service = (
            t_pessoa_representante_index_service()
        )

        # Lista todos os regimes de bens
        return {
            "message": "Pessoas localizados com sucesso",
            "data": self.t_pessoa_representante_index_service.execute(
                t_pessoa_representante_pessoa_id_schema
            ),
        }

    # Busca um regime de bens específico pelo ID
    def show(self, t_pessoa_representante_id_schema: TPessoaRepresentanteIdSchema):

        # Importação da classe desejada
        t_pessoa_representante_show_service = self.dynamic_import.service(
            "t_pessoa_representante_show_service", "TPessoaRepresentanteShowService"
        )

        # Instância da classe desejada
        self.t_pessoa_representante_show_service = t_pessoa_representante_show_service()

        # Busca e retorna o regime de bens desejado
        return {
            "message": "Pessoa localizado com sucesso",
            "data": self.t_pessoa_representante_show_service.execute(
                t_pessoa_representante_id_schema
            ),
        }

    # Cadastra um novo regime de bens
    def save(self, t_pessoa_representante_save_schema: TPessoaRepresentanteSaveSchema):

        # Importação da classe desejada
        t_pessoa_representante_save_service = self.dynamic_import.service(
            "t_pessoa_representante_save_service", "TPessoaRepresentanteSaveService"
        )

        # Instância da classe desejada
        self.t_pessoa_representante_save_service = t_pessoa_representante_save_service()
        # Busca e retorna o regime de bens desejado
        return {
            "message": "Pessoa salvo com sucesso",
            "data": self.t_pessoa_representante_save_service.execute(
                t_pessoa_representante_save_schema
            ),
        }

    # Atualiza os dados de um regime de bens
    def update(
        self, t_pessoa_representante_update_schame: TPessoaRepresentanteUpdateSchema
    ):

        # Importação da classe desejada
        t_pessoa_representante_update_service = self.dynamic_import.service(
            "t_pessoa_representante_update_service", "TPessoaRepresentanteUpdateService"
        )

        # Instância da classe desejada
        self.t_pessoa_representante_update_service = (
            t_pessoa_representante_update_service()
        )

        # Busca e retorna o regime de bens desejado
        return {
            "message": "Pessoa atualizado com sucesso",
            "data": self.t_pessoa_representante_update_service.execute(
                t_pessoa_representante_update_schame
            ),
        }

    # Exclui um regime de bens
    def delete(self, t_pessoa_representante_id_schema: TPessoaRepresentanteIdSchema):

        # Importação da classe desejada
        t_pessoa_representante_delete_service = self.dynamic_import.service(
            "t_pessoa_representante_delete_service", "TPessoaRepresentanteDeleteService"
        )

        # Instância da classe desejada
        self.t_pessoa_representante_delete_service = (
            t_pessoa_representante_delete_service()
        )

        # Busca e retorna o regime de bens desejado
        return {
            "message": "Pessoa removido com sucesso",
            "data": self.t_pessoa_representante_delete_service.execute(
                t_pessoa_representante_id_schema
            ),
        }
