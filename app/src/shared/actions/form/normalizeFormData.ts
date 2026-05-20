type NormalizeFormDataOptions = {
  booleanFields?: string[];
  numberFields?: string[];
  stringFields?: string[];
};

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value);
}

function shouldCoerceToNumber(key: string, options: NormalizeFormDataOptions) {
  return options.numberFields?.includes(key) || /(^id$|_id$)/i.test(key);
}

function shouldCoerceToBoolean(key: string, options: NormalizeFormDataOptions) {
  return options.booleanFields?.includes(key) ?? false;
}

function shouldCoerceToString(key: string, options: NormalizeFormDataOptions) {
  return options.stringFields?.includes(key) ?? false;
}

function normalizePrimitive(
  key: string,
  value: unknown,
  options: NormalizeFormDataOptions,
): unknown {
  if (value === null || value === undefined || value === '') {
    return undefined;
  }

  if (shouldCoerceToNumber(key, options)) {
    if (typeof value === 'number') {
      return Number.isNaN(value) ? undefined : value;
    }

    if (typeof value === 'string') {
      const numericValue = Number(value);
      return Number.isNaN(numericValue) ? undefined : numericValue;
    }
  }

  if (shouldCoerceToBoolean(key, options)) {
    if (typeof value === 'boolean') return value;
    if (value === 'true' || value === '1') return true;
    if (value === 'false' || value === '0') return false;
    return undefined;
  }

  if (shouldCoerceToString(key, options)) {
    return String(value);
  }

  return value;
}

function normalizeValue(key: string, value: unknown, options: NormalizeFormDataOptions): unknown {
  if (Array.isArray(value)) {
    return value.map((item) => normalizeValue(key, item, options));
  }

  if (isPlainObject(value)) {
    return Object.fromEntries(
      Object.entries(value).map(([childKey, childValue]) => [
        childKey,
        normalizeValue(childKey, childValue, options),
      ]),
    );
  }

  return normalizePrimitive(key, value, options);
}

/**
 * Normaliza dados antes de popular o react-hook-form.
 * - Converte `null`, `undefined` e `''` em `undefined`
 * - Converte strings numéricas de campos `id`/`*_id` em `number`
 * - Permite coerção explícita por campo via opções
 * - Trata objetos e arrays recursivamente
 */
export default function normalizeFormData<T extends Record<string, unknown>>(
  data: T,
  options: NormalizeFormDataOptions = {},
): T {
  return Object.fromEntries(
    Object.entries(data).map(([key, value]) => [key, normalizeValue(key, value, options)]),
  ) as T;
}
