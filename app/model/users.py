from app.db.db_helper import get_connection


class User:
    def __init__(self, id, username, email, is_active):
        self.id = id
        self.username = username
        self.email = email
        self.is_active = is_active

    def __str__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.is_active})"


def create_table():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                     id SERIAL PRIMARY KEY,
                     username VARCHAR(50) NOT NULL UNIQUE,
                     email VARCHAR(100) NOT NULL UNIQUE,
                     is_active BOOLEAN
                    )
                    """)
            conn.commit()


def create_user_db(username, email, is_active) -> User:
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO public.users (username, email, is_active) VALUES (%s, %s, %s)",
                    (username, email, is_active))
                conn.commit()
                user = get_user_by_email(email)
                return User(id=user.id, username=username, email=email, is_active=is_active)
    except Exception as e:
        print(f"An error occurred while creating user: {e}")
        return None


def get_all_users() -> list[User]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM public.users")
            return [User(id, username, email, is_active) for id, username, email, is_active in cur.fetchall()]


def get_user_by_email(email) -> User:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, email, is_active FROM public.users WHERE email = %s", (email,))
            row = cur.fetchone()
            if row:
                return User(*row)
            else:
                return None


def delete_all_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.users")
            conn.commit()


def delete_user_by_email(email):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM public.users where email = %s", (email,))
            conn.commit()
