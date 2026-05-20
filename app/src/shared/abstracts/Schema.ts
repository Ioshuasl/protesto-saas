export default class Schema {
  private _errors: any[] = [];

  get errors(): any {
    return this._errors;
  }

  set errors(value: any) {
    this._errors.push(value);
  }
}
