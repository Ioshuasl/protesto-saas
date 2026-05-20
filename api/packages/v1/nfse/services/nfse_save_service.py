from datetime import datetime
from decimal import Decimal

from packages.v1.nfse.actions.nfse_save_action import NfseSaveAction
from packages.v1.nfse.schemas.nfse_schema import NfseSaveSchema
from packages.v1.nfse.services.parametros_last_service import ParametrosLastService


class NfseSaveService:
    def execute(self, data: NfseSaveSchema):
        parametros_last_service = ParametrosLastService()
        parametros = parametros_last_service.execute()

        def gv(obj, field_name: str, default=None):
            value = getattr(obj, field_name, None)
            if value is None:
                value = getattr(obj, field_name.upper(), None)
            return default if value is None else value

        codigo_ibge = gv(parametros, "codigo_ibge")
        codigo_uf = gv(parametros, "codigo_uf")
        if codigo_uf is None and codigo_ibge is not None:
            codigo_uf = int(str(codigo_ibge)[:2])

        valor_pedido = getattr(data, "total_servicos", None)
        valor_pago = getattr(data, "total_liquido", None)
        total_servicos = (
            Decimal(str(valor_pedido)) if valor_pedido is not None else None
        )
        total_liquido = (
            Decimal(str(valor_pago))
            if valor_pago is not None
            else (Decimal(str(valor_pedido)) if valor_pedido is not None else None)
        )

        def should_drop(value) -> bool:
            if value is None:
                return True
            if isinstance(value, Decimal):
                return value == Decimal("0")
            if isinstance(value, str):
                return value.strip() == "" or value.strip() == "0"
            if isinstance(value, (int, float)):
                return value == 0
            return False

        payload_data = {
            "id_parametros": gv(parametros, "id_parametros"),
            "id_cliente": getattr(data, "id_cliente", None),
            "data_hora": getattr(data, "data_hora", datetime.now()),
            "serie": gv(parametros, "serie"),
            "dataemissao": getattr(data, "dataemissao", datetime.now()),
            "total_servicos": total_servicos,
            "base_calculo": total_servicos,
            "aliquota": gv(parametros, "aliquota_iss"),
            "total_liquido": total_liquido,
            "valor_iss": getattr(data, "valor_iss", None),
            "cod_cnae": gv(parametros, "cnae"),
            "cod_trib_mun": gv(parametros, "codigo_tributacao"),
            "discriminacao": getattr(data, "discriminacao", None),
            "codigo_municipio": codigo_ibge,
            "codigo_pais": 1058,
            "cod_mun_incid": codigo_ibge,
            "prestador_cnpj": gv(parametros, "cnpj"),
            "prestador_im": gv(parametros, "im"),
            "prestador_cod_uf": codigo_uf,
            "prestador_codmun": codigo_ibge,
            "prestador_razao_social": gv(parametros, "razao_social"),
            "tomador_razao_social": getattr(data, "tomador_razao_social", None),
            "tomador_cnpj": getattr(data, "tomador_cnpj", None),
            "item_lista": gv(parametros, "item_lista"),
            "natureza_operacao": gv(parametros, "natureza_padrao"),
            "regime_trib": gv(parametros, "regime_tributario"),
            "nome_prefeitura": gv(parametros, "nome_prefeitura"),
            "prestador_mail": gv(parametros, "email"),
            "prestador_telefone": gv(parametros, "telefone"),
            "prestador_cep": gv(parametros, "cep"),
            "codigo_nbs": gv(parametros, "codigo_nbs"),
            "class_trib": gv(parametros, "class_tributaria"),
            "simples_nacional": gv(parametros, "simples_nacional"),
            "prestador_fantasia": gv(parametros, "fantasia"),
            "prestador_endereco": gv(parametros, "endereco"),
            "prestador_num_endereco": gv(parametros, "numero_endereco"),
            "prestador_complemento_end": gv(parametros, "complemento_endereco"),
            "prestador_uf": gv(parametros, "uf"),
            "prestador_bairro": gv(parametros, "bairro"),
            "descricao_item_lista": gv(parametros, "descricao_item_lista"),
            "indicador_operacao": gv(parametros, "indicador_operacao"),
        }
        payload = NfseSaveSchema(
            **{k: v for k, v in payload_data.items() if not should_drop(v)}
        )

        action = NfseSaveAction()
        return action.execute(payload)
