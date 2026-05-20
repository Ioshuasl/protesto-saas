from decimal import ROUND_HALF_UP, Decimal


class Values:

    @staticmethod
    def percent(value: Decimal, percent: Decimal) -> Decimal:

        return value / percent

    @staticmethod
    def money(scale: str, value: Decimal) -> Decimal:

        return value.quantize(scale, rounding=ROUND_HALF_UP)
