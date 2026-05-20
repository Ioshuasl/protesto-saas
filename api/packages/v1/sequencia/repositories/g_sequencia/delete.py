from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from abstracts.repository import BaseRepository


class Delete(BaseRepository):

    def execute(self, sequencia_schema: GSequenciaDeleteSchema):

        if sequencia_schema.contador:

            # 1) garante existência (atômico)
            sql_upsert = """
                UPDATE OR INSERT INTO G_SEQUENCIA (TABELA, SEQUENCIA)
                VALUES (UPPER(:tabela), 0)
                MATCHING (TABELA)
            """

            self.run(sql_upsert, {"tabela": sequencia_schema.tabela})

            # 2) trava a linha REAL do contador
            sql_lock = """
                SELECT SEQUENCIA
                FROM G_SEQUENCIA
                WHERE TABELA = UPPER(:tabela)
                WITH LOCK
            """

            res = self.fetch_one(sql_lock, {"tabela": sequencia_schema.tabela})

            if not res:
                raise RuntimeError(
                    f"G_SEQUENCIA não possui registro para a tabela {sequencia_schema.tabela}"
                )

            current_seq = res["sequencia"]

            # proteção contra corrupção
            if sequencia_schema.sequencia > current_seq:
                raise Exception(
                    f"Tentativa de liberar sequência maior que o topo "
                    f"({sequencia_schema.sequencia} > {current_seq})"
                )

            # não era o topo → não mexe
            if sequencia_schema.sequencia < current_seq:
                return False

            # era o topo → decrementa
            new_seq = current_seq - 1 if current_seq > 0 else 0

            sql_update = """
                UPDATE G_SEQUENCIA
                SET SEQUENCIA = :seq
                WHERE TABELA = UPPER(:tabela)
                RETURNING SEQUENCIA
            """

            return self.run_and_return(
                sql_update, {"seq": new_seq, "tabela": sequencia_schema.tabela}
            )

        # 1) Descobre o nome da PK a partir dos metadados (como feito no Checkout)
        sql_pk = """
            SELECT
                sg.RDB$FIELD_NAME AS primary_key
            FROM RDB$RELATION_CONSTRAINTS rc
            JOIN RDB$INDEX_SEGMENTS sg
              ON rc.RDB$INDEX_NAME = sg.RDB$INDEX_NAME
            WHERE rc.RDB$CONSTRAINT_TYPE = 'PRIMARY KEY'
              AND rc.RDB$RELATION_NAME = UPPER(:tabela)
            ORDER BY sg.RDB$FIELD_POSITION
        """
        pk_result = self.fetch_one(sql_pk, {"tabela": sequencia_schema.tabela})

        if not pk_result:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Tabela {sequencia_schema.tabela} não possui chave primária",
            )

        pk_field = pk_result["primary_key"].strip()

        # 2) Aplica o LOCK na G_SEQUENCIA para evitar que outros processos gerem IDs
        # enquanto recalculamos o novo máximo
        sql_lock = """
            SELECT SEQUENCIA FROM G_SEQUENCIA
            WHERE TABELA = UPPER(:tabela)
            WITH LOCK
        """
        current_seq_res = self.fetch_one(sql_lock, {"tabela": sequencia_schema.tabela})

        if not current_seq_res:

            sql_upsert = """
                UPDATE OR INSERT INTO G_SEQUENCIA (TABELA, SEQUENCIA)
                VALUES (UPPER(:tabela), :seq)
                MATCHING (TABELA)
            """

            self.run(sql_upsert, {"tabela": sequencia_schema.tabela, "seq": 0})

            return False

        # 3) Verifica se o ID deletado era o último da tabela. Se não for, não precisa atualizar a sequência
        sql_check = f"""
            SELECT FIRST 1 {pk_field} AS last_id
            FROM {sequencia_schema.tabela}
            ORDER BY {pk_field} DESC
            WITH LOCK
        """
        last_id_res = self.fetch_one(sql_check)

        # Se não era o último, nem mexe na sequência
        if last_id_res and last_id_res["last_id"] > sequencia_schema.sequencia:
            return False

        # Se a tabela estiver vazia, o new_max será 0, reiniciando a sequência
        new_max = last_id_res["last_id"] if last_id_res else 0

        # 5) Atualiza a G_SEQUENCIA com o novo topo da tabela
        sql_update = """
            UPDATE G_SEQUENCIA
            SET SEQUENCIA = :sequencia
            WHERE TABELA = UPPER(:tabela)
            RETURNING TABELA, SEQUENCIA
        """
        params = {"sequencia": new_max, "tabela": sequencia_schema.tabela}

        response = self.run_and_return(sql_update, params)

        # Retorna o estado atualizado da sequência
        return response
