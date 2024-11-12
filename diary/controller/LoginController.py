from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
import httpx
from TokenProvicer import TokenProvider
from config import Settings
import LoginService

router = APIRouter()


def get_token_provider():
    return TokenProvider(Settings.JWT_SECRET, Settings.JWT_ALGORITHM)

def get_login_service(
    token_provider: Annotated[TokenProvider, Depends(get_token_provider)]
) -> LoginService:
    return LoginService(
        token_provider=token_provider,
        http_client=httpx.AsyncClient()
        client_id=Settings.KAKAO_CLIENT_ID,
        client_secret=Settings.KAKAO_CLIENT_SECRET,
        redirect_uri=Settings.REDIRECT_URI,
    )


@router.get("/auth/kakao/login")
def kakao_login():
    auth_url = "https://kauth.kakao.com/oauth/authorize"
    params = {
        "client_id": Settings.KAKAO_CLIENT_ID,
        "redirect_url": Settings.REDIRECT_URI,
        "response_type": "code",
    }

    url = f"{auth_url}?client_id={params['client_id']}&redirect_uri={params['redirect_uri']}&response_type={params['response_type']}"

    return RedirectResponse(url)


@router.get("/auth/kakao/callback")
async def kakao_callback(
    code: str,
    login_service: Annotated[LoginService, Depends(get_login_service)]
):
    return await login_service.kakao_callback(code)


@router.get("/protected")
async def protected_route(
    request: Request, 
    login_service: Annotated[LoginService, Depends(get_login_service)]
):
    auth_header = request.headers.get("Authorization")
    return await login_service.parse_access_token(auth_header)
