from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
import os
from dotenv import load_dotenv
import re


load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=OPENAI_API_KEY)
def chatgpt_message(prompt):
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "assistant", "content": "You are a travel vacation itinerary assistant, if the prompt has nothing to do with travel, please ask the user to resubmit"},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return chat_completion.choices[0].message.content.strip()


# example_gpt = chatgpt_message("miami")
# print(example_gpt)


app = FastAPI()

# Define the allowed origins
origins = ["*"]
    # "http://localhost:63342",
    # "https://voyage-arrr.vercel.app",  # Update this to your frontend URL


# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,  # Allow credentials (cookies, authorization headers, etc.)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

class TextData(BaseModel):
    text: str


# @app.get("/")
# async def get_data():
#     data = {'name': example_gpt,
#             'year': 2024}
#     return data
#
# @app.get("/info")
# async def get_info():
#     data = {'event': 'KNIGHT HACKS'}
#     return data


# @app.post("/submit_city")
# async def submit_city(data: TextData):
#     print(f"received data/city: {data.text}")
#     final_data = chatgpt_message(f"Quick paragraph overview of vacation things to do at {data.text}")
#     print(final_data)
#     return final_data


# Define the structure of the expected data, including the start and end dates
class TravelFormData(BaseModel):
    city: str
    startDate: str
    endDate: str
    budget: str
    nonNegotiables: str
    travelStyle: str
    pace: str
    numTravelers: str

# Create a POST endpoint to handle form submissions
@app.post("/submit")
async def submit_form(data: TravelFormData):
    # Process the data here, including the date range
    print(f"Received data: {data}")

    # Prepare the prompt for OpenAI
    prompt = (
        f"Create a detailed travel itinerary for a trip to {data.city} "
        f"from {data.startDate} to {data.endDate} with a budget of ${data.budget}. "
        f"Include must-visit places related to {data.nonNegotiables}. This does not mean base the entire itinerary around this, but you must include these activities at least once."
        "The pace of the itinerary must be {data.pace} paced."
        f"The theme or style of itinerary should be {data.travelStyle}."
        f"Please also consider this itinerary is for a group of {data.numTravelers} travelers."
    )
    
    itinerary = chatgpt_message(prompt)

    def remove_markdown_symbols(text):
        # Remove '#' symbols
        text = re.sub(r'#', '', text)
        # Remove '*' symbols
        text = re.sub(r'\*', '', text)
        # Remove '**' symbols
        text = re.sub(r'\*\*', '', text)
        return text

    # Remove markdown symbols from the itinerary
    itinerary = remove_markdown_symbols(itinerary)


    print(itinerary)
    
    # Return the itinerary to the frontend
    return {"itinerary": itinerary}
