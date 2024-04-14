from fastapi import APIRouter, HTTPException
from app.model.users import User
from app.service.user_service import get_user_by_email, create_user, delete_user_from_cache_and_database, get_cached_user_by_email

router = APIRouter()


@router.post("/users")
def create_new_user(username, email, is_active):
    user = create_user(username, email, is_active)
    if user is not None:
        return objToDict(user)
    raise HTTPException(status_code=500, detail="Internal Server Error, Unable to Create User")


@router.get("/users/{email}")
def get_user_by_email(email: str):
    user = get_cached_user_by_email(email)
    if user is not None:
        return user
    raise HTTPException(status_code=404, detail="User Not Found")


@router.delete("/users/{email}")
def delete_user(email: str):
    user = get_cached_user_by_email(email)
    if user is not None:
        delete_user_from_cache_and_database(email)


def objToDict(user: User):
    user_dict = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active
    }
    return user_dict
