from fastapi import HTTPException
from typing import Any, Optional


class BaseAPIException(HTTPException):
    def __init__(
        self, status_code: int, detail: str, headers: Optional[dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class UnauthorizedException(BaseAPIException):
    def __init__(self):
        super().__init__(status_code=402, detail="Usuário não autenticado.")


class TokenException(BaseAPIException):
    def __init__(self, resource):
        super().__init__(status_code=401, detail=f"Token {resource}.")


class SessionException(BaseAPIException):
    def __init__(self, resource):
        super().__init__(status_code=401, detail=f"Token {resource}.")


class PermissionDeniedException(BaseAPIException):
    def __init__(self):
        super().__init__(
            status_code=403, detail="Sem permissão para acessar este recurso."
        )


class NotFoundException(BaseAPIException):
    def __init__(self, resource: str):
        super().__init__(status_code=404, detail=f"{resource} não encontrado.")


class ValidationException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail=detail)


class ConflictException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(status_code=409, detail=detail)


class BusinessException(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)
