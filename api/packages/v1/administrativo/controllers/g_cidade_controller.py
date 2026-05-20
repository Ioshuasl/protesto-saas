from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_cidade_schema import (
    GCidadeIndexSchema,
    GCidadeSaveSchema,
    GCidadeUpdateSchema,
    GCidadeIdSchema,
    GCidadeNomeSchema,
)


class GCidadeController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("g_cidade")
        pass

    # Lista todos os registros de cidade
    def index(self, data: GCidadeIndexSchema):

        # Importação da classe desejada
        indexService = self.dynamic_import.service(
            "g_cidade_index_service", "IndexService"
        )

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de cidade
        return {
            "message": "Registros de cidade localizados com sucesso",
            "data": self.indexService.execute(data),
        }

    # Busca um registro de cidade específico pelo ID
    def show(self, g_cidade_schema: GCidadeIdSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "g_cidade_show_service", "ShowService"
        )

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de cidade desejado
        return {
            "message": "Registro de cidade localizado com sucesso",
            "data": self.show_service.execute(g_cidade_schema),
        }

    # Busca um registro de cidade pelo nome (CIDADE_NOME)
    def get_by_nome(self, g_cidade_schema: GCidadeNomeSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "g_cidade_get_nome_service", "GetByNomeService"
        )

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de cidade desejado
        return {
            "message": "Registro de cidade localizado com sucesso",
            "data": self.show_service.execute(g_cidade_schema, True),
        }

    # Cadastra um novo registro de cidade
    def save(self, g_cidade_schema: GCidadeSaveSchema):

        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "g_cidade_save_service", "SaveService"
        )

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de cidade desejado
        return {
            "message": "Registro de cidade salvo com sucesso",
            "data": self.save_service.execute(g_cidade_schema),
        }

    # Atualiza os dados de um registro de cidade
    def update(self, cidade_id: int, g_cidade_schema: GCidadeUpdateSchema):

        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "g_cidade_update_service", "UpdateService"
        )

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de cidade desejado
        return {
            "message": "Registro de cidade atualizado com sucesso",
            "data": self.update_service.execute(cidade_id, g_cidade_schema),
        }

    # Exclui um registro de cidade
    def delete(self, g_cidade_schema: GCidadeIdSchema):

        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "g_cidade_delete_service", "DeleteService"
        )

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de cidade desejado
        return {
            "message": "Registro de cidade removido com sucesso",
            "data": self.delete_service.execute(g_cidade_schema),
        }
