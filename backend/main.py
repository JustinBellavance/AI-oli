from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import base64
import io
from PIL import Image
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

from src.gemini import send_photo
from src.figures import create_figure

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://172.20.10.9:5173",
    "https://storage.googleapis.com",
    "http://aioli.tech",
    "http://www.aioli.tech",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           # Only allow specified origins
    allow_credentials=True,
    allow_methods=["*"],             # Allow all methods
    allow_headers=["*"],             # Allow all headers
)

templates = Jinja2Templates(directory="templates")

# Define the ImageData model
class ImageData(BaseModel):
    image: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_image(image_data: ImageData):
    try:
        # First, define the filename using the current date and time
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"data/images/uploaded_image_{timestamp}.png"
        
        # Now decode the image from base64
        image_data = image_data.image.split(",")[1]
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        # Convert the image to RGB format
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Ensure the data directory exists
        os.makedirs("data/images", exist_ok=True)

        # Save the image in the data directory
        image.save(filename)

        # Resize image if quality is too high
        width, height = image.size

        # Calculate the new size while maintaining aspect ratio
        max_size = 250
        ratio = min(max_size / width, max_size / height)
        new_size = (int(width * ratio), int(height * ratio))

        # Resize the image
        resized_image = image.resize(new_size, Image.LANCZOS)

        # Process the image with send_photo
        df_and_chat = send_photo(resized_image)

        dataframe = df_and_chat['df']
        chat = df_and_chat['chat']
        
        if dataframe.empty:
            return {"message": "Not food."}
        
        dataframe['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        

        csv_path = "data/data.csv"
        if os.path.exists(csv_path):
            dataframe.to_csv(csv_path, mode='a', header=False, index=False)
        else:
            dataframe.to_csv(csv_path, mode='w', header=True, index=False)
    

        figure = create_figure( pd.read_csv("data/data.csv")) 

        
        return {"figure": figure, "chat" : chat}

    except Exception as e:
        print(f"Error processing image: {e}")
        return {"message": "Error processing image"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
