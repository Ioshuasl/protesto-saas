import GConfigInterface from '@/shared/interfaces/GConfigInterface';

export default class ConfigParamHelper {
  private constructor() {}

  static getValorByNome<TFallback = undefined>(
    params: GConfigInterface[] | null | undefined,
    nome: string,
    fallback?: TFallback,
  ): string | TFallback {
    if (!Array.isArray(params) || !nome) return fallback as TFallback;

    const item = params.find((p) => p?.nome === nome);
    if (!item) return fallback as TFallback;

    // como "valor" na interface é string|undefined, retornamos string ou fallback
    return item.valor ?? (fallback as TFallback);
  }

  static getValorByNomeOrThrow(
    params: GConfigInterface[] | null | undefined,
    nome: string,
  ): string {
    const val = ConfigParamHelper.getValorByNome(params, nome, undefined);
    if (val === undefined) {
      throw new Error(`Parâmetro não encontrado para nome="${nome}"`);
    }
    return val;
  }

  static getItemByNome(
    params: GConfigInterface[] | null | undefined,
    nome: string,
  ): GConfigInterface | undefined {
    if (!Array.isArray(params) || !nome) return undefined;
    return params.find((p) => p?.nome === nome);
  }

  static toMap(params: GConfigInterface[] | null | undefined): Map<string, GConfigInterface> {
    const map = new Map<string, GConfigInterface>();
    if (!Array.isArray(params)) return map;

    for (const item of params) {
      const key = item?.nome;
      if (typeof key === 'string' && key.length) {
        map.set(key, item);
      }
    }
    return map;
  }

  static getValorFromMap<TFallback = undefined>(
    map: Map<string, GConfigInterface> | null | undefined,
    nome: string,
    fallback?: TFallback,
  ): string | TFallback {
    if (!map || !nome) return fallback as TFallback;

    const item = map.get(nome);
    if (!item) return fallback as TFallback;

    return item.valor ?? (fallback as TFallback);
  }
}
