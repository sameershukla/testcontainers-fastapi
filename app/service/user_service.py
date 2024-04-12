from app.model.users import create_user_db, get_user_by_email
from app.service.cache_service import UserCache


def create_user(username, email, is_active):
    user = create_user_db(username, email, is_active)
    user_cache = UserCache()
    user_cache.push_data(user.email, user)


def get_cached_user_by_email(email):
    user_cache = UserCache()
    user = user_cache.retrieve_data(email)
    if user is None:
        return get_user_by_email(email)
    else:
        return user

class UserService:
    pass
