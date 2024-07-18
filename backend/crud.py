from sqlmodel import Session, select

from models import User, UserCreate
from security import get_password_hash, verify_password


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()

    return session_user


def create_user(*, session: Session, user_create: UserCreate):
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)

    return db_obj


def update_password(*, session: Session, user: User, new_password: str):
    hashed_password = get_password_hash(new_password)
    user.hashed_password = hashed_password

    session.add(user)
    session.commit()


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    
    if not db_user:
        return None
    
    if not verify_password(password, db_user.hashed_password):
        return None
    
    return db_user
