from app.model.users import create_user_db, get_user_by_email, delete_user_by_email
from app.service.cache_service import UserCache


def create_user(username, email, is_active):
    user = create_user_db(username, email, is_active)
    user_cache = UserCache()
    user_cache.push_data(user.email, user.__dict__)
    return user


def get_cached_user_by_email(email):
    user_cache = UserCache()
    user = user_cache.retrieve_data(email)
    if user is None:
        return get_user_by_email(email)
    else:
        return user


def delete_user_from_cache_and_database(email):
    user_cache = UserCache()
    delete_user_by_email(email)
    user_cache.delete_data(email)


class UserService:

    def __init__(self):
        pass  # Empty method

