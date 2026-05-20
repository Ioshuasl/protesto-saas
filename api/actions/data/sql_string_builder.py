from typing import List


class SqlStringBuilder:
    """
    Classe utilitária para construção segura de strings SQL
    utilizadas em cláusulas IN.

    Uso:
        SqlStringBuilder.to_in_clause("A,B,C")
        -> "'A','B','C'"
    """

    @staticmethod
    def to_in_clause(value: str | None) -> str:
        """
        Recebe string separada por vírgula:
            "SAAS_MODELO_ETIQUETA,SAAS"

        Retorna:
            "'SAAS_MODELO_ETIQUETA','SAAS'"

        Observação:
            - Remove espaços extras
            - Remove valores vazios
            - Remove duplicados
            - Escapa aspas simples
        """

        parts = SqlStringBuilder._normalize(value)

        if not parts:
            return ""

        return ",".join(f"'{item}'" for item in parts)

    # ------------------------------------------------------
    # MÉTODOS INTERNOS
    # ------------------------------------------------------

    @staticmethod
    def _normalize(value: str | None) -> List[str]:
        if not value:
            return []

        normalized = []
        seen = set()

        for item in value.split(","):
            cleaned = item.strip()

            if not cleaned:
                continue

            # Escapa aspas simples para evitar quebra de SQL
            cleaned = cleaned.replace("'", "''")

            # Remove duplicados preservando ordem
            if cleaned not in seen:
                seen.add(cleaned)
                normalized.append(cleaned)

        return normalized
