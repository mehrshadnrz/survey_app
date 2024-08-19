from typing import List
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
    return {"message": "Register successful", "access_token": access_token, "token_type": "bearer", "role": created_user.role}


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
    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer", "role": user.role}


@router.get("/me", response_model=schemas.UserResponse)
async def get_current_user_profile(current_user: dict = Depends(dependencies.get_current_user)):
    return current_user


@router.put("/me", response_model=schemas.UserResponse)
async def update_user(user: schemas.UserUpdate, current_user: dict = Depends(dependencies.get_current_user)):
    updated_user = await crud.update_user(current_user.id, user)
    return updated_user


@router.post("/admins", response_model=schemas.UserResponse)
async def register_admin(user: schemas.UserCreate, current_user: dict = Depends(dependencies.get_current_super_admin_user)):
    db_user = await crud.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    created_admin = await crud.create_admin(user)
    return created_admin


@router.get("/admins", response_model=List[schemas.UserResponse])
async def list_admins(current_user: dict = Depends(dependencies.get_current_super_admin_user)):
    return await crud.list_admin_users()

@router.get("/", response_model=List[schemas.UserResponse])
async def list_users(current_user: dict = Depends(dependencies.get_current_admin_user)):
    return await crud.list_users()


# TEMP
@router.post("/superadmin", response_model=schemas.TokenResponse)
async def register_super_admin(user: schemas.UserCreate):
    db_user = await crud.get_user_by_email(user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    created_user = await crud.create_superadmin(user)
    access_token = auth.create_access_token(data={"sub": created_user.email})
    return {"message": "Register successful", "access_token": access_token, "token_type": "bearer", "role": created_user.role}