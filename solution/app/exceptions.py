from fastapi import HTTPException, status


class BaseServiceException(HTTPException):
    status_code = 500
    detail = ""

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


class PromoCreationException(BaseServiceException):
    detail = "Failed create promo"


class PromoGetException(BaseServiceException):
    detail = "Failed get promo"


class PromoNotFoundException(BaseServiceException):
    detail = "Promo not found"


class PromoNotBelongBusinessException(BaseServiceException):
    detail = "Promo does not belong business"


class BusinessNotAuthException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Business not authorized")
