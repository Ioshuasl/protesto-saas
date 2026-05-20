export default interface IConfig {
  state: string;
  api: {
    url: string;
    prefix: string;
    content_type: string;
  };
}
