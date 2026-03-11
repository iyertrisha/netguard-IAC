from fastapi import APIRouter, UploadFile
from .terraform_parser import parse_terraform
from .kubernetes_parser import parse_kubernetes

router = APIRouter()

@router.post("/parse")
async def parse_file(file: UploadFile):

    content = (await file.read()).decode()

    filename = file.filename

    if filename.endswith(".tf"):
        return parse_terraform(content)

    if filename.endswith(".yaml") or filename.endswith(".yml"):
        return parse_kubernetes(content)

    return {"error": "Unsupported file type"}