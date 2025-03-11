from firebase_admin import storage
from typing import Any, Optional
import uuid

bucket = storage.bucket()

async def upload_file(file_data: bytes, file_type: str) -> str:
    """
    Upload a file to Google Cloud Storage
    Returns the public URL of the uploaded file
    """
    file_name = f"{uuid.uuid4()}.{file_type}"
    blob = bucket.blob(file_name)
    blob.upload_from_string(file_data, content_type=f"image/{file_type}")
    blob.make_public()
    
    return blob.public_url

async def delete_file(file_url: str) -> bool:
    """
    Delete a file from Google Cloud Storage
    Returns True if successful, False otherwise
    """
    try:
        # Extract the file name from the URL
        file_name = file_url.split('/')[-1]
        blob = bucket.blob(file_name)
        blob.delete()
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False