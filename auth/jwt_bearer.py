from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_hander import decodeJWT

class jwtBearer(HTTPBearer):
    def __int__(self, auto_error: bool = True):
        super(jwtBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request : Request):
        credential : HTTPAuthorizationCredentials = await super(jwtBearer, self).__call__(request)
        if credential:
            if not credential.scheme =="Bearer":
                raise HTTPException(status_code=403, detail="Invalid or Expired Token!")
            return credential.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or Expired Token!")

    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool= False
        payload = decodeJWT(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid
