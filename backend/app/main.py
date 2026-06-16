from fastapi import FastAPI, HTTPException, status, Query
from pydantic import BaseModel

app = FastAPI()

class DatasetCreate(BaseModel):
    name: str
    description: str | None = None
    file_type: str

class DatasetResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    file_type: str
    status: str

class DatasetListResponse(BaseModel):
    count: int
    datasets: list[DatasetResponse]

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

@app.get("/datasets", response_model=DatasetListResponse)
def list_datasets(
    limit: int = Query(default=10, ge=1, le=100), 
    status: str | None = None
):
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

@app.get("/datasets/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int):
    for dataset in datasets:
        if dataset["id"] == dataset_id:
            return dataset
        
    raise HTTPException(
        status_code=404,
        detail="Dataset not found"
    )

@app.post("/datasets",
          status_code=status.HTTP_201_CREATED,
          response_model=DatasetResponse
)
def create_dataset(dataset: DatasetCreate):
    new_dataset = {
        "id": len(datasets) + 1,
        "name": dataset.name,
        "description": dataset.description,
        "file_type": dataset.file_type,
        "status": "created"
    }

    datasets.append(new_dataset)

    return new_dataset

# endregion
