from fastapi import HTTPException, status

from packages.v1.ged.schemas.ged_schema import GEDSaveBase64RequestSchema


class GEDSaveBase64PayloadAction:
    @staticmethod
    async def execute(data: GEDSaveBase64RequestSchema) -> str:
        payload = await data.request.json()

        base64_value = (payload or {}).get("base64")
        if not isinstance(base64_value, str) or not base64_value.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Campo 'base64' e obrigatorio.",
            )

        return base64_value
