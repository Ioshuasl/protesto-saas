/**
 * EnvLoader - Leitor universal de variáveis de ambiente
 * Compatível com Windows, Linux e EasyPanel (Docker)
 *
 * Suporta prefixos (ex: ORIUS_APP_), conversão automática de tipos
 * e acesso via ponto (ex: env.group("ORIUS_APP").api_url).
 */

type EnvValue = string | number | boolean | object | null;

class EnvLoader {
  private static instance: EnvLoader;
  private cache: Record<string, EnvValue> = {};

  private constructor() {
    this.loadAll();
  }

  /**
   * Singleton global
   */
  public static getInstance(): EnvLoader {
    if (!EnvLoader.instance) {
      EnvLoader.instance = new EnvLoader();
    }
    return EnvLoader.instance;
  }

  /**
   * Conversão automática de tipos
   */
  private convert(value: string): EnvValue {
    const trimmed = value.trim();

    // Boolean
    if (['true', 'false'].includes(trimmed.toLowerCase())) {
      return trimmed.toLowerCase() === 'true';
    }

    // Inteiro
    if (/^-?\d+$/.test(trimmed)) {
      return parseInt(trimmed, 10);
    }

    // Float
    if (/^-?\d+\.\d+$/.test(trimmed)) {
      return parseFloat(trimmed);
    }

    // JSON
    try {
      const parsed = JSON.parse(trimmed);
      if (typeof parsed === 'object') return parsed;
    } catch {
      /* ignora */
    }

    return trimmed;
  }

  /**
   * Carrega todas as variáveis do sistema
   */
  private loadAll(): void {
    for (const [key, value] of Object.entries(process.env)) {
      if (value !== undefined) {
        this.cache[key] = this.convert(value);
      }
    }
  }

  /**
   * Recarrega variáveis (útil em hot reload)
   */
  public reload(): void {
    this.cache = {};
    this.loadAll();
  }

  /**
   * Retorna todas as variáveis carregadas
   */
  public all(): Record<string, EnvValue> {
    return this.cache;
  }

  /**
   * Retorna variável específica
   */
  public get(key: string, required = true): EnvValue {
    const value = this.cache[key];
    if (value === undefined) {
      if (required) throw new Error(`Variável de ambiente obrigatória não encontrada: ${key}`);
      return null;
    }
    return value;
  }

  /**
   * Retorna variável com valor padrão
   */
  public getOrDefault<T extends EnvValue>(key: string, defaultValue: T): T {
    const value = this.get(key, false);
    return (value ?? defaultValue) as T;
  }

  /**
   * Retorna todas as variáveis que começam com um prefixo (ex: ORIUS_APP_)
   * Remove o prefixo e normaliza os nomes em minúsculo.
   * Retorna um objeto acessível via ponto (Proxy).
   */
  public group(prefix: string): Record<string, EnvValue> {
    const normalizedPrefix = prefix.toUpperCase().replace(/^_+|_+$/g, '') + '_';
    const groupData: Record<string, EnvValue> = {};

    for (const [key, value] of Object.entries(this.cache)) {
      if (key.startsWith(normalizedPrefix)) {
        const cleanKey = key.slice(normalizedPrefix.length).toLowerCase();
        groupData[cleanKey] = value;
      }
    }

    // Cria proxy para acesso via ponto, com mensagem amigável
    return new Proxy(groupData, {
      get(target, prop: string) {
        if (prop in target) {
          return target[prop];
        }
        throw new Error(`Variável '${prop}' não encontrada no grupo '${prefix}'`);
      },
    });
  }
}

// Exporta instância única
export const env = EnvLoader.getInstance();
