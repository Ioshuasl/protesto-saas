from __future__ import annotations

from decimal import Decimal
from typing import Iterable, Optional, Protocol, Any


class EmolumentoItemLike(Protocol):
    """Protocolo mínimo esperado para um item de emolumento."""

    valor_inicio: Optional[Decimal]
    valor_fim: Optional[Decimal]


class GEmolumentoItemGetFaixaValorAction:
    """
    Responsável por escolher, dentre uma coleção de itens de emolumento,
    aquele cuja faixa [valor_inicio, valor_fim] contem o valor_documento.
    - Se houver mais de um candidato, prioriza o de maior valor_inicio (faixa mais específica).
    - Se não houver faixa que contenha o valor_documento, tenta a faixa 'aberta' (valor_fim nulo).
    - Persistindo a ausência, retorna o item cujo valor_inicio é o mais próximo abaixo do valor_documento.
    """

    @staticmethod
    def _para_decimal(valor: Any, padrao: str = "0") -> Decimal:
        return valor if isinstance(valor, Decimal) else Decimal(str(valor or padrao))

    def execute(
        self,
        itens: Iterable[EmolumentoItemLike],
        valor_documento: Decimal,
    ) -> EmolumentoItemLike:
        lista = list(itens)
        if not lista:
            raise ValueError("Nenhum item de emolumento foi informado.")

        valor_doc = self._para_decimal(valor_documento)

        candidatos: list[tuple[Decimal, Decimal, EmolumentoItemLike]] = []
        abertos: list[tuple[Decimal, EmolumentoItemLike]] = []
        abaixo: list[tuple[Decimal, EmolumentoItemLike]] = []

        for item in lista:
            ini = self._para_decimal(getattr(item, "valor_inicio", None))
            fim_raw = getattr(item, "valor_fim", None)
            fim = (
                self._para_decimal(fim_raw, padrao="Infinity")
                if fim_raw is not None
                else Decimal("Infinity")
            )

            if ini <= valor_doc <= fim:
                candidatos.append((ini, fim, item))
            elif fim == Decimal("Infinity") and ini <= valor_doc:
                abertos.append((ini, item))
            elif ini <= valor_doc:
                abaixo.append((ini, item))

        if candidatos:
            candidatos.sort(key=lambda t: (t[0], t[1]))  # maior ini e menor fim
            return candidatos[-1][2]

        if abertos:
            abertos.sort(key=lambda t: t[0])  # maior ini
            return abertos[-1][1]

        if abaixo:
            abaixo.sort(key=lambda t: t[0])  # maior ini
            return abaixo[-1][1]

        # Fallback: não há faixa adequada nem valores abaixo; devolve o de menor valor_inicio
        lista_ordenada = sorted(
            lista, key=lambda it: self._para_decimal(getattr(it, "valor_inicio", None))
        )
        return lista_ordenada[0]
