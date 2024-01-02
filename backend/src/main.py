import asyncio
import uvicorn
from fastapi import FastAPI, Header, Request, Body
from fastapi.responses import ORJSONResponse
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr

from aiogram import Bot
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from src.core.config import settings
from src.api.api_v1.api import api_router


conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_EMAIL,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_EMAIL,
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.yandex.com",
    MAIL_FROM_NAME="Logs",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)
intern_master_address = settings.RECIEVER_EMAIL
bot = Bot(settings.TELEGRAM_TOKEN)


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Centr Invest TOP BANK API",
    version="0.4.2",
    openapi_url=None,
    default_response_class=ORJSONResponse,
    docs_url=None,
    redoc_url=None,
)
fm = FastMail(conf)


# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)


class FormData(BaseModel):
    fio: str
    email: EmailStr
    date: str
    place: str
    family: str


async def lazy_notify(form: FormData, where: str):
    html = f"""Данные с формы

Должность: {where}
ФИО: {form.fio}
Почта: {form.email}
День рождения: {form.date}
Место рождения: {form.place}
Семейное положение: {form.family}"""

    await bot.send_message(chat_id=settings.TELEGRAM_CHAT_ID, text=html)
    message = MessageSchema(
        subject="Заявки от интернов",
        recipients=[intern_master_address],  # List of recipients, as many as you can pass 
        body=html,
        subtype=MessageType.plain,
    )
    await fm.send_message(message)

    gratz = """Поздравляем, вы настолько крутой специалист, что нам даже проводить тестирование не придется!
Вы приняты!




















с 9 апреля"""

    message = MessageSchema(
        subject="Работа мечты в Centr Invest TOP BANK",
        recipients=[form.email],  # List of recipients, as many as you can pass 
        body=gratz,
        subtype=MessageType.plain,
    )
    try:
        await fm.send_message(message)
    except Exception as e:
        print(type(e), e)
    return True


@app.post("/form/{where}", include_in_schema=False)
async def read_users_list(
    where: str,
    *,
    form: FormData = Body(),
    request: Request,
    user_agent: str | None = Header(default=None),
) -> bool:
    if not (user_agent and request.client):
        return False
    asyncio.create_task(lazy_notify(form, where))
    return True


if __name__ == "__main__":
    uvicorn.run(
        "main:app", host="127.0.0.1",
        log_level='debug' if settings.DEBUG else "critical",
        reload=settings.DEBUG,
    )