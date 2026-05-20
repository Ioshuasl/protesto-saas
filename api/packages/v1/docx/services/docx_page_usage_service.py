class DOCXPageUsageService:
    """
    Calcula quantas folhas serao utilizadas a partir da quantidade de paginas
    e da regra de frente/verso.
    """

    _FRENTE_VERSO_TRUE_VALUES = {"S", "SIM", "1", "Y", "YES", "FV"}

    def execute(self, total_paginas: int, frente_verso) -> dict:
        paginas = int(total_paginas or 0)
        if paginas <= 0:
            raise ValueError("total_paginas deve ser maior que zero.")

        usa_frente_verso = self._is_frente_verso_enabled(frente_verso)
        folhas_utilizadas = (paginas + 1) // 2 if usa_frente_verso else paginas

        return {
            "total_paginas": paginas,
            "usa_frente_verso": usa_frente_verso,
            "folhas_utilizadas": folhas_utilizadas,
        }

    def _is_frente_verso_enabled(self, frente_verso) -> bool:
        frente_verso_raw = str(frente_verso or "").strip().upper()
        return frente_verso_raw in self._FRENTE_VERSO_TRUE_VALUES
