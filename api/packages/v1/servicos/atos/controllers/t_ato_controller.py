from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoAnteriorClearSchema,
    TAtoAnteriorUpdateSchema,
    TAtoClearTextoAssinaturaSchema,
    TAtoClearTextoFinalizacaoSchema,
    TAtoClearTextoSchema,
    TAtoIdSchema,
    TAtoLavraturaSchema,
    TAtoSaveMinuta,
    TAtoSaveSchema,
    TAtoTextoAssinatura,
    TAtoTextoAssinaturaUpdateSchema,
    TAtoTextoFinalizacao,
    TAtoTextoVisualizarSchema,
    TAtoUpdateSchema,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_ato_anterior_service import (
    TAtoAtoAnteriorService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_cancelar_ato_service import (
    TAtoCancelarAtoService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_anterior_update_service import (
    TAtoAnteriorUpdateService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_anterior_clear_service import (
    TAtoAnteriorClearService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_clear_texto_assinatura_service import (
    TAtoClearTextoAssinaturaService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_clear_texto_finalizacao_service import (
    TAtoClearTextoFinalizacaoService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_clear_texto_service import (
    TAtoClearTextoService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_delete_service import (
    TAtoDeleteService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_display_texto_service import (
    TAtoDisplayTextoService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_get_texto_assinatura_service import (
    TAtoGetTextoAssinaturaService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_get_texto_corpo_service import (
    TAtoGetTextoCorpoService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_get_texto_finalizacao_service import (
    TAtoGetTextoFinalizacaoService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_index_arquivos_service import (
    TAtoIndexrquivosService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_index_service import (
    TAtoIndexService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_lavrar_ato_service import (
    TAtoLavrarAtoService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_protocolar_service import (
    TAtoProtocolarService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_reativar_ato_service import (
    TAtoReativarAtoService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_recibo_protocolo_service import (
    TAtoReciboProtocoloService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_retirar_lavratura_service import (
    TAtoRetirarLavraturaService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_save_service import (
    TAtoSaveService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_show_service import (
    TAtoShowService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_update_minuta_service import (
    TAtoUpdateMinutaService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_update_service import (
    TAtoUpdateService,
)
from packages.v1.servicos.atos.services.t_ato.go.t_ato_update_texto_assinatura_service import (
    TAtoUpdateTextoAssinaturaService,
)


class TAtoController:
    def index(self):
        return {
            "message": "Registros de T_ATO localizados com sucesso.",
            "data": TAtoIndexService().execute(),
        }

    def show(self, data: TAtoIdSchema):
        return {
            "message": "Registro de T_ATO localizado com sucesso.",
            "data": TAtoShowService().execute(data),
        }

    def ato_anterior(self, data: TAtoIdSchema):
        return {
            "message": "Dados do ato anterior localizados com sucesso.",
            "data": TAtoAtoAnteriorService().execute(data),
        }

    def update_ato_anterior(self, data: TAtoAnteriorUpdateSchema):
        return {
            "message": "Dados do ato anterior atualizados com sucesso.",
            "data": TAtoAnteriorUpdateService().execute(data),
        }

    def clear_ato_anterior(self, data: TAtoAnteriorClearSchema):
        return {
            "message": "Dados do ato anterior limpos com sucesso.",
            "data": TAtoAnteriorClearService().execute(data),
        }

    def index_arquivos(self, data: TAtoIdSchema):
        return {
            "message": "Registro de T_ATO localizado com sucesso.",
            "data": TAtoIndexrquivosService().execute(data),
        }

    def get_texto(self, data: TAtoIdSchema):
        return {
            "message": "Registro de T_ATO localizado com sucesso.",
            "data": TAtoGetTextoCorpoService().execute(data),
        }

    def display_texto(self, data: TAtoTextoVisualizarSchema):
        return {
            "message": "Registro de T_ATO localizado com sucesso.",
            "data": TAtoDisplayTextoService().execute(data),
        }

    def show_finalizacao(self, data: TAtoTextoFinalizacao):
        return {
            "message": "Registro de T_ATO localizado com sucesso.",
            "data": TAtoGetTextoFinalizacaoService().execute(data),
        }

    def show_assinatura(self, data: TAtoTextoAssinatura):
        return {
            "message": "Registro de T_ATO localizado com sucesso.",
            "data": TAtoGetTextoAssinaturaService().execute(data),
        }

    def save(self, data: TAtoSaveSchema):
        return {
            "message": "Registro de T_ATO salvo com sucesso.",
            "data": TAtoSaveService().execute(data),
        }

    def update(self, data: TAtoUpdateSchema):
        return {
            "message": "Registro de T_ATO atualizado com sucesso.",
            "data": TAtoUpdateService().execute(data),
        }

    def update_minuta(self, data: TAtoSaveMinuta):
        return {
            "message": "Registro de T_ATO atualizado com sucesso.",
            "data": TAtoUpdateMinutaService().execute(data),
        }

    def update_assinatura(self, data: TAtoTextoAssinaturaUpdateSchema):
        return {
            "message": "Registro de T_ATO atualizado com sucesso.",
            "data": TAtoUpdateTextoAssinaturaService().execute(data),
        }

    def clear_texto(self, data: TAtoClearTextoSchema):
        return {
            "message": "Texto de T_ATO limpo com sucesso.",
            "data": TAtoClearTextoService().execute(data),
        }

    def clear_assinatura(self, data: TAtoClearTextoAssinaturaSchema):
        return {
            "message": "Texto de assinatura de T_ATO limpo com sucesso.",
            "data": TAtoClearTextoAssinaturaService().execute(data),
        }

    def clear_finalizacao(self, data: TAtoClearTextoFinalizacaoSchema):
        return {
            "message": "Texto de finalizacao de T_ATO limpo com sucesso.",
            "data": TAtoClearTextoFinalizacaoService().execute(data),
        }

    def delete(self, data: TAtoIdSchema):
        return {
            "message": "Registro de T_ATO removido com sucesso.",
            "data": TAtoDeleteService().execute(data),
        }

    def protocolar(self, data: TAtoIdSchema):
        return {
            "message": "Ato protocolado com sucesso.",
            "data": TAtoProtocolarService().execute(data),
        }

    def recibo_protocolo(self, data: TAtoIdSchema):
        return {
            "message": "Dados do recibo de protocolo obtidos com sucesso.",
            "data": TAtoReciboProtocoloService().execute(data),
        }

    def lavrar_ato(self, data: TAtoLavraturaSchema):
        return {
            "message": "Ato lavrado com sucesso.",
            "data": TAtoLavrarAtoService().execute(data),
        }

    def retirar_lavratura(self, data: TAtoIdSchema):
        return {
            "message": "Lavratura retirada com sucesso.",
            "data": TAtoRetirarLavraturaService().execute(data),
        }

    def cancelar_ato(self, data: TAtoIdSchema):
        return {
            "message": "Ato cancelado com sucesso.",
            "data": TAtoCancelarAtoService().execute(data),
        }

    def reativar_ato(self, data: TAtoIdSchema):
        return {
            "message": "Ato reativado com sucesso.",
            "data": TAtoReativarAtoService().execute(data),
        }
