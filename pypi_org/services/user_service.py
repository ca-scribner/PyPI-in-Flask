from typing import Optional

from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from pypi_org.infrastructure.num_convert import try_int
from pypi_org.data.db_session import create_session
from pypi_org.data.users import User

from sqlalchemy import exc


def get_user_count() -> int:
    session = create_session()
    return session.query(User).count()


def find_user_by_email(email) -> Optional[User]:
    if not email:
        return None
    email = email.strip().lower()
    s = create_session()
    user = s.query(User).filter(User.email == email).all()
    s.close()
    if len(user) > 1:
        raise ValueError(f"Found {len(user)} users - expected to find 0 or 1")
    elif len(user) == 0:
        return None
    else:
        return user[0]


def find_user_by_id(user_id) -> Optional[User]:
    user_id = try_int(user_id)
    if not user_id:
        return None
    s = create_session()
    user = s.query(User).filter(User.id == user_id).all()
    s.close()
    if len(user) > 1:
        raise ValueError(f"Found {len(user)} users - expected to find 0 or 1")
    elif len(user) == 0:
        return None
    else:
        return user[0]


def create_user(name: str, email: str, password: str,
                profile_image_url: str = None) -> Optional[User]:

    if not name or \
       not email or \
       not password:
        return None

    # Could use find_user to avoid committing an existing user, but I'm using the db to handle this.  Which is better?

    user = User()
    user.name = name
    user.email = email
    user.hashed_password = hash_text(password)
    user.profile_image_url = profile_image_url

    s = create_session()
    s.add(user)
    try:
        # Commit data to the DB but keep an unexpired version to pass back to caller
        s.expire_on_commit = False
        s.commit()
    except exc.IntegrityError:
        # Record already exists or cannot be added

        user = None
    s.close()
    return user


def login_user(email: str, password: str) -> Optional[User]:
    user = find_user_by_email(email)
    if not user:
        return

    if not verify_hash(hashed_text=user.hashed_password, plain_text=password):
        return None
    return user


def hash_text(text: str) -> str:
    # rounds set randomish but high
    hashed_text = crypto.encrypt(text, rounds=171204)
    return hashed_text


def verify_hash(hashed_text: str, plain_text: str) -> bool:
    return crypto.verify(plain_text, hashed_text)
