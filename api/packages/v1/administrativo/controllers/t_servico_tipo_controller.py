from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIndexSchema,
    TServicoTipoSaveSchema,
    TServicoTipoUpdateSchema,
    TServicoTipoIdSchema,
    TServicoTipoDescricaoSchema,
)


class TServicoTipoController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_servico_tipo")
        pass

    # Lista todos os registros de servico tipo
    def index(self, t_servico_tipo_index_schema: TServicoTipoIndexSchema):

        # Importação da classe desejada
        indexService = self.dynamic_import.service(
            "t_servico_tipo_index_service", "IndexService"
        )

        # Instância da classe service
        self.indexService = indexService()

        # Lista todos os registros de servico tipo
        return {
            "message": "Registros de servico tipo localizados com sucesso",
            "data": self.indexService.execute(t_servico_tipo_index_schema),
        }

    # Busca um registro de servico tipo específico pelo ID
    def show(self, servico_tipo_schema: TServicoTipoIdSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_servico_tipo_show_service", "ShowService"
        )

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de servico tipo desejado
        return {
            "message": "Registro de servico tipo localizado com sucesso",
            "data": self.show_service.execute(servico_tipo_schema),
        }

    # Busca um registro de servico tipo pela descrição
    def get_by_descricao(self, servico_tipo_schema: TServicoTipoDescricaoSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_servico_tipo_get_by_descricao_service", "GetByDescricaoService"
        )

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de servico tipo desejado
        return {
            "message": "Registro de servico tipo localizado com sucesso",
            "data": self.show_service.execute(servico_tipo_schema, True),
        }

    def top_servicos_tipo(self):
        service = self.dynamic_import.service(
            "t_servico_tipo_top_servicos_tipo_service", "TopServicosTipoService"
        )
        self.service = service()
        return {
            "message": "Ranking de servico tipo localizado com sucesso",
            "data": self.service.execute(),
        }

    # Cadastra um novo registro de servico tipo
    def save(self, servico_tipo_schema: TServicoTipoSaveSchema):

        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_servico_tipo_save_service", "SaveService"
        )

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de servico tipo desejado
        return {
            "message": "Registro de servico tipo salvo com sucesso",
            "data": self.save_service.execute(servico_tipo_schema),
        }

    # Atualiza os dados de um registro de servico tipo
    def update(
        self, servico_tipo_id: int, servico_tipo_schema: TServicoTipoUpdateSchema
    ):

        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_servico_tipo_update_service", "UpdateService"
        )

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de servico tipo desejado
        return {
            "message": "Registro de servico tipo atualizado com sucesso",
            "data": self.update_service.execute(servico_tipo_id, servico_tipo_schema),
        }

    # Exclui um registro de servico tipo
    def delete(self, servico_tipo_schema: TServicoTipoIdSchema):

        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_servico_tipo_delete_service", "DeleteService"
        )

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de servico tipo desejado
        return {
            "message": "Registro de servico tipo removido com sucesso",
            "data": self.delete_service.execute(servico_tipo_schema),
        }
