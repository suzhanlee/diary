from datetime import datetime, timedelta
from fastapi import HTTPException

import jwt


class TokenProvider:

    def __init__(self, jwt_secret, jwt_algorithm):
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm

    def create_jwt_token(self, user_info: dict) -> str:
        expires = datetime.now() + timedelta(days=1)

        jwt_data = {
            "sub": str(user_info["id"]),
            "nickname": user_info.get("properties", {}).get("nickname", ""),
            "exp": expires,
        }

        return jwt.encode(
            jwt_data, self.jwt_secret, algorithm=self.jwt_algorithm
        )

    async def verify_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(
                token, self.jwt_secret, algorithms=[self.jwt_algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="토큰이 만료됨")
        except jwt.JWTError:
            raise HTTPException(status_code=401, detail="유효한 토큰이 아니다.")
