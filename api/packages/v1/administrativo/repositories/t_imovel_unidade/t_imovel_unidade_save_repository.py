from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import TImovelUnidadeSaveSchema


class TImovelUnidadeSaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela t_t_imovel_unidade.
    """

    def execute(self, t_imovel_unidade_save_schema: TImovelUnidadeSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_imovel_unidade_save_schema (TUnidadeImovelUnidadeSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Montagem do SQL
            # ----------------------------------------------------
            sql = """
                INSERT INTO T_IMOVEL_UNIDADE (
                    IMOVEL_UNIDADE_ID,
                    IMOVEL_ID,
                    NUMERO_UNIDADE,
                    QUADRA,
                    AREA,
                    SUPERQUADRA,
                    CONJUNTO,
                    BLOCO,
                    AREA_DESCRITIVA,
                    CARACTERISTICA,
                    RESERVA_FLORESTAL,
                    GEO_REFERENCIAMENTO,
                    LOGRADOURO,
                    TB_TIPOLOGRADOURO_ID,
                    SELECIONADO,
                    COMPLEMENTO,
                    TIPO_IMOVEL,
                    TIPO_CONSTRUCAO,
                    TEXTO,
                    NUMERO_EDIFICACAO,
                    IPTU,
                    CCIR,
                    NIRF,
                    LOTE,
                    TORRE,
                    NOMELOTEAMENTO,
                    NOMECONDOMINIO,
                    NUMERO,
                    CNM_NUMERO,
                    IMOVEL_PUBLICO_UNIAO,
                    SPU_RIP,
                    CAT,
                    INSCRICAO_MUNICIPAL,
                    CIB,
                    AREA_CONSTRUIDA
                ) VALUES (
                    :imovel_unidade_id,
                    :imovel_id,
                    :numero_unidade,
                    :quadra,
                    :area,
                    :superquadra,
                    :conjunto,
                    :bloco,
                    :area_descritiva,
                    :caracteristica,
                    :reserva_florestal,
                    :geo_referenciamento,
                    :logradouro,
                    :tb_tipologradouro_id,
                    :selecionado,
                    :complemento,
                    :tipo_imovel,
                    :tipo_construcao,
                    :texto,
                    :numero_edificacao,
                    :iptu,
                    :ccir,
                    :nirf,
                    :lote,
                    :torre,
                    :nomeloteamento,
                    :nomecondominio,
                    :numero,
                    :cnm_numero,
                    :imovel_publico_uniao,
                    :spu_rip,
                    :cat,
                    :inscricao_municipal,
                    :cib,
                    :area_construida
                )
                RETURNING *;
            """

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = {
                'imovel_unidade_id': t_imovel_unidade_save_schema.imovel_unidade_id,
                'imovel_id': t_imovel_unidade_save_schema.imovel_id,
                'numero_unidade': t_imovel_unidade_save_schema.numero_unidade,
                'quadra': t_imovel_unidade_save_schema.quadra,
                'area': t_imovel_unidade_save_schema.area,
                'superquadra': t_imovel_unidade_save_schema.superquadra,
                'conjunto': t_imovel_unidade_save_schema.conjunto,
                'bloco': t_imovel_unidade_save_schema.bloco,
                'area_descritiva': t_imovel_unidade_save_schema.area_descritiva,
                'caracteristica': t_imovel_unidade_save_schema.caracteristica,
                'reserva_florestal': t_imovel_unidade_save_schema.reserva_florestal,
                'geo_referenciamento': t_imovel_unidade_save_schema.geo_referenciamento,
                'logradouro': t_imovel_unidade_save_schema.logradouro,
                'tb_tipologradouro_id': t_imovel_unidade_save_schema.tb_tipologradouro_id,
                'selecionado': t_imovel_unidade_save_schema.selecionado,
                'complemento': t_imovel_unidade_save_schema.complemento,
                'tipo_imovel': t_imovel_unidade_save_schema.tipo_imovel,
                'tipo_construcao': t_imovel_unidade_save_schema.tipo_construcao,
                'texto': t_imovel_unidade_save_schema.texto,
                'numero_edificacao': t_imovel_unidade_save_schema.numero_edificacao,
                'iptu': t_imovel_unidade_save_schema.iptu,
                'ccir': t_imovel_unidade_save_schema.ccir,
                'nirf': t_imovel_unidade_save_schema.nirf,
                'lote': t_imovel_unidade_save_schema.lote,
                'torre': t_imovel_unidade_save_schema.torre,
                'nomeloteamento': t_imovel_unidade_save_schema.nomeloteamento,
                'nomecondominio': t_imovel_unidade_save_schema.nomecondominio,
                'numero': t_imovel_unidade_save_schema.numero,
                'cnm_numero': t_imovel_unidade_save_schema.cnm_numero,
                'imovel_publico_uniao': t_imovel_unidade_save_schema.imovel_publico_uniao,
                'spu_rip': t_imovel_unidade_save_schema.spu_rip,
                'cat': t_imovel_unidade_save_schema.cat,
                'inscricao_municipal': t_imovel_unidade_save_schema.inscricao_municipal,
                'cib': t_imovel_unidade_save_schema.cib,
                'area_construida': t_imovel_unidade_save_schema.area_construida,
            }

            # Execução do sql
            return self.run_and_return(sql, params)
        
        except Exception as e:
        
            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar T_IMOVEL_UNIDADE: {e}"
            )