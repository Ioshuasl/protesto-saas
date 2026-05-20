from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import (
    TServicoEtiquetaSaveSchema,
    TServicoEtiquetaUpdateSchema,
    TServicoEtiquetaIdSchema,
    TServicoEtiquetaServicoTipoIdSchema,
)


class TServicoEtiquetaController:

    def __init__(self):
        # Action responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_servico_etiqueta")
        pass

    # Lista todos os registros de servico etiqueta
    def index(self):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_servico_etiqueta_index_service", "IndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Lista todos os registros de servico etiqueta
        return {
            "message": "Registros de servico etiqueta localizados com sucesso",
            "data": self.index_service.execute(),
        }

    # Busca um registro de servico etiqueta específico pelo ID serviço tipo
    def showServicoTipo(self, servico_tipo_schema: TServicoEtiquetaServicoTipoIdSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_servico_etiqueta_show_servico_tipo_service", "ShowService"
        )

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de servico etiqueta desejado
        return {
            "message": "Registros de serviço etiqueta localizados com sucesso",
            "data": self.show_service.execute(servico_tipo_schema),
        }

    # Busca um registro de servico etiqueta específico pelo ID
    def show(self, servico_etiqueta_schema: TServicoEtiquetaIdSchema):

        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_servico_etiqueta_show_service", "ShowService"
        )

        # Instância da classe desejada
        self.show_service = show_service()

        # Busca e retorna o registro de servico etiqueta desejado
        return {
            "message": "Registro de servico etiqueta localizado com sucesso",
            "data": self.show_service.execute(servico_etiqueta_schema),
        }

    # Cadastra um novo registro de servico etiqueta
    def save(self, servico_etiqueta_schema: TServicoEtiquetaSaveSchema):

        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_servico_etiqueta_save_service", "SaveService"
        )

        # Instância da classe desejada
        self.save_service = save_service()
        # Busca e retorna o registro de servico etiqueta desejado
        return {
            "message": "Registro de servico etiqueta salvo com sucesso",
            "data": self.save_service.execute(servico_etiqueta_schema),
        }

    # Atualiza os dados de um registro de servico etiqueta
    def update(
        self,
        servico_etiqueta_id: int,
        servico_etiqueta_schema: TServicoEtiquetaUpdateSchema,
    ):

        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_servico_etiqueta_update_service", "UpdateService"
        )

        # Instância da classe desejada
        self.update_service = update_service()

        # Busca e retorna o registro de servico etiqueta desejado
        return {
            "message": "Registro de servico etiqueta atualizado com sucesso",
            "data": self.update_service.execute(
                servico_etiqueta_id, servico_etiqueta_schema
            ),
        }

    # Exclui um registro de servico etiqueta
    def delete(self, servico_etiqueta_schema: TServicoEtiquetaIdSchema):

        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_servico_etiqueta_delete_service", "DeleteService"
        )

        # Instância da classe desejada
        self.delete_service = delete_service()

        # Busca e retorna o registro de servico etiqueta desejado
        return {
            "message": "Registro de servico etiqueta removido com sucesso",
            "data": self.delete_service.execute(servico_etiqueta_schema),
        }
