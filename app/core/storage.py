import os
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from app.core.config import settings

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class StorageService:
    @staticmethod
    def get_upload_dir() -> Path:
        return UPLOAD_DIR

    @staticmethod
    async def save_upload(file_obj, filename: str) -> str:
        """Saves a file locally and returns a 'path' identifier."""
        file_path = UPLOAD_DIR / filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file_obj.file, buffer)
        return str(file_path)

    @staticmethod
    def generate_signed_url(file_path: str, expiration_minutes: int = 60) -> str:
        """
        In a real cloud scenario (S3/Supabase), this generates a PRESIGNED URL.
        For local dev + Colab, we need the Colab to access THIS laptop.
        If the laptop is NOT exposed to the web, Colab cannot download from it directly 
        unless the laptop ALSO exposes a tunnel or uploads to cloud.
        
        As per the "Hub-and-Spoke" diagram, if 'Storage' is Firebase/Supabase,
        we assume the file is ALREADY there or we upload it there.
        
        For this MVP, we will assume we Return a Mock Signed URL or 
        we need a mechanism to upload to Supabase.
        """
        # TODO: Integrate actual Supabase/Firebase SDK here.
        # For now, we assume the 'file_path' is a key in the cloud bucket.
        return f"https://mock-storage.com/{file_path}?token=mock-signed-token"

    @staticmethod
    def upload_to_cloud(local_path: str, destination_path: str):
        """Mock upload to cloud storage."""
        print(f"Uploading {local_path} to Cloud at {destination_path}...")
        return destination_path
