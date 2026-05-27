from packages.v1.administrativo.services.tabelionato_protesto.go.tabelionato_protesto_dashboard_resumo_service import (
    TabelionatoProtestoDashboardResumoService,
)
from packages.v1.administrativo.services.tabelionato_protesto.go.tabelionato_protesto_dashboard_funil_service import (
    TabelionatoProtestoDashboardFunilService,
)


class TabelionatoProtestoController:
    def dashboard_resumo(self):
        data = TabelionatoProtestoDashboardResumoService().execute()
        return {
            "message": "Resumo do dashboard carregado com sucesso",
            "data": data,
        }

    def dashboard_funil(self):
        data = TabelionatoProtestoDashboardFunilService().execute()
        return {
            "message": "Funil semanal do dashboard carregado com sucesso",
            "data": data,
        }
