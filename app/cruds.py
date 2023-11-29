import databases
from app.schemas import UserSchema, CardSchema, UserCardSchema, UserWithPasswordSchema
from app.models import cards, users, user_card
from fastapi import HTTPException
from passlib.context import CryptContext

# This is used to hash passwords
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_user_by_id(self, id: int):
        user = await self.db.fetch_one(users.select().where(users.c.id == id))
        if user==None:
            raise HTTPException(status_code=404, detail="User with this id does not exist")
        return UserSchema(id=user.id, username=user.username, password=user.password)

    async def get_user_all(self):
        user_db = await self.db.fetch_all(users.select())
        if user_db==None:
            return None
        return [UserSchema(id=user.id, username=user.username, password=user.password) for
                user in user_db]

    async def create_user(self, new_user: UserWithPasswordSchema):
        user = await self.db.fetch_one(users.select().where(users.c.username == new_user.username))
        if user!=None:
            raise HTTPException(status_code=404, detail="User with this username already exists")
        hashed_password = pwd_context.hash(new_user.password)
        query = users.insert().values(username=new_user.username, password=hashed_password)
        await self.db.execute(query)
        return "success"

    async def update_user(self, new_user: UserSchema, id: int):
        query = users.update().values(username=new_user.username, password=new_user.password).where(users.c.id == id)
        await self.db.execute(query)
        return "success"

    async def delete_user(self, id: int):
        query = users.delete().where(users.c.id == id)
        await self.db.execute(query)
        return "success"


class CardsCruds:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_card_by_id(self, id: int):
        card = await self.db.fetch_one(cards.select().where(cards.c.id == id))
        if card==None:
            raise HTTPException(status_code=404, detail="Card with this id does not exist")
        return CardSchema(id=card.id, name=card.name, description=card.description, resourceURI=card.resourceURI)

    async def get_card_all(self):
        cards_db = await self.db.fetch_all(cards.select())
        if cards_db==None:
            return None
        return [CardSchema(id=card.id, name=card.name, description=card.description, resourceURI=card.resourceURI) for card in cards_db]

    async def create_card(self, new_card: CardSchema):
        query = cards.insert().values(name=new_card.name, description=new_card.description,
                                     resourceURI=new_card.resourceURI)
        await self.db.execute(query)
        return "success"

    async def update_card(self, new_card: CardSchema, id: int):
        query = cards.update().values(name=new_card.name, description=new_card.description,
                                     resourceURI=new_card.resourceURI).where(cards.c.id == id)
        await self.db.execute(query)
        return "success"

    async def delete_card(self, id: int):
        query = cards.delete().where(cards.c.id == id)
        await self.db.execute(query)
        return "success"


class UserCardCrud:
    def __init__(self, db: databases.Database):
        self.db = db

    async def get_user_card(self, username: str):
        user = await self.db.fetch_one(users.select().where(users.c.username == username))
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        user_card_db = await self.db.fetch_all(user_card.select().where(user_card.c.user_id == user.id))

        if user_card_db is None:
            raise HTTPException(status_code=404, detail="user_card_db not found")

        card_ids = [user_in_db.card_id for user_in_db in user_card_db]

        # Assuming 'cards' is an asynchronous SQLAlchemy table object
        cards_db = await self.db.fetch_all(cards.select().where(cards.c.id.in_(card_ids)))

        return [CardSchema(id=card.id, name=card.name, description=card.description, resourceURI=card.resourceURI) for card in cards_db]

    async def add_card_to_user(self, new_user_card: UserCardSchema):
        user = await self.db.fetch_one(users.select().where(users.c.username == new_user_card.username))
        card = await self.db.fetch_one(cards.select().where(cards.c.name == new_user_card.name))
        if card==None or user==None:
            raise HTTPException(status_code=404, detail="User not found")
        query = user_card.insert().values(user_id=user.id, card_id=card.id)
        await self.db.execute(query)
        return "success"