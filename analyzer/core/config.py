# core/config.py
import os
from typing import Dict, Any


class Config:
    """Configuration class for analyzer service"""
    
    def __init__(self):
        self.model_path = os.getenv('ANALYZER_MODEL_PATH', 'yolov8n.pt')
        self.confidence_threshold = float(os.getenv('ANALYZER_CONFIDENCE_THRESHOLD', 0.5))
        self.iou_threshold = float(os.getenv('ANALYZER_IOU_THRESHOLD', 0.5))
        self.frame_skip = int(os.getenv('ANALYZER_FRAME_SKIP', 1))
        self.draw_detections = os.getenv('ANALYZER_DRAW_DETECTIONS', 'false').lower() == 'true'
        self.max_objects = int(os.getenv('ANALYZER_MAX_OBJECTS', 100))
        
        # Kafka configuration
        self.kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092').split(',')
        
        # Redis configuration
        self.redis_host = os.getenv('REDIS_HOST', 'localhost')
        self.redis_port = int(os.getenv('REDIS_PORT', 6379))
        self.redis_db = int(os.getenv('REDIS_DB', 0))
        
        # Database configuration
        self.db_host = os.getenv('POSTGRES_HOST', 'localhost')
        self.db_port = int(os.getenv('POSTGRES_PORT', 5432))
        self.db_name = os.getenv('POSTGRES_DB', 'insightcore')
        self.db_user = os.getenv('POSTGRES_USER', 'insightcore_user')
        self.db_password = os.getenv('POSTGRES_PASSWORD', 'insightcore_password')
        
        # MinIO configuration
        self.minio_endpoint = os.getenv('MINIO_ENDPOINT', 'localhost:9000')
        self.minio_access_key = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
        self.minio_secret_key = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
        self.minio_secure = os.getenv('MINIO_SECURE', 'false').lower() == 'true'
        self.minio_bucket_name = os.getenv('MINIO_BUCKET_NAME', 'insightcore-videos')
    
    def get_db_connection_params(self) -> Dict[str, Any]:
        """Get database connection parameters"""
        return {
            'host': self.db_host,
            'port': self.db_port,
            'database': self.db_name,
            'user': self.db_user,
            'password': self.db_password
        }
    
    def get_minio_config(self) -> Dict[str, Any]:
        """Get MinIO configuration"""
        return {
            'endpoint': self.minio_endpoint,
            'access_key': self.minio_access_key,
            'secret_key': self.minio_secret_key,
            'secure': self.minio_secure
        }
    
    def get_kafka_config(self) -> Dict[str, Any]:
        """Get Kafka configuration"""
        return {
            'bootstrap_servers': self.kafka_servers
        }
    
    def get_redis_config(self) -> Dict[str, Any]:
        """Get Redis configuration"""
        return {
            'host': self.redis_host,
            'port': self.redis_port,
            'db': self.redis_db
        }