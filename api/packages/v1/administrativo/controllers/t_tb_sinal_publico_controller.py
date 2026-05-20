from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoDescricaoSchema,
    TTbSinalPublicoIdSchema,
    TTbSinalPublicoSaveSchema,
    TTbSinalPublicoUpdateSchema,
)


class TTbSinalPublicoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_tb_sinal_publico")

    def index(self):
        index_service = self.dynamic_import.service(
            "t_tb_sinal_publico_index_service",
            "TTbSinalPublicoIndexService",
        )
        self.indexService = index_service()

        return {
            "message": "Sinais publicos localizados com sucesso",
            "data": self.indexService.execute(),
        }

    def show(self, sinal_publico_schema: TTbSinalPublicoIdSchema):
        show_service = self.dynamic_import.service(
            "t_tb_sinal_publico_show_service",
            "TTbSinalPublicoShowService",
        )
        self.show_service = show_service()

        return {
            "message": "Sinal publico localizado com sucesso",
            "data": self.show_service.execute(sinal_publico_schema),
        }

    def get_by_descricao(self, sinal_publico_schema: TTbSinalPublicoDescricaoSchema):
        show_service = self.dynamic_import.service(
            "t_tb_sinal_publico_get_descricao_service",
            "TTbSinalPublicoGetByDescricaoService",
        )
        self.show_service = show_service()

        return {
            "message": "Sinal publico localizado com sucesso",
            "data": self.show_service.execute(sinal_publico_schema, True),
        }

    def save(self, sinal_publico_schema: TTbSinalPublicoSaveSchema):
        save_service = self.dynamic_import.service(
            "t_tb_sinal_publico_save_service",
            "TTbSinalPublicoSaveService",
        )
        self.save_service = save_service()

        return {
            "message": "Sinal publico salvo com sucesso",
            "data": self.save_service.execute(sinal_publico_schema),
        }

    def update(
        self,
        tb_sinalpublico_id: int,
        sinal_publico_schema: TTbSinalPublicoUpdateSchema,
    ):
        update_service = self.dynamic_import.service(
            "t_tb_sinal_publico_update_service",
            "TTbSinalPublicoUpdateService",
        )
        self.update_service = update_service()

        return {
            "message": "Sinal publico atualizado com sucesso",
            "data": self.update_service.execute(tb_sinalpublico_id, sinal_publico_schema),
        }

    def delete(self, sinal_publico_schema: TTbSinalPublicoIdSchema):
        delete_service = self.dynamic_import.service(
            "t_tb_sinal_publico_delete_service",
            "TTbSinalPublicoDeleteService",
        )
        self.delete_service = delete_service()

        return {
            "message": "Sinal publico removido com sucesso",
            "data": self.delete_service.execute(sinal_publico_schema),
        }
