from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoIdSchema,
    TLivroAndamentoNaturezaIdSchema,
    TLivroAndamentoSaveSchema,
    TLivroAndamentoUpdateSchema,
)
from packages.v1.administrativo.services.t_livro_andamento.go.t_livro_andamento_delete_service import (
    TLivroAndamentoDeleteService,
)
from packages.v1.administrativo.services.t_livro_andamento.go.t_livro_andamento_first_aberto_by_natureza_service import (
    TLivroAndamentoFirstAbertoByNaturezaService,
)
from packages.v1.administrativo.services.t_livro_andamento.go.t_livro_andamento_index_service import (
    TLivroAndamentoIndexService,
)
from packages.v1.administrativo.services.t_livro_andamento.go.t_livro_andamento_save_service import (
    TLivroAndamentoSaveService,
)
from packages.v1.administrativo.services.t_livro_andamento.go.t_livro_andamento_show_service import (
    TLivroAndamentoShowService,
)
from packages.v1.administrativo.services.t_livro_andamento.go.t_livro_andamento_update_service import (
    TLivroAndamentoUpdateService,
)


class TLivroAndamentoController:
    """Controller to orchestrate T_LIVRO_ANDAMENTO CRUD."""

    def index(self):
        return {
            "message": "Registros de T_LIVRO_ANDAMENTO localizados com sucesso.",
            "data": TLivroAndamentoIndexService().execute(),
        }

    def first_aberto_by_natureza(self, schema: TLivroAndamentoNaturezaIdSchema):
        return {
            "message": "Livro de andamento aberto localizado com sucesso.",
            "data": TLivroAndamentoFirstAbertoByNaturezaService().execute(schema),
        }

    def show(self, schema: TLivroAndamentoIdSchema):
        return {
            "message": "Registro de T_LIVRO_ANDAMENTO localizado com sucesso.",
            "data": TLivroAndamentoShowService().execute(schema),
        }

    def save(self, schema: TLivroAndamentoSaveSchema):
        return {
            "message": "Registro de T_LIVRO_ANDAMENTO salvo com sucesso.",
            "data": TLivroAndamentoSaveService().execute(schema),
        }

    def update(self, schema: TLivroAndamentoUpdateSchema):
        return {
            "message": "Registro de T_LIVRO_ANDAMENTO atualizado com sucesso.",
            "data": TLivroAndamentoUpdateService().execute(schema),
        }

    def delete(self, schema: TLivroAndamentoIdSchema):
        return {
            "message": "Registro de T_LIVRO_ANDAMENTO removido com sucesso.",
            "data": TLivroAndamentoDeleteService().execute(schema),
        }
