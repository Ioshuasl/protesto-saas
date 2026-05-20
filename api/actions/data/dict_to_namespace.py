import json
from types import SimpleNamespace


def dict_to_namespace(d):
    """
    Converte dict (ou string JSON) recursivamente em SimpleNamespace.
    """
    # Caso venha uma string JSON
    if isinstance(d, str):
        try:
            # tenta fazer parse do JSON interno
            parsed = json.loads(d)
            # se for mesmo JSON, converte recursivamente
            return dict_to_namespace(parsed)
        except (json.JSONDecodeError, TypeError):
            # não era JSON, retorna string normal
            return d

    # Caso seja um dicionário
    if isinstance(d, dict):
        return SimpleNamespace(**{k: dict_to_namespace(v) for k, v in d.items()})

    # Caso seja lista/tupla
    if isinstance(d, list):
        return [dict_to_namespace(i) for i in d]
    if isinstance(d, tuple):
        return tuple(dict_to_namespace(i) for i in d)

    # Caso base (valor simples)
    return d
