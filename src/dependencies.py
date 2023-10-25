from fastapi import UploadFile, status
from fastapi.exceptions import HTTPException
from config import settings
from utils import is_supported_file_type

def validate_supported_types(files: list[UploadFile]) -> list[UploadFile]:
    # Collect filenames not in the supported file types    
    unsupported_files = [
        file.filename for file in files
        if not is_supported_file_type(file.filename)
    ]

    if unsupported_files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not supported for {unsupported_files}. Supported file types are: {settings.SUPPORTED_FILE_TYPES}."
        )
    
    return files
