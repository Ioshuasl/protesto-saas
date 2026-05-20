from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
    TPessoaCartaoSaveSchema,
    TPessoaCartaoUpdateSchema,
    TPessoaCartaoIdSchema,
)


class TPessoaCartaoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_PESSOA_CARTAO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.balcao")
        self.dynamic_import.set_table("t_pessoa_cartao")

    # ----------------------------------------------------
    # Lista todos os registros de T_PESSOA_CARTAO
    # ----------------------------------------------------
    def index(self, t_pessoa_cartao_index_schema: TPessoaCartaoIndexchema):
        # Importação da classe desejada
        index_service = self.dynamic_import.service(
            "t_pessoa_cartao_index_service", "TPessoaCartaoIndexService"
        )

        # Instância da classe service
        self.index_service = index_service()

        # Execução da listagem
        return {
            "message": "Registros de T_PESSOA_CARTAO localizados com sucesso.",
            "data": self.index_service.execute(t_pessoa_cartao_index_schema),
        }

    # ----------------------------------------------------
    # Busca um registro específico de T_PESSOA_CARTAO pelo ID
    # ----------------------------------------------------
    def show(self, t_pessoa_cartao_id_schema: TPessoaCartaoIdSchema):
        # Importação da classe desejada
        show_service = self.dynamic_import.service(
            "t_pessoa_cartao_show_service", "TPessoaCartaoShowService"
        )

        # Instância da classe service
        self.show_service = show_service()

        # Execução da busca
        return {
            "message": "Registro de T_PESSOA_CARTAO localizado com sucesso.",
            "data": self.show_service.execute(t_pessoa_cartao_id_schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro em T_PESSOA_CARTAO
    # ----------------------------------------------------
    def save(self, t_pessoa_cartao_save_schema: TPessoaCartaoSaveSchema):
        # Importação da classe desejada
        save_service = self.dynamic_import.service(
            "t_pessoa_cartao_save_service", "TPessoaCartaoSaveService"
        )

        # Instância da classe service
        self.save_service = save_service()

        # Execução do salvamento
        return {
            "message": "Registro de T_PESSOA_CARTAO salvo com sucesso.",
            "data": self.save_service.execute(t_pessoa_cartao_save_schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente de T_PESSOA_CARTAO
    # ----------------------------------------------------
    def update(self, t_pessoa_cartao_update_schema: TPessoaCartaoUpdateSchema):
        # Importação da classe desejada
        update_service = self.dynamic_import.service(
            "t_pessoa_cartao_update_service", "TPessoaCartaoUpdateService"
        )

        # Instância da classe service
        self.update_service = update_service()

        # Execução da atualização
        return {
            "message": "Registro de T_PESSOA_CARTAO atualizado com sucesso.",
            "data": self.update_service.execute(t_pessoa_cartao_update_schema),
        }

    # ----------------------------------------------------
    # Exclui um registro de T_PESSOA_CARTAO
    # ----------------------------------------------------
    def delete(self, t_pessoa_cartao_id_schema: TPessoaCartaoIdSchema):
        # Importação da classe desejada
        delete_service = self.dynamic_import.service(
            "t_pessoa_cartao_delete_service", "TPessoaCartaoDeleteService"
        )

        # Instância da classe service
        self.delete_service = delete_service()

        # Execução da exclusão
        return {
            "message": "Registro de T_PESSOA_CARTAO removido com sucesso.",
            "data": self.delete_service.execute(t_pessoa_cartao_id_schema),
        }
