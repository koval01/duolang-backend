from fastapi import APIRouter, Response

router = APIRouter()


@router.get(
    "/healthz",
    summary="Health status",
    responses={200: {"content": None}},
    tags=["Service"]
)
async def healthz() -> Response:
    return Response(None)
