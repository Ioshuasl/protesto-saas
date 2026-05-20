from typing import Optional, Tuple


def infer_numero_genero(role_ctx: dict) -> Optional[Tuple[str, str]]:
    if not isinstance(role_ctx, dict):
        return None

    quantity = role_ctx.get("quantity")
    if not isinstance(quantity, int) or quantity <= 0:
        return None

    sexos = role_ctx.get("sexos") or []
    if not isinstance(sexos, list):
        return None

    sexos_normalizados = [str(sexo).upper() for sexo in sexos]

    numero = "S" if quantity == 1 else "P"

    if "M" in sexos_normalizados:
        genero = "M"
    elif "F" in sexos_normalizados:
        genero = "F"
    else:
        return None

    return numero, genero
