from fastapi import APIRouter, HTTPException, status, Query, File, UploadFile
from pydantic import BaseModel

from app.services.file_service import save_uploaded_file

router = APIRouter(
    prefix="/datasets",
    tags=["Datasets"]
)

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
    saved_path: str | None = None

class DatasetListResponse(BaseModel):
    count: int
    datasets: list[DatasetResponse]

datasets = []

def create_dataset_record(
        name: str,
        file_type: str,
        description: str | None = None,
        status: str = "created",
        saved_path: str | None = None
):
    
    new_dataset = {
        "id": len(datasets) + 1,
        "name": name,
        "description": description,
        "file_type": file_type,
        "status": status,
        "saved_path": saved_path 
    }
    
    datasets.append(new_dataset)

    return new_dataset

@router.get("/", response_model=DatasetListResponse)
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

@router.get("/{dataset_id}", response_model=DatasetResponse)
def get_dataset(dataset_id: int):
    for dataset in datasets:
        if dataset["id"] == dataset_id:
            return dataset
        
    raise HTTPException(
        status_code=404,
        detail="Dataset not found"
    )

@router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=DatasetResponse
)
def create_dataset(dataset: DatasetCreate):
    new_dataset = create_dataset_record(
        name= dataset.name,
        file_type= dataset.file_type,
        description= dataset.description,
    )

    return new_dataset


@router.post("/upload",
             status_code=status.HTTP_201_CREATED,
             response_model=DatasetResponse
)
def upload_dataset(file: UploadFile = File(...)):

    try:
        saved_path = save_uploaded_file(file)
        file_type = file.filename.split(".")[-1].lower()

        new_dataset = create_dataset_record(
            name= file.filename,
            file_type= file_type,
            status= "uploaded",
            saved_path= saved_path
        )

        return new_dataset
    
    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

