from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from passlib.context import CryptContext
import jwt
import datetime

SECRET_KEY = "supersecretkey"

# Настройка хеширования пароля
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Подключение к MongoDB
client = AsyncIOMotorClient("mongodb://localhost:27017")
db = client["eventfull"]
users_collection = db["users"]

# Создание маршрутизатора
router = APIRouter()

class UserRegister(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)

def create_jwt_token(data: dict) -> str:
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    data.update({"exp": expire})
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")

@router.post("/register")
async def register(user: UserRegister):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    hashed_password = hash_password(user.password)
    new_user = {"username": user.username, "password": hashed_password}
    await users_collection.insert_one(new_user)
    return {"message": "Пользователь зарегистрирован"}

@router.post("/login")
async def login(user: UserLogin):
    existing_user = await users_collection.find_one({"username": user.username})
    if not existing_user or not verify_password(user.password, existing_user["password"]):
        raise HTTPException(status_code=400, detail="Неверные данные")

    token = create_jwt_token({"sub": user.username})
    return {"token": token}
