export default interface withClientErrorHandlerInterface<T = any> {
  status: number;
  data?: T;
  message?: string;
}
