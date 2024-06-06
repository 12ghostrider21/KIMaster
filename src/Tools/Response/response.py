from dataclasses import dataclass
from .r_code import R_CODE


@dataclass
class Response:
    code: R_CODE
    data: dict | None

    def __init__(self, code: R_CODE, data: dict | None = None):
        self.code: R_CODE = code
        self.data: dict | None = data
