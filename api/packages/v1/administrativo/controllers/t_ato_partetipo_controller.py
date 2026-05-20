from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoSaveSchema,
    TAtoParteTipoUpdateSchema,
    TAtoParteTipoIdSchema
)


class TAtoParteTipoController:
    """
    Controller responsável pelas operações de CRUD na tabela T_ATO_PARTETIPO.
    Gerencia chamadas de listagem, busca, inserção, atualização e exclusão
    de registros utilizando o sistema de importação dinâmica de services.
    """

    def __init__(self):
        # Instancia o gerenciador dinâmico de imports
        self.dynamic_import = DynamicImport()

        # Define o pacote ao qual o controller pertence
        self.dynamic_import.set_package("administrativo")

        # Define a tabela alvo das operações
        self.dynamic_import.set_table("t_ato_partetipo")
        pass

    # ----------------------------------------------------
    # Lista todos os registros de T_ATO_PARTETIPO
    # ----------------------------------------------------
    def index(self):
        # Importa o service correspondente dinamicamente
        index_service_class = self.dynamic_import.service(
            "t_ato_partetipo_index_service",
            "TAtoParteTipoIndexService"
        )

        # Instancia o service
        self.index_service = index_service_class()

        # Executa a listagem e retorna o resultado
        return {
            "message": "Registros de T_ATO_PARTETIPO localizados com sucesso",
            "data": self.index_service.execute(),
        }

    # ----------------------------------------------------
    # Busca um registro de T_ATO_PARTETIPO pelo ID
    # ----------------------------------------------------
    def show(self, t_ato_partetipo_id_schema: TAtoParteTipoIdSchema):
        # Importa o service correspondente dinamicamente
        show_service_class = self.dynamic_import.service(
            "t_ato_partetipo_show_service",
            "TAtoParteTipoShowService"
        )

        # Instancia o service
        self.show_service = show_service_class()

        # Executa a busca e retorna o resultado
        return {
            "message": "Registro de T_ATO_PARTETIPO localizado com sucesso",
            "data": self.show_service.execute(t_ato_partetipo_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro de T_ATO_PARTETIPO
    # ----------------------------------------------------
    def save(self, t_ato_partetipo_save_schema: TAtoParteTipoSaveSchema):
        # Importa o service correspondente dinamicamente
        save_service_class = self.dynamic_import.service(
            "t_ato_partetipo_save_service",
            "TAtoParteTipoSaveService"
        )

        # Instancia o service
        self.save_service = save_service_class()

        # Executa a inserção e retorna o resultado
        return {
            "message": "Registro de T_ATO_PARTETIPO salvo com sucesso",
            "data": self.save_service.execute(t_ato_partetipo_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza os dados de um registro existente
    # ----------------------------------------------------
    def update(self, t_ato_partetipo_update_schema: TAtoParteTipoUpdateSchema):
        # Importa o service correspondente dinamicamente
        update_service_class = self.dynamic_import.service(
            "t_ato_partetipo_update_service",
            "TAtoParteTipoUpdateService"
        )

        # Instancia o service
        self.update_service = update_service_class()

        # Executa a atualização e retorna o resultado
        return {
            "message": "Registro de T_ATO_PARTETIPO atualizado com sucesso",
            "data": self.update_service.execute(t_ato_partetipo_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_ATO_PARTETIPO
    # ----------------------------------------------------
    def delete(self, t_ato_partetipo_id_schema: TAtoParteTipoIdSchema):
        # Importa o service correspondente dinamicamente
        delete_service_class = self.dynamic_import.service(
            "t_ato_partetipo_delete_service",
            "TAtoParteTipoDeleteService"
        )

        # Instancia o service
        self.delete_service = delete_service_class()

        # Executa a exclusão e retorna o resultado
        return {
            "message": "Registro de T_ATO_PARTETIPO removido com sucesso",
            "data": self.delete_service.execute(t_ato_partetipo_id_schema),
        }
