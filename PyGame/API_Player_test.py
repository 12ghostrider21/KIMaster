from io import BytesIO
from typing import List

import numpy as np
import uvicorn
from PIL import Image
from fastapi import FastAPI, Header, HTTPException, Depends, UploadFile, File
from starlette.responses import JSONResponse

app = FastAPI()

@app.post("/png")
async def upload_image(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith(('.png')):
            return JSONResponse(status_code=400, content={"message": "Only PNG files are allowed"})
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

        image.save("output.png", format="PNG")

        return JSONResponse(status_code=200,
                            content={"message": "Image uploaded successfully", "image_info": image_info})

    except Exception as e:
        return JSONResponse(status_code=500, content={"message": "Internal Server Error", "error": str(e)})


@app.post("/play")
async def receive_array(array: List[List[int]]):
    np_array = np.array(array)
    print(np_array)
    return 0

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
