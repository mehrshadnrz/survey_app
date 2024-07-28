from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, crud, auth, dependencies


router = APIRouter()


@router.post("/register", response_model=schemas.TokenResponse)
async def register(user: schemas.UserCreate):
    db_user = await crud.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    created_user = await crud.create_user(user)
    access_token = auth.create_access_token(data={"sub": created_user.email})
    return {"message": "Register successful", "access_token": access_token, "token_type": "bearer", "role": created_user.role.value}


@router.post("/login", response_model=schemas.TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_email_or_username(form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username/email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer", "role": user.role.value}


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_profile(current_user: dict = Depends(dependencies.get_current_user)):
    return current_user
