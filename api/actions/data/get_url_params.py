from fastapi import Request


async def get_url_params(request: Request):
    return dict(request.query_params)
