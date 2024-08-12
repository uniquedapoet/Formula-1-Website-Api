import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import circuits, drivers
from app.data_loader import load_circuits_data, load_drivers_data
from contextlib import asynccontextmanager
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust this to match your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(circuits.router)
app.include_router(drivers.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Formula 1 API!"}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    load_circuits_data()
    load_drivers_data()
    print("Data loaded!")
    yield
    # No shutdown code needed in this case

app.router.lifespan_context = lifespan

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)