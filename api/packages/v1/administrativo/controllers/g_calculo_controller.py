from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.administrativo.schemas.g_calculo_schema import (
    GCalculoRapidoSchema,
    GCalculoServico,
)


class GCalculoController:

    def __init__(self):
        # ----------------------------------------------------
        # Inicialização do DynamicImport
        # ----------------------------------------------------
        self.dynamic_import = DynamicImport()
        self.dynamic_import.set_package("administrativo")
        self.dynamic_import.set_table("g_calculo")

    # ----------------------------------------------------
    # Lista todos os registros de G_EMOLUMENTO
    # ----------------------------------------------------
    def rapido(self, g_calculo_rapido_schema: GCalculoRapidoSchema):

        # Importação da classe desejada
        rapido_service = self.dynamic_import.service(
            "g_calculo_rapido_service", "GCalculoRapidoService"
        )

        # Instância da classe service
        self.rapido_service = rapido_service()

        # Execução da listagem
        return {
            "message": "Cálculo realizado com sucesso",
            "data": self.rapido_service.execute(g_calculo_rapido_schema),
        }

        # ----------------------------------------------------

    # Lista todos os registros de G_EMOLUMENTO
    # ----------------------------------------------------
    def servico(self, g_calculo_servico: GCalculoServico):

        # Importação da classe desejada
        service = self.dynamic_import.service(
            "g_calculo_servico_service", "GCalculoServicoService"
        )

        # Instância da classe service
        self.service = service()

        # Execução da listagem
        return {
            "message": "Cálculo realizado com sucesso",
            "data": self.service.execute(g_calculo_servico),
        }
