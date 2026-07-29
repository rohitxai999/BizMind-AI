from fastapi import APIRouter, File, UploadFile, HTTPException
import pandas as pd
import os

from app.services.business_service import BusinessService
from app.schemas.analysis import BusinessInput

router = APIRouter(
    prefix="/upload",
    tags=["File Upload"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/")
async def upload_file(file: UploadFile = File(...)):

    filename = file.filename
    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(await file.read())

    if filename.endswith(".csv"):
        df = pd.read_csv(filepath)

    elif filename.endswith(".xlsx"):
        df = pd.read_excel(filepath)

    else:
        raise HTTPException(
            status_code=400,
            detail="Only CSV and Excel files are supported."
        )

    results = []

    for _, row in df.iterrows():

        business = BusinessInput(
            revenue=row["revenue"],
            expenses=row["expenses"],
            customers=row["customers"],
            employees=row["employees"]
        )

        results.append(
            BusinessService.analyze(business)
        )

    return {
        "records": len(results),
        "analysis": results
    }