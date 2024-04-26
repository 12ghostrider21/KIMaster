import random
from io import BytesIO

import pygame
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.responses import StreamingResponse

app = FastAPI()

lobby_key = "ABC"


# Define a custom dependency to check the header key
def verify_api_key(api_key: str = Header(...)):
    # Check if the provided API key matches the required key
    if api_key != lobby_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


@app.get("/")
async def test():
    return "Hallo World!"


# Example endpoint that requires the custom dependency
@app.get("/protected_data")
def get_protected_data(api_key: str = Depends(verify_api_key)):
    return {"data": "This is protected data and requires a valid API key"}

@app.get("/get_image")
async def get_image():
    from TicTacToeGame import TicTacToeGame
    g = TicTacToeGame()
    b = g.getInitBoard()
    b[random.randint(0, 2)][random.randint(0, 2)] = random.randint(-1, 1)
    surface = g.draw(b)

    image_buffer = BytesIO()
    pygame.image.save(surface, image_buffer, "PNG")
    image_buffer.seek(0)  # Reset the buffer position to the start

    # Return the image as a response
    return StreamingResponse(image_buffer, media_type="image/png")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
