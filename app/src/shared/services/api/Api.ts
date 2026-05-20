import TokenGet from '@/shared/actions/token/TokenGet';
import ApiSchema from '@/shared/services/api/schemas/ApiSchema';

import ApiInterface from './interfaces/ApiInterface';

export default class API {
  private ApiSchema: ApiSchema;

  constructor() {
    // Classe validadora das informaes
    this.ApiSchema = new ApiSchema();
  }

  public async send(data: ApiInterface) {
    const _data = data;

    try {
      const urlType = _data.urlType ?? 'primary';
      const secondaryUrl =
        process.env.NEXT_PUBLIC_ORIUS_APP_API_SECONDARY_URL || 'http://localhost:8000';
      const primaryUrl =
        process.env.NEXT_PUBLIC_ORIUS_APP_API_URL || process.env.NEXT_PUBLIC_ORIUS_APP_API_SECONDARY_URL;
      const selectedBaseUrl = urlType === 'primary' ? primaryUrl : secondaryUrl;

      // Verifica se todos os dados esto corretos
      this.ApiSchema.url = selectedBaseUrl ? selectedBaseUrl + '/' : undefined;
      this.ApiSchema.prefix = process.env.NEXT_PUBLIC_ORIUS_APP_API_PREFIX + '/';
      this.ApiSchema.endpoint = _data.endpoint;
      this.ApiSchema.contentType = process.env.NEXT_PUBLIC_ORIUS_APP_API_CONTENT_TYPE;
      this.ApiSchema.token = await TokenGet();

      if (this.ApiSchema.errors.length > 0) {
        throw new Error(`Erros no schema: ${this.ApiSchema.errors.join(', ')}`);
      }

      const isFormData = typeof FormData !== 'undefined' && _data.body instanceof FormData;
      const filteredBody =
        _data.body && !isFormData
          ? Object.fromEntries(Object.entries(_data.body).filter(([_, v]) => v != null && v !== ''))
          : null;

      const endpoint = this.ApiSchema.endpoint ?? '';
      const isAbsoluteEndpoint = endpoint.startsWith('http://') || endpoint.startsWith('https://');
      const isRelativeEndpoint = endpoint.startsWith('/');
      const absoluteUrl = isAbsoluteEndpoint
        ? endpoint
        : isRelativeEndpoint
          ? endpoint
          : `${this.ApiSchema.url}${this.ApiSchema.prefix}${endpoint}`;
      const headers: Record<string, string> = {
        Accept: `${this.ApiSchema.contentType}`,
      };
      if (this.ApiSchema.token) {
        headers.Authorization = `Bearer ${this.ApiSchema.token}`;
      }
      if (!isFormData) {
        headers['Content-Type'] = `${this.ApiSchema.contentType}`;
      }

      const sentBody: BodyInit | null = isFormData
        ? (_data.body as FormData)
        : filteredBody
          ? JSON.stringify(filteredBody)
          : null;
      const isCrossOrigin =
        typeof window !== 'undefined' &&
        !isRelativeEndpoint &&
        !absoluteUrl.startsWith(window.location.origin);
      const credentials: RequestCredentials = isCrossOrigin ? 'omit' : 'include';

      const response = await fetch(absoluteUrl, {
        method: _data.method,
        headers,
        credentials,
        ...(sentBody && { body: sentBody }),
      });

      const responseData = await response.json();
      responseData.status = response.status;

      return responseData;
    } catch (error) {
      console.error('Erro ao enviar requisição:', error);
      throw error;
    }
  }
}
