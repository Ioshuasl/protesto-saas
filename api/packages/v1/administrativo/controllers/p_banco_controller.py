from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoIdSchema,
    PBancoIndexSchema,
    PBancoSaveSchema,
    PBancoUpdateSchema,
)


class PBancoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_banco")

    def index(self, banco_index_schema: PBancoIndexSchema):
        index_service = self.dynamic_import.service(
            "p_banco_index_service",
            "IndexService",
        )
        return {
            "message": "Bancos localizados com sucesso",
            "data": index_service().execute(banco_index_schema),
        }

    def show(self, banco_schema: PBancoIdSchema):
        show_service = self.dynamic_import.service(
            "p_banco_show_service",
            "ShowService",
        )
        return {
            "message": "Banco localizado com sucesso",
            "data": show_service().execute(banco_schema),
        }

    def save(self, banco_schema: PBancoSaveSchema):
        save_service = self.dynamic_import.service(
            "p_banco_save_service",
            "SaveService",
        )
        return {
            "message": "Banco salvo com sucesso",
            "data": save_service().execute(banco_schema),
        }

    def update(self, banco_id: int, banco_schema: PBancoUpdateSchema):
        update_service = self.dynamic_import.service(
            "p_banco_update_service",
            "UpdateService",
        )
        return {
            "message": "Banco atualizado com sucesso",
            "data": update_service().execute(banco_id, banco_schema),
        }

    def delete(self, banco_schema: PBancoIdSchema):
        delete_service = self.dynamic_import.service(
            "p_banco_delete_service",
            "DeleteService",
        )
        return {
            "message": "Banco removido com sucesso",
            "data": delete_service().execute(banco_schema),
        }
