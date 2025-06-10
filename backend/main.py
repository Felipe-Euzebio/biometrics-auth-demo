from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# FastAPI application instance
app = FastAPI(
    root_path="/api",  # Set the root path for the API
)

# CORS configuration to allow requests from a specific origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Define a simple route for testing
@app.get("/hello")
async def hello():
    return {"message": "Hello, World!"}

if __name__ == "__main__":
    # Run the FastAPI application using uvicorn
    uvicorn.run(app, host="localhost", port=8000)
    