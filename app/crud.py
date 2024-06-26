from prisma import Prisma
from app.schemas import UserCreate
from app.auth import get_password_hash

prisma = Prisma()

async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = {"username": user.username, "email": user.email, "password": hashed_password}
    return await prisma.user.create(data=user_data)

async def get_user_by_email(email: str):
    return await prisma.user.find_unique(where={"email": email})

async def get_user_by_username(username: str):
    return await prisma.user.find_unique(where={"username": username})

async def get_user(user_id: int):
    return await prisma.user.find_unique(where={"id": user_id})

async def get_user_by_email_or_username(identifier: str):
    user = await get_user_by_email(identifier)
    if not user:
        user = await get_user_by_username(identifier)
    return user