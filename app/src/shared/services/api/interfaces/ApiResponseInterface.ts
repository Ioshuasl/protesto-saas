export default interface ApiResponseInterface<T = any> {
  status: number;
  message: string;
  data?: T | T[] | null;
}
