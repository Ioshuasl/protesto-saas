from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.nfse.schemas.nfse_schema import NfseSaveSchema


class NfseSaveRepository(BaseRepository):
    def execute(self, data: NfseSaveSchema):
        try:
            sql = """
                INSERT INTO NFSE (
                    ID_NFSE, DATA_HORA, NUMNFSE, SERIE, DATAEMISSAO, TOTAL_SERVICOS,
                    TOTAL_DEDUCOES, TOTAL_COFINS, TOTAL_INSS, TOTAL_IR, TOTAL_CSLL,
                    TOTAL_ISS_RETIDO, OUTRAS_RETENCOES, DESCONTO_INCONDICIONADO,
                    DESCONTO_CONDIDIONADO, BASE_CALCULO, ALIQUOTA, TOTAL_LIQUIDO,
                    COD_CNAE, COD_TRIB_MUN, DISCRIMINACAO, CODIGO_MUNICIPIO,
                    CODIGO_PAIS, COD_MUN_INCID, PRESTADOR_CNPJ, PRESTADOR_IM,
                    PRESTADOR_COD_UF, PRESTADOR_CODMUN, PRESTADOR_RAZAO_SOCIAL,
                    TOMADOR_CNPJ, TOMADOR_IM, TOMADOR_RAZAO_SOCIAL, TOMADOR_ENDERECO,
                    TOMADOR_NUMEND, TOMADOR_COMPLEMENTO, TOMADOR_BAIRRO, TOMADOR_UF,
                    TOMADOR_CODPAIS, TOMADOR_CEP, TOMADOR_PAIS, TOMADOR_IE,
                    TOMADOR_TELEFONE, TOMADOR_EMAIL, ID_CLIENTE, DT_APROVADO,
                    NUMERO_RPS, NUMERO_VERIFICACAO, VALOR_ISS, ITEM_LISTA, TOTAL_PIS,
                    NATUREZA_OPERACAO, REGIME_TRIB, ISS_RETIDO, NOME_PREFEITURA,
                    CODIGO_CANCELAMENTO, LINK, PRESTADOR_MAIL, PRESTADOR_TELEFONE,
                    PRESTADOR_CEP, INCIDENCIA_ISS, CODIGO_NBS, ENT_GOV, CLASS_TRIB,
                    ID_PARAMETROS, TOMADOR_MUNICIPIO, DATA_CANCELAMENTO,
                    SIMPLES_NACIONAL, TOMADOR_CODMUN, PRESTADOR_FANTASIA,
                    PRESTADOR_ENDERECO, PRESTADOR_NUM_ENDERECO,
                    PRESTADOR_COMPLEMENTO_END, PRESTADOR_UF, PRESTADOR_BAIRRO,
                    DESCRICAO_ITEM_LISTA, INDICADOR_OPERACAO
                ) VALUES (
                    :id_nfse, :data_hora, :numnfse, :serie, :dataemissao, :total_servicos,
                    :total_deducoes, :total_cofins, :total_inss, :total_ir, :total_csll,
                    :total_iss_retido, :outras_retencoes, :desconto_incondicionado,
                    :desconto_condidionado, :base_calculo, :aliquota, :total_liquido,
                    :cod_cnae, :cod_trib_mun, :discriminacao, :codigo_municipio,
                    :codigo_pais, :cod_mun_incid, :prestador_cnpj, :prestador_im,
                    :prestador_cod_uf, :prestador_codmun, :prestador_razao_social,
                    :tomador_cnpj, :tomador_im, :tomador_razao_social, :tomador_endereco,
                    :tomador_numend, :tomador_complemento, :tomador_bairro, :tomador_uf,
                    :tomador_codpais, :tomador_cep, :tomador_pais, :tomador_ie,
                    :tomador_telefone, :tomador_email, :id_cliente, :dt_aprovado,
                    :numero_rps, :numero_verificacao, :valor_iss, :item_lista, :total_pis,
                    :natureza_operacao, :regime_trib, :iss_retido, :nome_prefeitura,
                    :codigo_cancelamento, :link, :prestador_mail, :prestador_telefone,
                    :prestador_cep, :incidencia_iss, :codigo_nbs, :ent_gov, :class_trib,
                    :id_parametros, :tomador_municipio, :data_cancelamento,
                    :simples_nacional, :tomador_codmun, :prestador_fantasia,
                    :prestador_endereco, :prestador_num_endereco,
                    :prestador_complemento_end, :prestador_uf, :prestador_bairro,
                    :descricao_item_lista, :indicador_operacao
                )
                RETURNING
                    ID_NFSE,
                    NUMNFSE,
                    DATAEMISSAO,
                    TOTAL_LIQUIDO,
                    TOMADOR_RAZAO_SOCIAL
            """

            params = data.model_dump()
            return self.run_and_return(sql, params)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar NFSE: {exc}",
            )
