from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DatasetCreate(BaseModel):
    name: str
    description: str | None = None
    file_type: str

datasets = []

@app.get("/")
def root():
    return {"message": "Hello Burak, FastAPI is working"}


@app.get("/health")
def health_check():
    return {"status": "ok"}

##datasets
@app.get("/datasets")
def list_datasets(limit: int = 10, status: str | None = None):
    results = datasets

    if status is not None:
        results = [
            dataset for dataset in datasets
            if dataset["status"] == status
        ]
    
    return {
        "count": len(results[:limit]),
        "datasets": results[:limit]
    }

@app.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: int):
    for dataset in datasets:
        if dataset["id"] == dataset_id:
            return dataset
        
    return {"error": "Dataset not found"}

@app.post("/datasets")
def create_dataset(dataset: DatasetCreate):
    new_dataset = {
        "id": len(datasets) + 1,
        "name": dataset.name,
        "description": dataset.description,
        "file_type": dataset.file_type,
        "status": "created"
    }

    datasets.append(new_dataset)

    return{
        "message": "Dataset created successfully",
        "dataset": new_dataset
    }

@app.get("/users/{username}")
def get_user(username: str):
    return {
        "username": username,
        "message": f"Profile page for {username}"
    }

@app.get("/search")
def search(q: str | None = None, limit: int = 10):
    return{
        "query": q,
        "limit": limit,
        "message": f"Searching for {q} with limit {limit}"
    }