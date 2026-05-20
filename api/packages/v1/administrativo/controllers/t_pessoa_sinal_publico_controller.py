from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
    TPessoaSinalPublicoSaveSchema,
    TPessoaSinalPublicoSchema,
    TPessoaSinalPublicoUpdateSchema,
)


class TPessoaSinalPublicoController:
    def __init__(self):
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("t_pessoa_sinal_publico")

    def index(self, data: TPessoaSinalPublicoSchema):
        service = self.dynamic_import.service(
            "t_pessoa_sinal_publico_index_service",
            "TPessoaSinalPublicoIndexService",
        )
        self.index_service = service()

        return {
            "message": "Pessoas sinais publicos localizados com sucesso",
            "data": self.index_service.execute(data),
        }

    def show(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoIdSchema):
        service = self.dynamic_import.service(
            "t_pessoa_sinal_publico_show_service",
            "TPessoaSinalPublicoShowService",
        )
        self.show_service = service()

        return {
            "message": "Pessoa sinal publico localizado com sucesso",
            "data": self.show_service.execute(pessoa_sinal_publico_schema),
        }

    def save(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoSaveSchema):
        service = self.dynamic_import.service(
            "t_pessoa_sinal_publico_save_service",
            "TPessoaSinalPublicoSaveService",
        )
        self.save_service = service()

        return {
            "message": "Pessoa sinal publico salvo com sucesso",
            "data": self.save_service.execute(pessoa_sinal_publico_schema),
        }

    def update(
        self,
        pessoa_sinalpublico_id: int,
        pessoa_sinal_publico_schema: TPessoaSinalPublicoUpdateSchema,
    ):
        service = self.dynamic_import.service(
            "t_pessoa_sinal_publico_update_service",
            "TPessoaSinalPublicoUpdateService",
        )
        self.update_service = service()

        return {
            "message": "Pessoa sinal publico atualizado com sucesso",
            "data": self.update_service.execute(
                pessoa_sinalpublico_id,
                pessoa_sinal_publico_schema,
            ),
        }

    def delete(self, pessoa_sinal_publico_schema: TPessoaSinalPublicoIdSchema):
        service = self.dynamic_import.service(
            "t_pessoa_sinal_publico_delete_service",
            "TPessoaSinalPublicoDeleteService",
        )
        self.delete_service = service()

        return {
            "message": "Pessoa sinal publico removido com sucesso",
            "data": self.delete_service.execute(pessoa_sinal_publico_schema),
        }
