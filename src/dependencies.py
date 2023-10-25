from fastapi import UploadFile, status
from fastapi.exceptions import HTTPException
from config import settings

def validate_supported_types(files: list[UploadFile]) -> list[UploadFile]:
    # Collect filenames not in the supported file types
    unsupported_files = [
        file.filename for file in files
        if not file.filename or file.filename.rsplit(".").pop().lower() not in settings.SUPPORTED_FILE_TYPES
    ]

    if unsupported_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported for {unsupported_files}. Please upload files of type: {settings.SUPPORTED_FILE_TYPES}."
        )
    
    return files
