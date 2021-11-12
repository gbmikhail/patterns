from pydantic import BaseModel


class Request(BaseModel):
    method: str
    base: str
    url: str
    headers: dict
