from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.api.routers import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='hatakon'
)

app.include_router(router, tags=["Main"])

origins = [
    "http://localhost",
    "http://localhost:8000",
]

# Добавление middleware для CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <a href="http://127.0.0.1:8000/docs"><h1>Documentation</h1></a><br>
    <a href="http://127.0.0.1:8000/redoc"><h1>ReDoc</h1></a>
    """