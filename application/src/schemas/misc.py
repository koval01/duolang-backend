from pydantic import BaseModel


class ResultBody(BaseModel):
    success: bool
