from dataclasses import dataclass
from Tools.rcode import RCODE


@dataclass
class Response:
    code: RCODE
    data: dict | None

    def __init__(self, code: RCODE, data: dict | None = None):
        self.code: RCODE = code
        self.data: dict | None = data
