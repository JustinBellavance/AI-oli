from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from google.oauth2 import service_account
from google.cloud import aiplatform
from PIL import Image
import pandas as pd
import base64
import io
import os

from google import genai
import csv
import pandas as pd
from io import StringIO

client = genai.Client()

def send_photo(image: Image.Image) -> pd.DataFrame:
    # print(f"{image=}")
    result = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            image,
            "\n\n",
            """
            Based on the given image, estimate "calories (kcal)", "protein (g)", "carbohydrates (g)" and "fat (g)" of each individual element in a csv format. 
            
            Only output the csv.
            
            The rows should be each independent elements of food in the picture. 
                        
            Get the most accurate measurement, and try to analyse the food to scale with items around it, when applicable. 
                        
            If it's not food, only send 'not food' instead of the csv.
            """,
        ],
    )
    # print(result.text)

    # Check if the result is "not food"
    if result.text.lower() == "not food":
        return pd.DataFrame()
    
    csv_data = result.text.replace('```csv', '').replace('```', '').strip()

    # print(csv_data)

    # Parse the CSV string
    df = pd.read_csv(StringIO(csv_data))
    
    chat = send_chat(df)

    return {"df" : df, "chat" : chat}

def send_chat(df : pd.DataFrame) -> str:
    
    result = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            """
            Using the contents of this dataframe which describes a meal the user just ate,
            very very briefly describe the food and give advice or recommendations, if needed.
            
            Keep it very brief.
            
            If dataframe is empty. Send 'This was not recognized as food!'
            """,
            "\n\n",
            df.to_string()
        ],
    )
    
    print(result.text)
        
    return result.text
