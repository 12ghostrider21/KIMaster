import random
from io import BytesIO
from typing import List

import numpy as np
import pygame
import uvicorn
from PIL import Image
from fastapi import FastAPI, Header, HTTPException, Depends, UploadFile, File
from fastapi.responses import StreamingResponse
from starlette.responses import JSONResponse

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

@app.post("/play")
async def receive_array(array: List[List[int]]):
    np_array = np.array(array)
    print(np_array)
    return 0

@app.post("/png")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read the image file into memory
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        # Process the image (e.g., save to disk, perform operations)
        # For demonstration, let's just print image details
        image_info = {
            "filename": file.filename,
            "content_type": file.content_type,
            "image_format": image.format,
            "image_size": image.size
        }
        print("Image Uploaded:", image_info)

        return JSONResponse(status_code=200,
                            content={"message": "Image uploaded successfully", "image_info": image_info})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})

# *******************************************************************************************************************

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
    uvicorn.run(app, host="127.0.0.1", port=8001)
