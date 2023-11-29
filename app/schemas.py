from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class UserSchema(BaseModel):
    username: str | None = None

class UserWithPasswordSchema(BaseModel):
    username: str | None = None
    password: str | None = None


class CardSchema(BaseModel):
    name: str | None = None
    description: str
    resourceURI: str


class UserCardSchema(BaseModel):
    username: str
    name: str
