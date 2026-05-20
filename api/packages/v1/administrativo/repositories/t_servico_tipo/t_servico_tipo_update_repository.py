from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):
    """
    Repositório para a operação de atualização na tabela T_SERVICO_TIPO.
    """

    def execute(self, servico_tipo_id : int, servico_tipo_schema: TServicoTipoUpdateSchema):
        """
        Executa a atualização de um registro na tabela.
        
        Args:
            servico_tipo_id (int): O ID do registro a ser atualizado.
            servico_tipo_schema (TServicoTipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O registro atualizado.
            
        Raises:
            HTTPException: Se o registro não for encontrado ou ocorrer um erro na atualização.
        """
        try:
            updates = []
            params = {}

            # --- Campos da T_SERVICO_TIPO que podem ser atualizados (com base na DDL) ---
            
            if servico_tipo_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = servico_tipo_schema.descricao

            if servico_tipo_schema.valor is not None:
                updates.append("VALOR = :valor")
                params["valor"] = servico_tipo_schema.valor

            if servico_tipo_schema.tipo_item is not None:
                updates.append("TIPO_ITEM = :tipo_item")
                params["tipo_item"] = servico_tipo_schema.tipo_item

            if servico_tipo_schema.requer_autorizacao is not None:
                updates.append("REQUER_AUTORIZACAO = :requer_autorizacao")
                params["requer_autorizacao"] = servico_tipo_schema.requer_autorizacao

            if servico_tipo_schema.requer_biometria is not None:
                updates.append("REQUER_BIOMETRIA = :requer_biometria")
                params["requer_biometria"] = servico_tipo_schema.requer_biometria

            if servico_tipo_schema.tipo_pessoa is not None:
                updates.append("TIPO_PESSOA = :tipo_pessoa")
                params["tipo_pessoa"] = servico_tipo_schema.tipo_pessoa

            if servico_tipo_schema.tb_reconhecimentotipo_id is not None:
                updates.append("TB_RECONHECIMENTOTIPO_ID = :tb_reconhecimentotipo_id")
                params["tb_reconhecimentotipo_id"] = servico_tipo_schema.tb_reconhecimentotipo_id

            if servico_tipo_schema.tipo_permissao_cpf is not None:
                updates.append("TIPO_PERMISSAO_CPF = :tipo_permissao_cpf")
                params["tipo_permissao_cpf"] = servico_tipo_schema.tipo_permissao_cpf

            if servico_tipo_schema.requer_abonador is not None:
                updates.append("REQUER_ABONADOR = :requer_abonador")
                params["requer_abonador"] = servico_tipo_schema.requer_abonador

            if servico_tipo_schema.requer_representante is not None:
                updates.append("REQUER_REPRESENTANTE = :requer_representante")
                params["requer_representante"] = servico_tipo_schema.requer_representante

            if servico_tipo_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = servico_tipo_schema.situacao

            if servico_tipo_schema.requer_cpf is not None:
                updates.append("REQUER_CPF = :requer_cpf")
                params["requer_cpf"] = servico_tipo_schema.requer_cpf

            if servico_tipo_schema.servico_padrao is not None:
                updates.append("SERVICO_PADRAO = :servico_padrao")
                params["servico_padrao"] = servico_tipo_schema.servico_padrao

            if servico_tipo_schema.maximo_pessoa is not None:
                updates.append("MAXIMO_PESSOA = :maximo_pessoa")
                params["maximo_pessoa"] = servico_tipo_schema.maximo_pessoa

            if servico_tipo_schema.alterar_valor is not None:
                updates.append("ALTERAR_VALOR = :alterar_valor")
                params["alterar_valor"] = servico_tipo_schema.alterar_valor

            if servico_tipo_schema.servico_caixa_id is not None:
                updates.append("SERVICO_CAIXA_ID = :servico_caixa_id")
                params["servico_caixa_id"] = servico_tipo_schema.servico_caixa_id

            if servico_tipo_schema.lancar_taxa is not None:
                updates.append("LANCAR_TAXA = :lancar_taxa")
                params["lancar_taxa"] = servico_tipo_schema.lancar_taxa

            if servico_tipo_schema.lancar_fundesp is not None:
                updates.append("LANCAR_FUNDESP = :lancar_fundesp")
                params["lancar_fundesp"] = servico_tipo_schema.lancar_fundesp

            if servico_tipo_schema.liberar_desconto is not None:
                updates.append("LIBERAR_DESCONTO = :liberar_desconto")
                params["liberar_desconto"] = servico_tipo_schema.liberar_desconto

            if servico_tipo_schema.fundesp_automatica is not None:
                updates.append("FUNDESP_AUTOMATICA = :fundesp_automatica")
                params["fundesp_automatica"] = servico_tipo_schema.fundesp_automatica

            if servico_tipo_schema.lancar_valor_documento is not None:
                updates.append("LANCAR_VALOR_DOCUMENTO = :lancar_valor_documento")
                params["lancar_valor_documento"] = servico_tipo_schema.lancar_valor_documento

            if servico_tipo_schema.valor_fixo is not None:
                updates.append("VALOR_FIXO = :valor_fixo")
                params["valor_fixo"] = servico_tipo_schema.valor_fixo

            if servico_tipo_schema.emolumento_id is not None:
                updates.append("EMOLUMENTO_ID = :emolumento_id")
                params["emolumento_id"] = servico_tipo_schema.emolumento_id

            if servico_tipo_schema.ato_praticado is not None:
                updates.append("ATO_PRATICADO = :ato_praticado")
                params["ato_praticado"] = servico_tipo_schema.ato_praticado

            if servico_tipo_schema.selar is not None:
                updates.append("SELAR = :selar")
                params["selar"] = servico_tipo_schema.selar

            if servico_tipo_schema.frenteverso is not None:
                updates.append("FRENTEVERSO = :frenteverso")
                params["frenteverso"] = servico_tipo_schema.frenteverso

            if servico_tipo_schema.pagina_acrescida is not None:
                updates.append("PAGINA_ACRESCIDA = :pagina_acrescida")
                params["pagina_acrescida"] = servico_tipo_schema.pagina_acrescida

            if servico_tipo_schema.emolumento_obrigatorio is not None:
                updates.append("EMOLUMENTO_OBRIGATORIO = :emolumento_obrigatorio")
                params["emolumento_obrigatorio"] = servico_tipo_schema.emolumento_obrigatorio

            if servico_tipo_schema.apresentante_selo is not None:
                updates.append("APRESENTANTE_SELO = :apresentante_selo")
                params["apresentante_selo"] = servico_tipo_schema.apresentante_selo

            if servico_tipo_schema.renovacao_cartao is not None:
                updates.append("RENOVACAO_CARTAO = :renovacao_cartao")
                params["renovacao_cartao"] = servico_tipo_schema.renovacao_cartao

            if servico_tipo_schema.etiqueta_unica is not None:
                updates.append("ETIQUETA_UNICA = :etiqueta_unica")
                params["etiqueta_unica"] = servico_tipo_schema.etiqueta_unica

            if servico_tipo_schema.transferencia_veiculo is not None:
                updates.append("TRANSFERENCIA_VEICULO = :transferencia_veiculo")
                params["transferencia_veiculo"] = servico_tipo_schema.transferencia_veiculo

            if servico_tipo_schema.usar_a4 is not None:
                updates.append("USAR_A4 = :usar_a4")
                params["usar_a4"] = servico_tipo_schema.usar_a4

            if servico_tipo_schema.averbacao is not None:
                updates.append("AVERBACAO = :averbacao")
                params["averbacao"] = servico_tipo_schema.averbacao

            # -------------------------------------------------------------------------
            
            if not updates:
                return False

            params["servico_tipo_id"] = servico_tipo_id
            sql = f"UPDATE T_SERVICO_TIPO SET {', '.join(updates)} WHERE SERVICO_TIPO_ID = :servico_tipo_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)
            
            # O result é uma tupla/objeto com os campos do registro, 
            # verificamos a existência do campo chave para confirmação
            if not result or not getattr(result, 'servico_tipo_id', None):
                # Informa que não existe o registro a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum SERVIÇO TIPO localizado para esta solicitação'
                )
            
            # Se houver um resultado e ele tiver o ID, a atualização foi bem-sucedida
            if result:
                return result

        except Exception as e:
            # Informa que houve uma falha na atualização
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o SERVIÇO TIPO: {e}"
            )