from prisma import Prisma
from app.schemas import UserCreate
from app.auth import get_password_hash

prisma = Prisma()
# prisma.connect()

async def create_user(user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_data = {"username": user.username, "email": user.email, "password": hashed_password}
    return await prisma.user.create(data=user_data)

async def get_user_by_email(email: str):
    return await prisma.user.find_unique(where={"email": email})

async def get_user(user_id: int):
    return await prisma.user.find_unique(where={"id": user_id})
