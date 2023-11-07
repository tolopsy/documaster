from config import settings

def is_supported_file_type(filename: str | None) -> str | None:
    extension = filename.rsplit(".", maxsplit=1).pop() if "." in filename else None
    return extension.lower() in settings.SUPPORTED_FILE_TYPES
