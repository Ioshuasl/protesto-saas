from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_minuta_schema import (
    TMinutaSaveSchema,
    TMinutaUpdateSchema,
    TMinutaIdSchema,
    TMinutaDescricaoSchema,
    TMinutaUpdateTextoSchema
)

class TMinutaController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_minuta")
        pass

    # Lista todos os registros de minuta
    def index(self):

        # Importação da classe desejada
        indexService = self.dynamic_import.service("t_minuta_index_service", "IndexService")

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de minuta
        return {
            'message': 'Registros de minuta localizados com sucesso',
            'data': self.indexService.execute()
        }


    # Busca um registro de minuta específico pelo ID
    def show_texto(self, minuta_schema: TMinutaIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_minuta_show_texto_service', 'TMinutaShowTextoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de minuta desejado
        return {
            'message': 'Registro de minuta localizado com sucesso',
            'data': self.show_service.execute(minuta_schema)
        }

    # Busca um registro de minuta específico pelo ID
    def show(self, minuta_schema: TMinutaIdSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_minuta_show_service', 'ShowService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de minuta desejado
        return {
            'message': 'Registro de minuta localizado com sucesso',
            'data': self.show_service.execute(minuta_schema)
        }


    # Busca um registro de minuta específico pela descrição
    def get_by_descricao(self, minuta_schema: TMinutaDescricaoSchema):

        #Importação da classe desejada
        show_service = self.dynamic_import.service('t_minuta_get_descricao_service', 'GetByDescricaoService')

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de minuta desejado
        return {
            'message': 'Registro de minuta localizado com sucesso',
            'data': self.show_service.execute(minuta_schema, True)
        }

    # Cadastra um novo registro de minuta
    def save(self, minuta_schema: TMinutaSaveSchema):

        #Importação da classe desejada
        save_service = self.dynamic_import.service('t_minuta_save_service', 'SaveService')

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de minuta desejado
        return {
            'message': 'Registro de minuta salvo com sucesso',
            'data': self.save_service.execute(minuta_schema)
        }

    # Atualiza os dados de um registro de minuta
    def update(self, minuta_id_schema: TMinutaIdSchema, minuta_schema: TMinutaUpdateSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('t_minuta_update_service', 'UpdateService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de minuta desejado
        return {
            'message': 'Registro de minuta atualizado com sucesso',
            'data': self.update_service.execute(minuta_id_schema.minuta_id, minuta_schema)
        }

    # Atualiza os dados de um registro de minuta
    def update_texto(self, data: TMinutaUpdateTextoSchema):

        #Importação da classe desejada
        update_service = self.dynamic_import.service('t_minuta_update_texto_service', 'TMinutaUpdateTextoService')

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de minuta desejado
        return {
            'message': 'Registro de minuta atualizado com sucesso',
            'data': self.update_service.execute(data)
        }

    # Exclui um registro de minuta
    def delete(self, minuta_schema: TMinutaIdSchema):

        #Importação da classe desejada
        delete_service = self.dynamic_import.service('t_minuta_delete_service', 'DeleteService')

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de minuta desejado
        return {
            'message': 'Registro de minuta removido com sucesso',
            'data': self.delete_service.execute(minuta_schema)
        }
