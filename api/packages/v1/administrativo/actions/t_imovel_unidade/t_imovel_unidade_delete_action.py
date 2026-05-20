from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel_unidade.t_imovel_unidade_delete_repository import (
    TImovelUnidadeDeleteRepository,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeSchema,
)


class TImovelUnidadeDeleteAction(BaseAction):
    
    def execute(self, t_imovel_unidade_id_schema: TImovelUnidadeSchema):
        
        # Instanciamento do repositório
        t_imovel_unidade_delete_repository = TImovelUnidadeDeleteRepository()

        # Execução do repositório
        return t_imovel_unidade_delete_repository.execute(t_imovel_unidade_id_schema)
