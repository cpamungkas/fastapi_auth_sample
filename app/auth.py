from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, status
from app.models import TokenData, UserInDB, User
from app.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(
    schemes=["bcrypt"],
    bcrypt__default_rounds=12,  # Bisa lo adjust, default-nya 12.
    bcrypt__ident="2b"  # Pakai identifier `2b`, biar aman.
)


# Mock user database
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Johnson",
        "email": "alice@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
    },
    "disabled_user": {
        "username": "disabled_user",
        "full_name": "Disabled User",
        "email": "disabled_user@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": True,
    },
    "expired_user": {
        "username": "expired_user",
        "full_name": "Expired User",
        "email": "expired_user@example.com",
        "hashed_password": pwd_context.hash("secret"),
        "disabled": False,
        # User expired 1 day ago
        "exp": (datetime.utcnow() - timedelta(days=1)).timestamp(),
        # User created 2 days ago
        "iat": (datetime.utcnow() - timedelta(days=2)).timestamp(),
    },
    "kangcp": {
        "username": "kangcp",
        "full_name": "kang cp",
        "email": "kangcp@example.com",
        "hashed_password": pwd_context.hash("rahasiadonk"),
        "disabled": False,
    }

}


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
