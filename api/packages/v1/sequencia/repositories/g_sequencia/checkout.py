from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from abstracts.repository import BaseRepository
from fastapi import HTTPException, status


class Checkout(BaseRepository):

    def execute(self, sequencia_schema: GSequenciaSchema):

        # Se for contador, incrementa e retorna a sequência
        if sequencia_schema.contador:

            sql_seq = """
                SELECT SEQUENCIA
                FROM G_SEQUENCIA
                WHERE TABELA = UPPER(:tabela)
                WITH LOCK
            """

            gSequenciaResult = self.fetch_one(sql_seq, {
                "tabela": sequencia_schema.tabela
            })

            # Se não existir → cria começando do 1
            if not gSequenciaResult:

                sql_insert = """
                    INSERT INTO G_SEQUENCIA (TABELA, SEQUENCIA)
                    VALUES (UPPER(:tabela), 1)
                """

                self.run(sql_insert, {
                    "tabela": sequencia_schema.tabela
                })

                return

            nova_seq = gSequenciaResult["sequencia"] + 1

            sql_update = """
                UPDATE G_SEQUENCIA
                SET SEQUENCIA = :seq
                WHERE TABELA = UPPER(:tabela)
            """

            self.run(sql_update, {
                "seq": nova_seq,
                "tabela": sequencia_schema.tabela
            })

            return

        # 1) Descobre PK
        sql_pk = """ 
            SELECT sg.RDB$FIELD_NAME AS primary_key
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
                detail=f"Tabela {sequencia_schema.tabela} não possui chave primária"
            )

        pk_field = pk_result["primary_key"].strip()

        # 2) Descobre topo REAL da tabela
        sql_last = f"""
            SELECT FIRST 1 {pk_field} AS last_id
            FROM {sequencia_schema.tabela}
            ORDER BY {pk_field} DESC
            WITH LOCK
        """

        last_id = self.fetch_one(sql_last)

        current_max = last_id["last_id"] if last_id else 0

        # 3) LOCK na sequência → mutex global
        sql_seq = """
            SELECT SEQUENCIA
            FROM G_SEQUENCIA
            WHERE TABELA = UPPER(:tabela)
            WITH LOCK
        """

        gSequenciaResult = self.fetch_one(sql_seq, {"tabela": sequencia_schema.tabela})        

        # CASO NÃO EXISTA → cria
        if not gSequenciaResult:

            sql_upsert = """
                UPDATE OR INSERT INTO G_SEQUENCIA (TABELA, SEQUENCIA)
                VALUES (UPPER(:tabela), :sequencia)
                MATCHING (TABELA)
            """

            self.run(sql_upsert, {
                "tabela": sequencia_schema.tabela,
                "sequencia": current_max
            })

            return

        db_seq = gSequenciaResult["sequencia"]

        # Divergência perigosa (sequência maior)
        if db_seq > current_max:

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Sequência ({db_seq}) maior que o topo da tabela ({current_max}). Possível corrupção."
            )

        # Divergência comum → autocorrige
        if db_seq < current_max:

            sql_fix = """
                UPDATE G_SEQUENCIA
                SET SEQUENCIA = :seq
                WHERE TABELA = UPPER(:tabela)
            """

            self.run(sql_fix, {
                "seq": current_max,
                "tabela": sequencia_schema.tabela
            })
        
        return
