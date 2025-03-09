from dotenv import load_dotenv
load_dotenv()

import os
import pandas as pd
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import base64
import io
from PIL import Image
from datetime import datetime

from src.gemini import send_photo

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Define the ImageData model
class ImageData(BaseModel):
    image: str


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_image(image_data: ImageData):
    # First, define the filename using the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"data/images/uploaded_image_{timestamp}.png"
    
    with open('data/images/bigmac_patrick.png', 'rb') as image_file:
        img_str = base64.b64encode(image_file.read()).decode('utf-8')
    image_data.image = f"data:image/png;base64,{img_str}"
    
    # Now decode the image from base64
    image_data = image_data.image.split(",")[1]
    image = Image.open(io.BytesIO(base64.b64decode(image_data)))

    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    # Save the image in the data directory
    image.save(filename)
    
    dataframe = send_photo(image)
    
    dataframe['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(dataframe.info())

    csv_path = "data/data.csv"
    if os.path.exists(csv_path):
        dataframe.to_csv(csv_path, mode='a', header=False, index=False)
    else:
        dataframe.to_csv(csv_path, mode='w', header=True, index=False)
        
    print(dataframe.head())

    return {"filename": filename}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, ssl_keyfile="key.pem", ssl_certfile="cert.pem")
