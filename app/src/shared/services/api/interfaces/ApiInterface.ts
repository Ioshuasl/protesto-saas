import { Methods } from '../enums/ApiMethodEnum';

export type ApiUrlType = 'primary' | 'secondary';

export default interface ApiInterface {
  method: Methods;
  endpoint: string;
  body?: object | FormData;
  urlType?: ApiUrlType;
}
