from fastapi import HTTPException, status


class BaseServiceException(HTTPException):
    status_code = 500
    detail = ""
    status = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


class TokenExpiredException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")


class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")


class BusinessExistsException(BaseServiceException):
    detail = "Business already exists"
