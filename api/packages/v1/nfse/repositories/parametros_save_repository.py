from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.nfse.schemas.parametros_schema import ParametrosSaveSchema


class ParametrosSaveRepository(BaseRepository):
    def execute(self, data: ParametrosSaveSchema):
        try:
            sql = """
                INSERT INTO PARAMETROS (
                    ID_PARAMETROS, RAZAO_SOCIAL, CODIGO_IBGE, CNPJ, CEP, IM, CODIGO_UF, CNAE,
                    EMAIL, TELEFONE, SIMPLES_NACIONAL, SERIE, ALIQUOTA_ISS, CLASS_TRIBUTARIA,
                    CODIGO_NBS, ITEM_LISTA, NATUREZA_PADRAO, NOME_PREFEITURA,
                    NUMERO_SERIE_CERTIFICADO, UF, LOGO_CARTORIO, SMTP_EMAIL, SMTP_CORPO_EMAIL,
                    SMTP_SENHA, SMTP_PORTA, SMTP_SSL, SMTP_TLS, SMTP_USUARIO, USUARIO_WEB_SERVICE,
                    SENHA_USUARIO_WEB_SERVICE, ENDERECO, NUMERO_ENDERECO, BAIRRO,
                    COMPLEMENTO_ENDERECO, CODIGO_TRIBUTACAO, MUNICIPIO, DESCRICAO_ITEM_LISTA,
                    FANTASIA, DATA_HORA, REGIME_TRIBUTARIO, INDICADOR_OPERACAO, SMTP_HOST,
                    SMTP_ASSUNTO
                ) VALUES (
                    :id_parametros, :razao_social, :codigo_ibge, :cnpj, :cep, :im, :codigo_uf,
                    :cnae, :email, :telefone, :simples_nacional, :serie, :aliquota_iss,
                    :class_tributaria, :codigo_nbs, :item_lista, :natureza_padrao,
                    :nome_prefeitura, :numero_serie_certificado, :uf, :logo_cartorio,
                    :smtp_email, :smtp_corpo_email, :smtp_senha, :smtp_porta, :smtp_ssl,
                    :smtp_tls, :smtp_usuario, :usuario_web_service, :senha_usuario_web_service,
                    :endereco, :numero_endereco, :bairro, :complemento_endereco,
                    :codigo_tributacao, :municipio, :descricao_item_lista, :fantasia,
                    :data_hora, :regime_tributario, :indicador_operacao, :smtp_host,
                    :smtp_assunto
                )
                RETURNING *
            """
            return self.run_and_return(sql, data.model_dump())
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar PARAMETROS: {exc}",
            )

