from dataclasses import dataclass
from .r_code import R_CODE

@dataclass
class Response:
    response_code: R_CODE
    response_msg: str
    data: dict | None

    def __init__(self, response_code: R_CODE, response_msg: str, data: dict | None = None):
        self.response_code: R_CODE = response_code
        self.response_msg: str = response_msg
        self.data: dict | None = data
