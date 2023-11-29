from fastapi import APIRouter
from app.cruds import UserCruds, CardsCruds, UserCardCrud
from app.database import db
from app.schemas import UserSchema, CardSchema, UserCardSchema, UserWithPasswordSchema

router = APIRouter()


@router.post("/user/get/", tags=["User"])
async def get_by_id_card(id: int):
    return await UserCruds(db=db).get_user_by_id(id)


@router.post("/user/getall/", tags=["User"])
async def get_all_card():
    return await UserCruds(db=db).get_user_all()


@router.post("/user/register/", tags=["User"])
async def add_user(new_user: UserWithPasswordSchema):
    await UserCruds(db=db).create_user(new_user)
    return {
        "result": "user added successfully"
    }


@router.post("/user/update/", tags=["User"])
async def update_user(new_user: UserSchema, id: int):
    await UserCruds(db=db).update_user(new_user, id)
    return {
        "result": "user update successfully"
    }


@router.post("/user/delete/", tags=["User"])
async def delete_user(id: int):
    await UserCruds(db=db).delete_user(id)
    return {
        "result": "user delete successfully"
    }


@router.post("/card/get/", tags=["Card"])
async def get_by_id_card(id: int):
    return await CardsCruds(db=db).get_card_by_id(id)


@router.post("/card/getall/", tags=["Card"])
async def get_all_card():
    return await CardsCruds(db=db).get_card_all()


@router.post("/card/add/", tags=["Card"])
async def add_card(new_card: CardSchema):
    await CardsCruds(db=db).create_card(new_card)
    return {
        "result": "card added successfully"
    }


@router.post("/card/update/", tags=["Card"])
async def update_card(new_card: CardSchema, id: int):
    await CardsCruds(db=db).update_card(new_card, id)
    return {
        "result": "card update successfully"
    }


@router.post("/card/delete/", tags=["Card"])
async def delete_card(id: int):
    await CardsCruds(db=db).delete_card(id)
    return {
        "result": "card delete successfully"
    }


@router.post("/card/delete/", tags=["Card"])
async def delete_card(id: int):
    await CardsCruds(db=db).delete_card(id)
    return {
        "result": "card delete successfully"
    }


@router.post("/user-card/add/", tags=["User-card"])
async def user_add_card(new_user_card: UserCardSchema):
    await UserCardCrud(db=db).add_card_to_user(new_user_card)
    return {
        "result": "card added to user"
    }


@router.post("/user-card/all/", tags=["User-card"])
async def user_all_card(username: str):
    return await UserCardCrud(db=db).get_user_card(username)
