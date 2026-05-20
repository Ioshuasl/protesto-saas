from fastapi import Request, HTTPException, status


def get_session_user(request: Request) -> dict:
    user = request.session.get("user")
    if not user:
        # ajuste conforme sua regra (pode só retornar None)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão inválida"
        )
    return user
