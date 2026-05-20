from actions.system.exceptions import BusinessRuleException


class GedFilenameBuilder:
    """
    Builder responsavel por gerar nomes de arquivos GED
    com base no codigo do sistema (G_SISTEMA.TIPO_CARTORIO).
    """

    DEFAULT_EXT = ".spd"
    DEFAULT_PAD = 6

    # -------------------------
    # Regras por TIPO_CARTORIO
    # -------------------------

    SISTEMA_RULES = {
        # 1 - Tabelionato de Notas
        1: {
            # aceita string OU inteiro
            "subtipos": {
                "BIOMETRIA": "Biometria",
                "FOTO": "F",
                "IMAGEM": "F",
                "LIVRO": "L",
                "INDICE": "I",
                "CARTAO": "C",
                "DOCUMENTO": "D",
                "PROCURACAO": "P",
                "ATO": "A",
                "CARTÃO": "C",
                "PROCURAÇÃO": "P",
                1: "F",  # FOTO
                2: "F",  # IMAGEM
                3: "L",  # LIVRO
                4: "I",  # INDICE
                5: "Biometria",  # Biometria
                6: "P",  # Procuracao
                7: "C",  # Cartao
                8: "D",  # Documento
            },
            # sufixo independente por subtipo
            "sufixos_subtipos": {
                "BIOMETRIA": "B",
                "FOTO": "F",
                "IMAGEM": "F",
                "LIVRO": "L",
                "INDICE": "I",
                "CARTAO": "C",
                "DOCUMENTO": "D",
                "PROCURACAO": "P",
                "ATO": "#",
                "CARTÃƒO": "C",
                "PROCURAÃ‡ÃƒO": "P",
                1: "F",  # FOTO
                2: "F",  # IMAGEM
                3: "L",  # LIVRO
                4: "I",  # INDICE
                5: "B",  # Biometria
                6: "P",  # Procuracao
                7: "C",  # Cartao
                8: "D",  # Documento
            },
            "sufixo": "C",
        },
        # 2 - Registro de Imoveis
        2: {
            "prefixo": "F",
            "sufixo": "I",
        },
        # 3 - Registro Civil
        3: {
            "prefixo": "F",
            "sufixo": "C",
        },
        # 4 - RTD
        4: {
            "prefixo": "F",
            "sufixo": "D",
        },
        # 5 - Protesto
        5: {
            "prefixo": "F",
            "sufixo": "P",
        },
    }

    # -------------------------
    # API publica
    # -------------------------

    @classmethod
    def build(
        cls,
        *,
        serventia: int,
        record_id: int,
        subtipo: int | str | None = None,
        ext: str | None = None,
        pad: int | None = None,
    ) -> str:
        """
        Gera nome do arquivo GED conforme TIPO_CARTORIO.
        """

        cls._validate_inputs(serventia, record_id)

        regra = cls._resolve_regra(serventia)

        # Prefixo
        if "subtipos" in regra:
            if subtipo is None:
                raise BusinessRuleException(
                    "Subtipo obrigatorio para Tabelionato de Notas (TIPO_CARTORIO=1)"
                )

            prefixo, subtipo_key = cls._resolve_subtipo(regra["subtipos"], subtipo)
            sufixo = cls._resolve_sufixo_subtipo(regra, subtipo_key)
        else:
            prefixo = regra["prefixo"]
            sufixo = regra["sufixo"]
        record_fmt = str(record_id).zfill(pad or cls.DEFAULT_PAD)
        ext = ext or cls.DEFAULT_EXT

        return f"{prefixo}_{record_fmt}{sufixo}{ext}"

    # -------------------------
    # Helpers internos
    # -------------------------

    @classmethod
    def _validate_inputs(cls, serventia: int, record_id: int) -> None:
        if not isinstance(serventia, int):
            raise BusinessRuleException("serventia deve ser int")

        if serventia not in cls.SISTEMA_RULES:
            raise BusinessRuleException(f"TIPO_CARTORIO nao suportado: {serventia}")

        if not isinstance(record_id, int) or record_id <= 0:
            raise BusinessRuleException("record_id invalido")

    @classmethod
    def _resolve_regra(cls, serventia: int) -> dict:
        return cls.SISTEMA_RULES[serventia]

    @classmethod
    def _resolve_subtipo(cls, subtipos: dict, subtipo: int | str) -> tuple[str, int | str]:
        # subtipo vindo como INT (banco)
        if isinstance(subtipo, int):
            if subtipo not in subtipos:
                raise BusinessRuleException(f"Subtipo nao suportado: {subtipo}")
            return subtipos[subtipo], subtipo

        # subtipo vindo como STRING
        if isinstance(subtipo, str):
            key = subtipo.strip().upper()
            if key not in subtipos:
                raise BusinessRuleException(f"Subtipo nao suportado: {subtipo}")
            return subtipos[key], key

        raise BusinessRuleException("subtipo deve ser int ou str")

    @classmethod
    def _resolve_sufixo_subtipo(cls, regra: dict, subtipo_key: int | str) -> str:
        sufixos_subtipos = regra.get("sufixos_subtipos", {})
        if isinstance(sufixos_subtipos, dict) and subtipo_key in sufixos_subtipos:
            return sufixos_subtipos[subtipo_key]
        return regra["sufixo"]
