import os

def validate_file_exists(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"The file at {path} does not exist.")
    return True
