from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Define the allowed origins
origins = [
    "http://localhost:63342",  # Update this to your frontend URL
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
    data = {'name': 'John',
            'age': 30}
    return data

@app.get("/info")
async def get_info():
    data = {'event': 'KNIGHT HACKS'}
    return data

