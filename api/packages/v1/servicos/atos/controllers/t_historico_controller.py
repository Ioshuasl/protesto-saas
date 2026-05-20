from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoHashSchema,
    THistoricoIndexSchema,
    THistoricoSaveSchema,
    THistoricoUpdateSchema,
    THistoricoIdSchema,
)
from packages.v1.servicos.atos.services.t_historico.go.t_historico_hash_service import (
    THistoricoHashService,
)


class THistoricoController:
    """
    Controller responsável por orquestrar as operações CRUD da tabela T_HISTORICO,
    utilizando carregamento dinâmico de serviços via DynamicImport.
    """

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("servicos.atos")
        self.dynamic_import.set_table("t_historico")

    # ----------------------------------------------------
    # Lista todos os registros
    # ----------------------------------------------------
    def index(self, data: THistoricoIndexSchema):
        index_service = self.dynamic_import.service(
            "t_historico_index_service", "THistoricoIndexService"
        )

        service = index_service()

        return {
            "message": "Registros de T_HISTORICO localizados com sucesso.",
            "data": service.execute(data),
        }

    # ----------------------------------------------------
    # Busca um registro específico pelo ID
    # ----------------------------------------------------
    def show(self, schema: THistoricoIdSchema):
        show_service = self.dynamic_import.service(
            "t_historico_show_service", "THistoricoShowService"
        )

        service = show_service()

        return {
            "message": "Registro de T_HISTORICO localizado com sucesso.",
            "data": service.execute(schema),
        }

    def show_by_hash(self, schema: THistoricoHashSchema):
        return {
            "message": "Registros de T_HISTORICO localizados por hash com sucesso.",
            "data": THistoricoHashService().execute(schema),
        }

    # ----------------------------------------------------
    # Cadastra um novo registro
    # ----------------------------------------------------
    def save(self, schema: THistoricoSaveSchema):
        save_service = self.dynamic_import.service(
            "t_historico_save_service", "THistoricoSaveService"
        )

        service = save_service()

        return {
            "message": "Registro de T_HISTORICO salvo com sucesso.",
            "data": service.execute(schema),
        }

    # ----------------------------------------------------
    # Atualiza um registro existente
    # ----------------------------------------------------
    def update(self, schema: THistoricoUpdateSchema):
        update_service = self.dynamic_import.service(
            "t_historico_update_service", "THistoricoUpdateService"
        )

        service = update_service()

        return {
            "message": "Registro de T_HISTORICO atualizado com sucesso.",
            "data": service.execute(schema),
        }

    # ----------------------------------------------------
    # Exclui um registro
    # ----------------------------------------------------
    def delete(self, schema: THistoricoIdSchema):
        delete_service = self.dynamic_import.service(
            "t_historico_delete_service", "THistoricoDeleteService"
        )

        service = delete_service()

        return {
            "message": "Registro de T_HISTORICO removido com sucesso.",
            "data": service.execute(schema),
        }
