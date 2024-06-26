import os

from fastapi import FastAPI, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.crud.utils import select_chat_messages
from src.utils import lifespan, client

app = FastAPI(
    lifespan=lifespan,
    title="Business App",
    description="Telegram client wrapper"
)
accepted_ips = set(os.getenv('IPS').split(','))
# TODO implement web sockets


def validate_client(_client: str):
    """
    check if device ip is from a proper vlan
    returns true if client in proper vlan
    """
    _client_sub = ".".join(_client.split(".")[:3])
    return f"{_client_sub}." in accepted_ips


@app.post("/message/contact")
async def send_message_contact(
        request: Request, text: str, to: int
):
    _client = request.client.host

    if not validate_client(_client):
        raise HTTPException(
            status_code=403,
            detail="Forbidden to users"
        )

    to = f"+960{to}"
    if len(to) != 11:
        raise HTTPException(
            status_code=422,
            detail="To must have exactly 7 digits"
        )

    await client.send_message(to, text)
    return {"details": "success"}


@app.get("/my/chats")
async def get_chats(request: Request) -> JSONResponse:
    _client = request.client.host

    # if not validate_client(_client):
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Forbidden to users"
    #     )

    chats = await client.get_chats()

    return JSONResponse(
        content=chats
    )


@app.get("/channel/medias")
async def download_channel_medias(
        channel: int, limit: int, request: Request
) -> JSONResponse:
    _client = request.client.host

    # if not validate_client(_client):
    #     raise HTTPException(
    #         status_code=403,
    #         detail="Forbidden to users"
    #     )

    await client.download(channel, limit=limit)
    return JSONResponse(content={"details": "ok"})


@app.get("/messages/chat")
async def get_chat_messages(
        user: int, limit: int, request: Request
) -> JSONResponse:
    _client = request.client.host

    if not validate_client(_client):
        raise HTTPException(
            status_code=403,
            detail="Forbidden to users"
        )

    l = await select_chat_messages(user, limit=limit)

    print(l)
