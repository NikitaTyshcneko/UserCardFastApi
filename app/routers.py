from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from app.cruds import UserCruds, CardsCruds, UserCardCrud, pwd_context
from app.database import db
from app.schemas import UserSchema, CardSchema, UserCardSchema, UserWithPasswordSchema
from fastapi import HTTPException

from app.utils import create_access_token, get_username_from_token, refresh_access_token, token_auth_scheme

router = APIRouter()


@router.post("/refresh-token/", tags=["Login"])
async def refresh_token(token: str = Depends(token_auth_scheme)):
    response = JSONResponse(status_code=200, content={
        "access_token": refresh_access_token(token=token)
    })
    return response


@router.post("/user/login/", tags=["Login"])
async def user_login(user: UserWithPasswordSchema):
    user_db = await UserCruds(db=db).get_user_by_username(user.username)
    if pwd_context.verify(user.password, user_db.password):
        return{'access_token':create_access_token(user_db.username)}
    raise HTTPException(status_code=404, detail="User with this id does not exist")


@router.get("/user/get/", tags=["User"])
async def get_by_id_card(id: int):
    return await UserCruds(db=db).get_user_by_id(id)


@router.get("/user/getall/", tags=["User"])
async def get_all_user():
    return await UserCruds(db=db).get_user_all()


@router.post("/user/register/", tags=["User"])
async def add_user(new_user: UserWithPasswordSchema):
    await UserCruds(db=db).create_user(new_user)
    return {
        "result": "user added successfully"
    }


@router.put("/user/update/", tags=["User"])
async def update_user(new_user: UserWithPasswordSchema, username_from_jwt: str = Depends(get_username_from_token)):
    await UserCruds(db=db).update_user(new_user, username_from_jwt)
    return {
        "result": "user update successfully"
    }


@router.delete("/user/delete/", tags=["User"])
async def delete_user(username_from_jwt: str = Depends(get_username_from_token)):
    await UserCruds(db=db).delete_user(username_from_jwt)
    return {
        "result": "user delete successfully"
    }


@router.get("/card/get/", tags=["Card"])
async def get_by_id_card(id: int):
    return await CardsCruds(db=db).get_card_by_id(id)


@router.get("/card/getall/", tags=["Card"])
async def get_all_card():
    return await CardsCruds(db=db).get_card_all()


@router.post("/card/add/", tags=["Card"])
async def add_card(new_card: CardSchema):
    await CardsCruds(db=db).create_card(new_card)
    return {
        "result": "card added successfully"
    }


@router.put("/card/update/", tags=["Card"])
async def update_card(new_card: CardSchema, id: int):
    await CardsCruds(db=db).update_card(new_card, id)
    return {
        "result": "card update successfully"
    }


@router.delete("/card/delete/", tags=["Card"])
async def delete_card(id: int):
    await CardsCruds(db=db).delete_card(id)
    return {
        "result": "card delete successfully"
    }


@router.post("/user-card/add/", tags=["User-card"])
async def user_add_card(card_name: str, username_from_jwt: str = Depends(get_username_from_token)):
    await UserCardCrud(db=db).add_card_to_user(card_name, username_from_jwt)
    return {
        "result": "card added to user"
    }


@router.get("/user-card/all/", tags=["User-card"])
async def user_all_card(username: str):
    return await UserCardCrud(db=db).get_user_card(username)
