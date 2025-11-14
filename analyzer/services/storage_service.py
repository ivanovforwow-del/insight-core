# services/storage_service.py
from typing import Dict, Any, Optional
import minio
from datetime import datetime
import os


class StorageService:
    """Service class for handling video storage operations"""
    
    def __init__(self, minio_endpoint: str, access_key: str, secret_key: str, secure: bool = False):
        self.minio_client = minio.Minio(
            minio_endpoint,
            access_key=access_key,
            secret_key=secret_key,
            secure=secure
        )
        self.bucket_name = os.getenv('MINIO_BUCKET_NAME', 'insightcore-videos')
        
        # Create bucket if it doesn't exist
        try:
            if not self.minio_client.bucket_exists(self.bucket_name):
                self.minio_client.make_bucket(self.bucket_name)
        except Exception as e:
            print(f"Error creating bucket: {e}")
    
    def upload_video(self, file_path: str, object_name: Optional[str] = None) -> Dict[str, Any]:
        """Upload video file to MinIO storage"""
        if object_name is None:
            object_name = f"videos/{os.path.basename(file_path)}"
        
        try:
            result = self.minio_client.fput_object(
                self.bucket_name,
                object_name,
                file_path,
                content_type="video/mp4"
            )
            return {
                'status': 'uploaded',
                'object_name': object_name,
                'etag': result.etag,
                'version_id': result.version_id
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def download_video(self, object_name: str, file_path: str) -> Dict[str, Any]:
        """Download video file from MinIO storage"""
        try:
            self.minio_client.fget_object(
                self.bucket_name,
                object_name,
                file_path
            )
            return {
                'status': 'downloaded',
                'file_path': file_path
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def get_presigned_url(self, object_name: str, expires_hours: int = 24) -> Dict[str, Any]:
        """Generate presigned URL for video access"""
        try:
            presigned_url = self.minio_client.presigned_get_object(
                self.bucket_name,
                object_name,
                expires=datetime.timedelta(hours=expires_hours)
            )
            return {
                'status': 'success',
                'presigned_url': presigned_url
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def delete_video(self, object_name: str) -> Dict[str, Any]:
        """Delete video file from MinIO storage"""
        try:
            self.minio_client.remove_object(
                self.bucket_name,
                object_name
            )
            return {
                'status': 'deleted',
                'object_name': object_name
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }
    
    def list_videos(self, prefix: str = "videos/") -> Dict[str, Any]:
        """List all video files in storage"""
        try:
            objects = self.minio_client.list_objects(
                self.bucket_name,
                prefix=prefix,
                recursive=True
            )
            video_list = []
            for obj in objects:
                video_list.append({
                    'object_name': obj.object_name,
                    'size': obj.size,
                    'last_modified': obj.last_modified,
                    'etag': obj.etag
                })
            return {
                'status': 'success',
                'videos': video_list
            }
        except Exception as e:
            return {
                'status': 'failed',
                'error': str(e)
            }