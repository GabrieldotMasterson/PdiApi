from pydantic import BaseModel


class DefaultResponse(BaseModel):
    msg: str

class ErrorResponse(BaseModel):
    error: str