from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.c_caixa_servico_schema import (
    CCaixaServicoSaveSchema,
    CCaixaServicoUpdateSchema,
    CCaixaServicoIdSchema,
    CCaixaServicoDescricaoSchema,
    CCaixaServicoSistemaIdSchema,
)


class CCaixaServicoController:

    def __init__(self):
        # Action responsável por carregar as services de acodo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("c_caixa_servico")
        pass

    # Lista todos os caixa serviço
    def index(self):

        # Importação da classe desejada
        indexService = self.dynamic_import.service(
            "c_caixa_servico_index_service", "IndexService"
        )

        # Instânciamento da classe service
        self.indexService = indexService()

        # Lista todos os caixa serviço
        return {
            "message": "caixa serviço localizados com sucesso",
            "data": self.indexService.execute(),
        }

    # Busca um usuário especifico pelo ID
    def show(self, caixa_servico_schema: CCaixaServicoIdSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "c_caixa_servico_show_service", "ShowService"
        )

        # Instânciamento da classe desejada
        self.show_service = show_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Caixa Serviço localizado com sucesso",
            "data": self.show_service.execute(caixa_servico_schema),
        }

    # Busca um caixa serviço pela descrição
    def getDescricao(self, caixa_servico_schema: CCaixaServicoDescricaoSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "c_caixa_servico_get_descricao_service", "GetDescricaoService"
        )

        # Instânciamento da classe desejada
        self.show_service = show_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Caixa Serviço localizado com sucesso",
            "data": self.show_service.execute(
                caixa_servico_schema, True
            ),  # True para retornar a mensagem de erro caso não localize o serviço
        }

    # Busca um caixa serviço pelp sistema_id
    def getSistemaId(self, caixa_servico_schema: CCaixaServicoSistemaIdSchema):

        # Importação da classe desejada
        show_sistema_id_service = self.dynamic_import.service(
            "c_caixa_servico_get_sistema_id_service", "GetSistemaIdService"
        )

        # Instânciamento da classe desejada
        self.show_sistema_id_service = show_sistema_id_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Caixa Serviços localizados com sucesso",
            "data": self.show_sistema_id_service.execute(caixa_servico_schema),
        }

    # Cadastra um novo usuário
    def save(self, caixa_servico_schema: CCaixaServicoSaveSchema):

        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "c_caixa_servico_save_service", "CCaixaServicoSaveService"
        )

        # Instânciamento da classe desejada
        self.save_service = save_service()
        # Busca e retorna o usuário desejado
        return {
            "message": "Caixa Serviço salvo com sucesso",
            "data": self.save_service.execute(caixa_servico_schema),
        }

    # Atualiza os dados de um usuário
    def update(
        self, caixa_servico_id: int, caixa_servico_schema: CCaixaServicoUpdateSchema
    ):

        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "c_caixa_servico_update_service", "CCaixaServicoUpdateService"
        )

        # Instânciamento da classe desejada
        self.save_service = save_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Caixa Serviço atualizado com sucesso",
            "data": self.save_service.execute(caixa_servico_id, caixa_servico_schema),
        }

    # Exclui um usuário
    def delete(self, caixa_servico_schema: CCaixaServicoIdSchema):

        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "c_caixa_servico_delete_service", "DeleteService"
        )

        # Instânciamento da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o usuário desejado
        return {
            "message": "Caixa Serviço removido com sucesso",
            "data": self.delete_service.execute(caixa_servico_schema),
        }
