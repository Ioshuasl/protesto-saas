import Schema from '@/shared/abstracts/Schema';
import empty from '@/shared/actions/validations/empty';

export default class ApiSchema extends Schema {
  private _url?: string;
  private _prefix?: string;
  private _endpoint?: string;
  private _contentType?: string;
  private _token?: string;

  get url(): string | undefined {
    return this._url;
  }

  set url(value: string | undefined) {
    this._url = value;

    // Verifica se esta preenchido
    if (empty(this._url)) {
      this.errors = 'A informação "URL" deve esta preenchido';
    }
  }

  get prefix(): string | undefined {
    return this._prefix;
  }

  set prefix(value: string | undefined) {
    this._prefix = value;

    // Verifica se esta preenchido
    if (empty(this._prefix)) {
      this.errors = 'A informação "Prefixo" deve esta preenchido';
    }
  }

  get endpoint(): string | undefined {
    return this._endpoint;
  }

  set endpoint(value: string | undefined) {
    this._endpoint = value;

    // Verifica se esta preenchido
    if (empty(this._endpoint)) {
      this.errors = 'A informação "Endpoint" deve esta preenchido';
    }
  }

  get contentType(): string | undefined {
    return this._contentType;
  }

  set contentType(value: string | undefined) {
    this._contentType = value;

    // Verifica se esta preenchido
    if (empty(this._contentType)) {
      this.errors = 'A informação "Tipo de Conteúdo" deve esta preenchido';
    }
  }

  get token(): string | undefined {
    return this._token;
  }

  set token(value: string | undefined) {
    this._token = value;
  }
}
