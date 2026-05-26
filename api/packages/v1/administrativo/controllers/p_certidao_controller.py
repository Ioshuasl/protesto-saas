from actions.data.query_params_parser import QueryParams
from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoConsultaApresentanteSchema,
    PCertidaoIdSchema,
    PCertidaoIndexSchema,
    PCertidaoSaveSchema,
    PCertidaoUpdateSchema,
)


class PCertidaoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("p_certidao")

    def index(
        self,
        certidao_index_schema: PCertidaoIndexSchema,
        query_params: QueryParams,
    ):
        index_service = self.dynamic_import.service(
            "p_certidao_index_service",
            "IndexService",
        )
        result = index_service().execute(certidao_index_schema, query_params)
        return {
            "message": "Certidões localizadas com sucesso",
            "data": result["rows"],
            "pagination": result["pagination"],
        }

    def consulta_apresentante(
        self, consulta_schema: PCertidaoConsultaApresentanteSchema
    ):
        consulta_service = self.dynamic_import.service(
            "p_certidao_consulta_apresentante_service",
            "ConsultaApresentanteService",
        )
        return {
            "message": "Consulta de apresentante realizada com sucesso",
            "data": consulta_service().execute(consulta_schema),
        }

    def show(self, certidao_schema: PCertidaoIdSchema):
        show_service = self.dynamic_import.service(
            "p_certidao_show_service",
            "ShowService",
        )
        return {
            "message": "Certidão localizada com sucesso",
            "data": show_service().execute(certidao_schema),
        }

    def save(self, certidao_schema: PCertidaoSaveSchema):
        save_service = self.dynamic_import.service(
            "p_certidao_save_service",
            "SaveService",
        )
        return {
            "message": "Certidão salva com sucesso",
            "data": save_service().execute(certidao_schema),
        }

    def update(
        self,
        certidao_id: int,
        certidao_schema: PCertidaoUpdateSchema,
    ):
        update_service = self.dynamic_import.service(
            "p_certidao_update_service",
            "UpdateService",
        )
        return {
            "message": "Certidão atualizada com sucesso",
            "data": update_service().execute(certidao_id, certidao_schema),
        }

    def cancelar(self, certidao_schema: PCertidaoIdSchema):
        cancelar_service = self.dynamic_import.service(
            "p_certidao_cancelar_service",
            "CancelarService",
        )
        return {
            "message": "Certidão cancelada com sucesso",
            "data": cancelar_service().execute(certidao_schema),
        }

    def delete(self, certidao_schema: PCertidaoIdSchema):
        delete_service = self.dynamic_import.service(
            "p_certidao_delete_service",
            "DeleteService",
        )
        return {
            "message": "Certidão removida com sucesso",
            "data": delete_service().execute(certidao_schema),
        }
