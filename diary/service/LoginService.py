from fastapi import HTTPException
import TokenProvicer
import httpx


class LoginService:

    def __init__(
        self,
        token_provider: TokenProvicer,
        http_client: httpx.AsyncClient,
        client_id,
        client_secret,
        redirect_uri,
    ):
        self.token_provider = token_provider
        self.http_client = http_client
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

    async def login_kakao_oauth(self, code: str):
        try:
            token_url = "https://kauth.kakao.com/oauth/token"
            data = {
                "grant_type": "authorization_code",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "code": code,
                "redirect_uri": self.redirect_uri,
            }

            response = await self.http_client.post(token_url, data=data)
            token_data = response.json()

            if response.status_code != 200:
                raise HTTPException(
                    status_code=400, detail="액세스 토큰 가져오기를 실패했습니다."
                )

            user_info_url = "https://kapi.kakao.com/v2/user/me"
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}

            user_response = await self.http_client.get(user_info_url, headers=headers)
            user_info = user_response.json()

            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Failed to get user info")

            jwt_token = self.token_provider.create_jwt_token(user_info)

            return {"token": jwt_token, "user_info": user_info}

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    async def parse_access_token(self, auth_header):
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="No valid token provided")

        token = auth_header.split(" ")[1]
        payload = await self.token_provider.verify_token(token)

        return {"message": "Protected route accessed", "user": payload}
