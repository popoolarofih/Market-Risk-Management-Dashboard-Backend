from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from jose import JWTError, jwt
from datetime import datetime, timedelta
from supabase import create_client, Client
from dotenv import load_dotenv
import os
from passlib.context import CryptContext

# Load environment variables from .env file
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Load secrets from environment
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Supabase setup using env variables
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int = None
    username: str
    email: EmailStr
    created_at: datetime = None

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    response = supabase.table("users").select("*").eq("username", username).execute()
    users = response.data
    if not users:
        return False
    user = users[0]
    if not verify_password(password, user.get("password")):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    # Check if username or email exists
    username_exists = supabase.table("users").select("id").eq("username", user.username).execute().data
    email_exists = supabase.table("users").select("id").eq("email", user.email).execute().data
    if username_exists or email_exists:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = get_password_hash(user.password)
    result = supabase.table("users").insert({
        "username": user.username,
        "email": user.email,
        "password": hashed_password
    }).execute()
    user_data = result.data[0]
    return User(id=user_data["id"], username=user_data["username"], email=user_data["email"], created_at=user_data["created_at"])

@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"], "user_id": user["id"]})
    return {"access_token": access_token, "token_type": "bearer"}
