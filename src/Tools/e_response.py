from dataclasses import dataclass
from enum import Enum


class EResponse(Enum):
    SUCCESS = 200
    ERROR = 400

@dataclass
class Response:
    response_code: EResponse
    response_msg: str
    data: dict | None

    def __init__(self, response_code: EResponse, response_msg: str, data: dict | None = None):
        self.response_code: EResponse = response_code
        self.response_msg: str = response_msg
        self.data: dict | None = data