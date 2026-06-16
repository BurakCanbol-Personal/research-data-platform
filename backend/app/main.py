from fastapi import FastAPI, HTTPException, status
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

# region Health routes

@app.get("/health")
def health_check():
    return {"status": "ok"}


# endregion



# region Dataset routes

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
        
    raise HTTPException(
        status_code=404,
        detail="Dataset not found"
    )

@app.post("/datasets", status_code=status.HTTP_201_CREATED)
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

# endregion
