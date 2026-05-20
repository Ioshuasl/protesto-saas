export default class Response {
  public handler(data: any) {
    switch (Number(data.status)) {
      case 400 | 404:
        this.status400(data);
    }

    return data;
  }

  private status400(data: any) {
    console.log(data.error);
  }
}
