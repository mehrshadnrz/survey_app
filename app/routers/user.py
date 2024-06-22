from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app import schemas, crud, auth


router = APIRouter()

@router.post("/register", response_model=schemas.UserCreate)
async def register(user: schemas.UserCreate):
    return await crud.create_user(user)

@router.post("/token", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.get_user_by_email(form_data.username)
    if not user or not auth.verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserCreate)
async def read_users_me(current_user: schemas.UserCreate = Depends(auth.get_current_user)):
    return current_user
