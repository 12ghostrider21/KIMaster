
import random
from io import BytesIO

import pygame
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import StreamingResponse

app = FastAPI()



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
