from fastapi import APIRouter
from src.user.schemas import UserInput

router = APIRouter()


@router.get("/me", response_model=UserInput)
async def get_me():
    pass
    # return user


@router.get("/me", response_model=UserInput)
async def get_user(user_id):
    pass
    # return user


@router.delete("/me")
async def delete_me():
    pass


@router.patch("/me")
async def patch_me(user: UserInput):
    return user


@router.patch("/user_id")
async def patch_user(user: UserInput):
    return user


@router.get("/all")
async def get_uses():
    pass
