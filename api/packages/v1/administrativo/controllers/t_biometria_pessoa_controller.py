from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIndexSchema,
    TBiometriaPessoaSaveSchema,
    TBiometriaPessoaUpdateSchema,
    TBiometriaPessoaIdSchema,
)


class TBiometriaPessoaController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_BIOMETRIA_PESSOA,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_biometria_pessoa")

    # ----------------------------------------------------
    # Lista todos os registros de T_BIOMETRIA_PESSOA
    # ----------------------------------------------------
    def index(self, biometria_pessoa_index_schema: TBiometriaPessoaIndexSchema):

        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_biometria_pessoa_index_service", "TBiometriaPessoaIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_BIOMETRIA_PESSOA localizados com sucesso.",
            "data": self.index_service.execute(biometria_pessoa_index_schema),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_BIOMETRIA_PESSOA pelo ID
    # ----------------------------------------------------
    def show(self, t_biometria_pessoa_id_schema: TBiometriaPessoaIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_biometria_pessoa_show_service", "TBiometriaPessoaShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_BIOMETRIA_PESSOA localizado com sucesso.",
            "data": self.show_service.execute(t_biometria_pessoa_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_BIOMETRIA_PESSOA
    # ----------------------------------------------------
    def save(self, t_biometria_pessoa_save_schema: TBiometriaPessoaSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_biometria_pessoa_save_service", "TBiometriaPessoaSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_BIOMETRIA_PESSOA salvo com sucesso.",
            "data": self.save_service.execute(t_biometria_pessoa_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_BIOMETRIA_PESSOA
    # ----------------------------------------------------
    def update(self, t_biometria_pessoa_update_schema: TBiometriaPessoaUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_biometria_pessoa_update_service", "TBiometriaPessoaUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_BIOMETRIA_PESSOA atualizado com sucesso.",
            "data": self.update_service.execute(t_biometria_pessoa_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_BIOMETRIA_PESSOA
    # ----------------------------------------------------
    def delete(self, t_biometria_pessoa_id_schema: TBiometriaPessoaIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_biometria_pessoa_delete_service", "TBiometriaPessoaDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_BIOMETRIA_PESSOA removido com sucesso.",
            "data": self.delete_service.execute(t_biometria_pessoa_id_schema),
        }
