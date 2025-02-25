from fastapi import HTTPException

class InvalidCurrencyException(HTTPException):
    def __init__(self, detail: str, status_code: int):
        super().__init__(status_code=status_code, detail=detail)
