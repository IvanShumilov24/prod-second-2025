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


class BusinessNotAuthException(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Business not authorized")


class BusinessExistsException(BaseServiceException):
    detail = "Business already exists"


class PromoCreationException(BaseServiceException):
    detail = "Failed create promo"


class PromoGetException(BaseServiceException):
    detail = "Failed get promo"


class PromoUpdateException(BaseServiceException):
    detail = "Failed update promo"


class PromoNotFoundException(BaseServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Promo not found"


class PromoNotBelongBusinessException(BaseServiceException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Promo does not belong business"


class UserExistsException(BaseServiceException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already exists"


class UserGetException(BaseServiceException):
    detail = "Failed get user"


class UserNotFoundException(BaseServiceException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Promo not found"


class UserUpdateException(BaseServiceException):
    detail = "Failed update user"
