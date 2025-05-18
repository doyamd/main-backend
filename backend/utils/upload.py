import cloudinary
import cloudinary.uploader
from typing import Optional, Tuple
from django.core.files.uploadedfile import UploadedFile

def upload_file(file: UploadedFile, folder: str = "legal_documents") -> Tuple[str, Optional[str]]:
    """
    Upload a file to Cloudinary and return the URL and public_id
    
    Args:
        file (UploadedFile): The file to upload
        folder (str): The folder in Cloudinary where the file should be stored
        
    Returns:
        Tuple[str, Optional[str]]: A tuple containing (file_url, public_id)
        
    Raises:
        Exception: If the upload fails
    """
    try:
        # Upload the file to Cloudinary
        result = cloudinary.uploader.upload(
            file,
            folder=folder,
            resource_type="auto"  # Automatically detect if it's an image, video, or raw file
        )
        
        # Return the secure URL and public_id
        return result.get('secure_url'), result.get('public_id')
    except Exception as e:
        raise Exception(f"Failed to upload file: {str(e)}")

def delete_file(public_id: str) -> bool:
    """
    Delete a file from Cloudinary using its public_id
    
    Args:
        public_id (str): The public_id of the file to delete
        
    Returns:
        bool: True if deletion was successful, False otherwise
    """
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get('result') == 'ok'
    except Exception as e:
        raise Exception(f"Failed to delete file: {str(e)}") 