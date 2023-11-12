from config import settings

def is_supported_file_type(filename: str | None) -> str | None:
    if not filename or "." not in filename:
        return False

    _, extension = filename.rsplit(".", maxsplit=1)
    return extension.lower() in settings.SUPPORTED_FILE_TYPES
