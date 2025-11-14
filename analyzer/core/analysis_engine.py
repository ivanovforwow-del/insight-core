# core/analysis_engine.py
from typing import List, Dict, Any, Tuple
from datetime import datetime
import numpy as np
import cv2
from kafka import KafkaProducer
import redis
import json
from .config import Config
from ..services.detection_service import DetectionService, Detection
from ..services.tracking_service import TrackingService, Track
from ..services.rule_engine_service import RuleEngineService
from ..services.storage_service import StorageService


class AnalysisEngine:
    """Main analysis engine that coordinates detection, tracking, and rule evaluation"""
    
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize services
        self.detection_service = DetectionService(
            model_path=config.model_path,
            confidence_threshold=config.confidence_threshold,
            iou_threshold=config.iou_threshold
        )
        self.tracking_service = TrackingService()
        self.rule_engine_service = RuleEngineService(
            db_connection_params=config.get_db_connection_params()
        )
        self.storage_service = StorageService(**config.get_minio_config())
        
        # Initialize Kafka producer
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=config.get_kafka_config()['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        # Initialize Redis client
        self.redis_client = redis.Redis(**config.get_redis_config())
    
    def process_frame(self, frame: np.ndarray, camera_id: str, frame_time: datetime) -> List[Dict]:
        """Process a single frame and return detected events"""
        # Run object detection
        detections = self.detection_service.detect_objects(frame)
        
        # Update object tracking
        tracks = self.tracking_service.track_objects(detections, frame.shape)
        
        # Check rules and generate events
        events = self.rule_engine_service.check_rules(tracks, camera_id, frame_time)
        
        return events
    
    def process_video_stream(self, camera_id: str, stream_url: str):
        """Process video stream from RTSP/HTTP source"""
        print(f"Starting video stream processing for camera {camera_id}")
        
        cap = cv2.VideoCapture(stream_url)
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print(f"Failed to read frame from camera {camera_id}")
                    break
                
                frame_count += 1
                if frame_count % self.config.frame_skip != 0:
                    continue
                
                frame_time = datetime.now()
                
                # Process frame
                events = self.process_frame(frame, camera_id, frame_time)
                
                # Send events to Kafka
                for event in events:
                    self.kafka_producer.send('insightcore-events', event)
                    print(f"Event sent to Kafka: {event}")
                
                # Optional: Draw detections on frame for visualization
                if self.config.draw_detections:
                    detections = self.detection_service.detect_objects(frame)
                    frame = self.detection_service.draw_detections(frame, detections)
                    
                    # Display frame (optional)
                    cv2.imshow(f'Camera {camera_id}', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        
        except KeyboardInterrupt:
            print(f"Stopping video stream processing for camera {camera_id}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
    
    def process_video_file(self, camera_id: str, file_path: str, start_time: datetime):
        """Process video file"""
        print(f"Starting video file processing: {file_path}")
        
        cap = cv2.VideoCapture(file_path)
        frame_count = 0
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                if frame_count % self.config.frame_skip != 0:
                    continue
                
                # Calculate actual timestamp for this frame
                frame_time = start_time + datetime.timedelta(seconds=frame_count / fps)
                
                # Process frame
                events = self.process_frame(frame, camera_id, frame_time)
                
                # Send events to Kafka
                for event in events:
                    self.kafka_producer.send('insightcore-events', event)
                    print(f"Event sent to Kafka: {event}")
        
        finally:
            cap.release()
            print(f"Finished processing video file: {file_path}")