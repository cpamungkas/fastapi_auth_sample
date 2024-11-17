from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from datetime import timedelta
from app.auth import authenticate_user, create_access_token, get_current_active_user, fake_users_db
from app.models import Token, User
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://yourdomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mock fake product database table
fake_product_db = {
    "1": {"name": "Product 1", "description": "A great product"},
    "2": {"name": "Product 2", "description": "Another fantastic product"},
    "3": {"name": "Product 3", "description": "Another fantastic product"},
    "4": {"name": "Product 4", "description": "Another fantastic product"},
    "5": {"name": "Product 5", "description": "Another fantastic product"},
    "6": {"name": "Product 6", "description": "Another fantastic product"},
    # Add more products here
    #...
}


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


# get data from fake_product_db with auth token
@app.get("/products")
async def get_products(current_user: User = Depends(get_current_active_user)):
    # fetch data from your real database using the access token
    # here we are just returning a sample list of products
 return fake_product_db



# get 1 data from fake_product_db with auth token
@app.get("/products/{product_id}")
async def read_product(product_id: int, current_user: User = Depends(get_current_active_user)):
    # fetch data from your real database using the access token
    # here we are just returning a sample product
    if product_id not in fake_product_db:
        raise HTTPException(status_code=404, detail="Product not found")
    return fake_product_db[product_id]



