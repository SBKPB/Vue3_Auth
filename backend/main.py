from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import col, delete, func, select

from crud import authenticate, create_user, get_user_by_email, update_password
from db import SessionDep, create_db_and_tables
from models import Email, User, UserCreate, UserLoginForm, UserPublic, UsersPublic
from security import generate_otp
from send_mail import send_email

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/users/", response_model=UserPublic)
def add_user(session: SessionDep, user_in: UserCreate, response_model=UserPublic):

    user = get_user_by_email(session=session, email=user_in.email)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = create_user(session=session, user_create=user_in)

    return user


@app.get("/users/", response_model=UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    count_statement = select(func.count()).select_from(User)
    count = session.exec(count_statement).one()

    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()

    return UsersPublic(data=users, count=count)


@app.post("/check-mail")
def check_mail(session: SessionDep, email_in: Email) -> Any:
    user = get_user_by_email(session=session, email=email_in.email)

    print(f"email_in: {email_in}")

    if not user:
        otp_code = generate_otp()

        user_create = UserCreate(
            email=email_in.email,
            name=email_in.email,
            password=otp_code,
            identity="外部使用者",
        )
        create_user(session=session, user_create=user_create)
        send_email(email_in.email, otp_code)

        raise HTTPException(404, "Email does not exist")

    if user.identity == "外部使用者":
        otp_code = generate_otp()

        send_email(email_in.email, otp_code)

        update_password(session=session, user=user, new_password=otp_code)

    return {"status_code": 200, "detail": "Email exists"}


@app.post("/login")
def login(session: SessionDep, login_Form: UserLoginForm):
    user = authenticate(
        session=session, email=login_Form.email, password=login_Form.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    
    return {"status_code": 200, "detail": "Login Success"}


@app.get("/tables/test")
def read_table_by_id(id: int):
    return {"table_id": id}
