from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import datetime
import jwt
from fastapi.encoders import jsonable_encoder
from passlib.context import CryptContext

# --- Инициализация FastAPI ---
app = FastAPI()

# --- Разрешение CORS (для фронта) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники (можно указать frontend)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Подключение к MongoDB ---
MONGO_URL = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URL)
db = client.eventful_db
users_collection = db.users
events_collection = db.events

# --- Настройки безопасности ---
SECRET_KEY = "secret"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --- Модели данных ---
class UserCreate(BaseModel):
    username: str
    password: str

class Event(BaseModel):
    title: str
    description: str
    date: datetime.datetime
    location: str

# --- Функция для преобразования ObjectId ---
def fix_mongo_id(data):
    if isinstance(data, list):
        return [fix_mongo_id(item) for item in data]
    if isinstance(data, dict):
        return {key: fix_mongo_id(value) for key, value in data.items()}
    if isinstance(data, ObjectId):  
        return str(data)
    return data

# --- Функция проверки токена ---
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Недействительный токен")
        user = await users_collection.find_one({"username": username})
        if user is None:
            raise HTTPException(status_code=401, detail="Пользователь не найден")
        return user
    except:
        raise HTTPException(status_code=401, detail="Ошибка в токене")

# --- Регистрация пользователя ---
@app.post("/register")
async def register_user(user: UserCreate):
    existing_user = await users_collection.find_one({"username": user.username})
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")
    
    hashed_password = pwd_context.hash(user.password)
    new_user = {"username": user.username, "password": hashed_password}
    await users_collection.insert_one(new_user)

    return {"message": "Регистрация успешна"}

# --- Авторизация (логин) ---
@app.post("/login")
async def login(user: UserCreate):
    db_user = await users_collection.find_one({"username": user.username})
    if not db_user or not pwd_context.verify(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Неверный логин или пароль")

    token_payload = {
        "sub": db_user["username"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
    
    return {"access_token": token}

# --- Защищенный маршрут (профиль) ---
@app.get("/protected")
async def protected_route(user: dict = Depends(get_current_user)):
    return {"username": user["username"]}

# --- Создание события ---
@app.post("/events")
async def create_event(event: Event, user: dict = Depends(get_current_user)):
    event_data = event.dict()
    event_data["created_by"] = user["username"]
    new_event = await events_collection.insert_one(event_data)
    return {"message": "Событие создано", "event_id": str(new_event.inserted_id)}

# --- Получение списка событий (фикс ObjectId) ---
@app.get("/events")
async def get_events():
    events = await events_collection.find().to_list(100)
    return jsonable_encoder(fix_mongo_id(events))

# --- Обновление события ---
@app.put("/events/{event_id}")
async def update_event(event_id: str, updated_event: Event):
    event_data = updated_event.dict()
    result = await events_collection.update_one({"_id": ObjectId(event_id)}, {"$set": event_data})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    return {"message": "Событие обновлено"}

# --- Удаление события ---
@app.delete("/events/{event_id}")
async def delete_event(event_id: str):
    result = await events_collection.delete_one({"_id": ObjectId(event_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Событие не найдено")
    return {"message": "Событие удалено"}
