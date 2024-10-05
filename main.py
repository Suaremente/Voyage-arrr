from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI


client = OpenAI(
    api_key="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"
)
def chatgpt_message(prompt):
    chat_completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "assistant", "content": "You are a travel vacation assistant"},
            {
                "role": "user",
                "content": prompt
            }
        ]
    )
    return chat_completion.choices[0].message.content.strip()


example_gpt = chatgpt_message("give me a one sentence overview of paris")
print(example_gpt)


app = FastAPI()

# Define the allowed origins
origins = [
    "http://localhost:63342",
    "https://voyage-arrr.vercel.app",  # Update this to your frontend URL
]

# Add the CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,  # Allow credentials (cookies, authorization headers, etc.)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def get_data():
    data = {'name': example_gpt,
            'age': 20}
    return data

@app.get("/info")
async def get_info():
    data = {'event': 'KNIGHT HACKS'}
    return data

