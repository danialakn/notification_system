from fastapi import FastAPI
from routers import notif_route, health
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(notif_route.router, tags=["notif_route"])
app.include_router(health.router, tags=["health"])

origins = [
    # Add the address of your frontend here. Common examples for development:
    "http://localhost:8000",  # If your frontend is served by Django
    "http://127.0.0.1:5500",  # Example for VS Code's "Live Server"
                   # If you open the index.html file directly in the browser
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      # The list of origins that are allowed to make requests
    allow_credentials=True,   # Allows cookies to be included
    allow_methods=["*"],      # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],      # Allows all headers
)