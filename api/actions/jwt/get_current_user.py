import json

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from actions.jwt.verify_token import VerifyToken

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token", auto_error=False
)


def get_current_user(request: Request, token: str | None = Depends(oauth2_scheme)):
    # Main flow: JWT bearer token via Authorization header.
    if token:
        verify_token = VerifyToken()
        result = verify_token.execute(token)

        if result["status"] != "valid":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=result.get("message", "Token invalido ou expirado"),
                headers={"WWW-Authenticate": "Bearer"},
            )

        return result["payload"]

    # Fallback flow: session cookie (sid) set during authenticate.
    session_user = request.session.get("user")
    if session_user:
        return {"type": "session", "data": json.dumps(session_user)}

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
        headers={"WWW-Authenticate": "Bearer"},
    )
