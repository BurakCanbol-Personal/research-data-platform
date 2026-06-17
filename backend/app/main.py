from fastapi import FastAPI

from app.api.routes_datasets import router as datasets_router
from app.api.routes_health import router as health_router


app = FastAPI(
    title="Research Data Platform API",
    description="API for uploading, processing and viewing research datasets.",
    version="0.1.0",
)

app.include_router(health_router)
app.include_router(datasets_router)

@app.get("/")
def root():
    return {"message": "Hello Burak, FastAPI is working"}
