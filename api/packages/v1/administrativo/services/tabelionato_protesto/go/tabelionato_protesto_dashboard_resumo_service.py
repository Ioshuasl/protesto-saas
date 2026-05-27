from packages.v1.administrativo.actions.tabelionato_protesto.tabelionato_protesto_dashboard_resumo_action import (
    TabelionatoProtestoDashboardResumoAction,
)


class TabelionatoProtestoDashboardResumoService:
    def execute(self):
        return TabelionatoProtestoDashboardResumoAction().execute()
