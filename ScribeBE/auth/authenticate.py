from auth.JWT_token import verify_access_token
from fastapi import Depends, HTTPException, status  # type: ignore
from fastapi.security import OAuth2PasswordBearer  # type: ignore

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")


async def authenticate(token: str = Depends(oauth2_scheme)) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sign in for access"
        )

    decoded_token = verify_access_token(token)
    return decoded_token
