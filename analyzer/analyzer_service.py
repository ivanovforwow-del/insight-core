#!/usr/bin/env python3
"""
Video Analysis Service for InsightCore
This service processes video streams and files using YOLOv8 and OpenCV,
detects objects, tracks them, and generates alerts based on configured rules.
"""

import asyncio
import logging
import json
import time
import threading
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import numpy as np
import cv2
from ultralytics import YOLO
from kafka import KafkaConsumer, KafkaProducer
import redis
import psycopg2
from psycopg2.extras import RealDictCursor
import minio
from dataclasses import dataclass
from enum import Enum
import os
import queue


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DetectionType(Enum):
    PERSON = 'person'
    CAR = 'car'
    TRUCK = 'truck'
    BICYCLE = 'bicycle'
    MOTORCYCLE = 'motorcycle'
    BUS = 'bus'
    TRAIN = 'train'
    TRAFFIC_LIGHT = 'traffic light'
    FIRE_HYDRANT = 'fire hydrant'
    STOP_SIGN = 'stop sign'
    PARKING_METER = 'parking meter'
    BENCH = 'bench'
    BIRD = 'bird'
    CAT = 'cat'
    DOG = 'dog'
    HORSE = 'horse'
    SHEEP = 'sheep'
    COW = 'cow'
    ELEPHANT = 'elephant'
    BEAR = 'bear'
    ZEBRA = 'zebra'
    GIRAFFE = 'giraffe'
    BACKPACK = 'backpack'
    UMBRELLA = 'umbrella'
    HANDBAG = 'handbag'
    TIE = 'tie'
    SUITCASE = 'suitcase'
    FRISBEE = 'frisbee'
    SKIS = 'skis'
    SNOWBOARD = 'snowboard'
    SPORTS_BALL = 'sports ball'
    KITE = 'kite'
    BASEBALL_BAT = 'baseball bat'
    BASEBALL_GLOVE = 'baseball glove'
    SKATEBOARD = 'skateboard'
    SURFBOARD = 'surfboard'
    TENNIS_RACKET = 'tennis racket'
    BOTTLE = 'bottle'
    WINE_GLASS = 'wine glass'
    CUP = 'cup'
    FORK = 'fork'
    KNIFE = 'knife'
    SPOON = 'spoon'
    BOWL = 'bowl'
    BANANA = 'banana'
    APPLE = 'apple'
    SANDWICH = 'sandwich'
    ORANGE = 'orange'
    BROCCOLI = 'broccoli'
    CARROT = 'carrot'
    HOT_DOG = 'hot dog'
    PIZZA = 'pizza'
    DONUT = 'donut'
    CAKE = 'cake'
    CHAIR = 'chair'
    COUCH = 'couch'
    POTTED_PLANT = 'potted plant'
    BED = 'bed'
    DINING_TABLE = 'dining table'
    TOILET = 'toilet'
    TV = 'tv'
    LAPTOP = 'laptop'
    MOUSE = 'mouse'
    REMOTE = 'remote'
    KEYBOARD = 'keyboard'
    CELL_PHONE = 'cell phone'
    MICROWAVE = 'microwave'
    OVEN = 'oven'
    TOASTER = 'toaster'
    SINK = 'sink'
    REFRIGERATOR = 'refrigerator'
    BOOK = 'book'
    CLOCK = 'clock'
    VASE = 'vase'
    SCISSORS = 'scissors'
    TEDDY_BEAR = 'teddy bear'
    HAIR_DRIER = 'hair drier'
    TOOTHBRUSH = 'toothbrush'


@dataclass
class Detection:
    """Detection result from YOLO model"""
    class_id: int
    class_name: str
    confidence: float
    bbox: Tuple[float, float, float, float]  # x1, y1, x2, y2
    center: Tuple[float, float]  # x, y center
    area: float


@dataclass
class Track:
    """Object tracking information"""
    track_id: int
    class_name: str
    bbox_history: List[Tuple[float, float, float, float]]
    center_history: List[Tuple[float, float]]
    last_seen: datetime
    first_seen: datetime
    confidence: float
    is_active: bool = True


class VideoAnalyzer:
    """Main video analysis class using YOLOv8 and OpenCV"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.model = YOLO(config.get('model_path', 'yolov8n.pt'))
        self.confidence_threshold = config.get('confidence_threshold', 0.5)
        self.iou_threshold = config.get('iou_threshold', 0.5)
        self.frame_skip = config.get('frame_skip', 1)
        self.max_objects = config.get('max_objects', 100)
        
        # Tracking
        self.tracks: Dict[int, Track] = {}
        self.next_track_id = 1
        
        # Kafka setup
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=config.get('kafka_servers', ['localhost:9092']),
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        # Redis for caching
        self.redis_client = redis.Redis(
            host=config.get('redis_host', 'localhost'),
            port=config.get('redis_port', 6379),
            db=config.get('redis_db', 0)
        )
        
        # PostgreSQL connection
        self.db_connection = psycopg2.connect(
            host=config.get('db_host', 'localhost'),
            port=config.get('db_port', 5432),
            database=config.get('db_name', 'insightcore'),
            user=config.get('db_user', 'insightcore_user'),
            password=config.get('db_password', 'insightcore_password')
        )
        
        # MinIO client
        self.minio_client = minio.Minio(
            config.get('minio_endpoint', 'localhost:9000'),
            access_key=config.get('minio_access_key', 'minioadmin'),
            secret_key=config.get('minio_secret_key', 'minioadmin'),
            secure=config.get('minio_secure', False)
        )
        
        # Load class names
        self.class_names = self.model.names
        
        logger.info("VideoAnalyzer initialized successfully")
    
    def detect_objects(self, frame: np.ndarray) -> List[Detection]:
        """Run YOLO object detection on frame"""
        try:
            results = self.model(frame, conf=self.confidence_threshold, iou=self.iou_threshold)
            
            detections = []
            for result in results:
                boxes = result.boxes
                if boxes is not None:
                    for box in boxes:
                        class_id = int(box.cls[0])
                        class_name = self.class_names[class_id]
                        confidence = float(box.conf[0])
                        bbox = box.xyxy[0].cpu().numpy()  # x1, y1, x2, y2
                        center = ((bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2)
                        area = (bbox[2] - bbox[0]) * (bbox[3] - bbox[1])
                        
                        detection = Detection(
                            class_id=class_id,
                            class_name=class_name,
                            confidence=confidence,
                            bbox=tuple(bbox),
                            center=center,
                            area=area
                        )
                        detections.append(detection)
            
            return detections
        except Exception as e:
            logger.error(f"Error in object detection: {e}")
            return []
    
    def track_objects(self, detections: List[Detection], frame_shape: Tuple[int, int]) -> List[Track]:
        """Simple object tracking using bounding box matching"""
        current_tracks = []
        
        for detection in detections:
            # Find closest existing track
            best_match = None
            best_distance = float('inf')
            
            for track_id, track in self.tracks.items():
                if track.is_active:
                    last_center = track.center_history[-1]
                    distance = np.sqrt(
                        (detection.center[0] - last_center[0])**2 + 
                        (detection.center[1] - last_center[1])**2
                    )
                    
                    if distance < best_distance and distance < 100:  # Threshold for matching
                        best_distance = distance
                        best_match = track_id
            
            if best_match is not None:
                # Update existing track
                track = self.tracks[best_match]
                track.bbox_history.append(detection.bbox)
                track.center_history.append(detection.center)
                track.last_seen = datetime.now()
                track.confidence = max(track.confidence, detection.confidence)
                current_tracks.append(track)
            else:
                # Create new track
                new_track = Track(
                    track_id=self.next_track_id,
                    class_name=detection.class_name,
                    bbox_history=[detection.bbox],
                    center_history=[detection.center],
                    first_seen=datetime.now(),
                    last_seen=datetime.now(),
                    confidence=detection.confidence
                )
                self.tracks[self.next_track_id] = new_track
                current_tracks.append(new_track)
                self.next_track_id += 1
        
        # Deactivate old tracks
        current_time = datetime.now()
        for track_id, track in list(self.tracks.items()):
            if (current_time - track.last_seen).seconds > 30:  # 30 seconds timeout
                track.is_active = False
        
        # Keep only active tracks
        active_tracks = [track for track in current_tracks if track.is_active]
        return active_tracks
    
    def check_rules(self, tracks: List[Track], camera_id: str, frame_time: datetime) -> List[Dict]:
        """Check if any rules are triggered by the detected objects"""
        triggered_events = []
        
        # Get rules for this camera from database
        cursor = self.db_connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT * FROM rules 
            WHERE camera_id = %s AND enabled = true
        """, (camera_id,))
        rules = cursor.fetchall()
        cursor.close()
        
        for rule in rules:
            if rule['rule_type'] == 'line_crossing':
                events = self._check_line_crossing_rule(tracks, rule, frame_time)
                triggered_events.extend(events)
            elif rule['rule_type'] == 'zone_violation':
                events = self._check_zone_violation_rule(tracks, rule, frame_time)
                triggered_events.extend(events)
            elif rule['rule_type'] == 'behavior_detection':
                events = self._check_behavior_rule(tracks, rule, frame_time)
                triggered_events.extend(events)
            elif rule['rule_type'] == 'loitering':
                events = self._check_loitering_rule(tracks, rule, frame_time)
                triggered_events.extend(events)
            elif rule['rule_type'] == 'object_left_behind':
                events = self._check_object_left_behind_rule(tracks, rule, frame_time)
                triggered_events.extend(events)
        
        return triggered_events
    
    def _check_line_crossing_rule(self, tracks: List[Track], rule: Dict, frame_time: datetime) -> List[Dict]:
        """Check line crossing rule"""
        events = []
        
        # Parse line coordinates from rule conditions
        line_points = rule['conditions'].get('line_points', [])
        if len(line_points) < 2:
            return events
        
        # Simple line crossing detection (simplified for demo)
        for track in tracks:
            if len(track.center_history) >= 2:
                prev_center = track.center_history[-2]
                curr_center = track.center_history[-1]
                
                # Check if line is crossed (simplified algorithm)
                # In real implementation, use proper line intersection algorithm
                if self._line_crossed(prev_center, curr_center, line_points):
                    event = {
                        'rule_id': rule['id'],
                        'camera_id': rule['camera_id'],
                        'timestamp': frame_time.isoformat(),
                        'object_class': track.class_name,
                        'track_id': track.track_id,
                        'bbox': track.bbox_history[-1],
                        'confidence': track.confidence,
                        'severity': rule['severity'],
                        'rule_type': rule['rule_type'],
                        'message': f'{track.class_name} crossed line at {frame_time}'
                    }
                    events.append(event)
        
        return events
    
    def _check_zone_violation_rule(self, tracks: List[Track], rule: Dict, frame_time: datetime) -> List[Dict]:
        """Check zone violation rule"""
        events = []
        
        # Parse zone coordinates from rule conditions
        zone_polygon = rule['conditions'].get('zone_polygon', [])
        if not zone_polygon:
            return events
        
        for track in tracks:
            # Check if object is in zone (simplified point-in-polygon check)
            center = track.center_history[-1]
            if self._point_in_polygon(center, zone_polygon):
                # Check allowed/forbidden objects
                allowed_objects = rule['conditions'].get('allowed_objects', [])
                forbidden_objects = rule['conditions'].get('forbidden_objects', [])
                
                if forbidden_objects and track.class_name in forbidden_objects:
                    event = {
                        'rule_id': rule['id'],
                        'camera_id': rule['camera_id'],
                        'timestamp': frame_time.isoformat(),
                        'object_class': track.class_name,
                        'track_id': track.track_id,
                        'bbox': track.bbox_history[-1],
                        'confidence': track.confidence,
                        'severity': rule['severity'],
                        'rule_type': rule['rule_type'],
                        'message': f'{track.class_name} in forbidden zone at {frame_time}'
                    }
                    events.append(event)
        
        return events
    
    def _check_behavior_rule(self, tracks: List[Track], rule: Dict, frame_time: datetime) -> List[Dict]:
        """Check behavior detection rule"""
        events = []
        
        # Behavior detection would require more complex analysis
        # For now, return empty list
        return events
    
    def _check_loitering_rule(self, tracks: List[Track], rule: Dict, frame_time: datetime) -> List[Dict]:
        """Check loitering detection rule"""
        events = []
        
        for track in tracks:
            # Check if object has been in same area for too long
            if len(track.center_history) > 10:  # At least 10 frames
                # Calculate average position
                avg_x = sum([center[0] for center in track.center_history[-10:]]) / 10
                avg_y = sum([center[1] for center in track.center_history[-10:]]) / 10
                
                # Check if movement is minimal (loitering)
                max_distance = max([
                    np.sqrt((center[0] - avg_x)**2 + (center[1] - avg_y)**2)
                    for center in track.center_history[-10:]
                ])
                
                if max_distance < 50:  # Threshold for loitering
                    event = {
                        'rule_id': rule['id'],
                        'camera_id': rule['camera_id'],
                        'timestamp': frame_time.isoformat(),
                        'object_class': track.class_name,
                        'track_id': track.track_id,
                        'bbox': track.bbox_history[-1],
                        'confidence': track.confidence,
                        'severity': rule['severity'],
                        'rule_type': rule['rule_type'],
                        'message': f'{track.class_name} loitering detected at {frame_time}'
                    }
                    events.append(event)
        
        return events
    
    def _check_object_left_behind_rule(self, tracks: List[Track], rule: Dict, frame_time: datetime) -> List[Dict]:
        """Check object left behind rule"""
        events = []
        
        # This would require tracking static objects over time
        # For now, return empty list
        return events
    
    def _line_crossed(self, point1: Tuple[float, float], point2: Tuple[float, float], line_points: List[Dict]) -> bool:
        """Check if line is crossed between two points"""
        # Simplified line crossing detection
        # In real implementation, use proper line intersection algorithm
        return False
    
    def _point_in_polygon(self, point: Tuple[float, float], polygon: List[Dict]) -> bool:
        """Check if point is inside polygon using ray casting algorithm"""
        x, y = point
        n = len(polygon)
        inside = False
        
        p1x = polygon[0]['x']
        p1y = polygon[0]['y']
        for i in range(1, n + 1):
            p2x = polygon[i % n]['x']
            p2y = polygon[i % n]['y']
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        
        return inside
    
    def process_frame(self, frame: np.ndarray, camera_id: str, frame_time: datetime) -> List[Dict]:
        """Process a single frame and return detected events"""
        # Run object detection
        detections = self.detect_objects(frame)
        
        # Update object tracking
        tracks = self.track_objects(detections, frame.shape)
        
        # Check rules and generate events
        events = self.check_rules(tracks, camera_id, frame_time)
        
        return events
    
    def process_video_stream(self, camera_id: str, stream_url: str):
        """Process video stream from RTSP/HTTP source"""
        logger.info(f"Starting video stream processing for camera {camera_id}")
        
        cap = cv2.VideoCapture(stream_url)
        frame_count = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.warning(f"Failed to read frame from camera {camera_id}")
                    time.sleep(1)
                    continue
                
                frame_count += 1
                if frame_count % self.frame_skip != 0:
                    continue
                
                frame_time = datetime.now()
                
                # Process frame
                events = self.process_frame(frame, camera_id, frame_time)
                
                # Send events to Kafka
                for event in events:
                    self.kafka_producer.send('insightcore-events', event)
                    logger.info(f"Event sent to Kafka: {event}")
                
                # Optional: Draw detections on frame for visualization
                if self.config.get('draw_detections', False):
                    for detection in [d for d in self.detect_objects(frame) if d.confidence > 0.7]:
                        x1, y1, x2, y2 = map(int, detection.bbox)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"{detection.class_name} {detection.confidence:.2f}", 
                                  (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    
                    # Display frame (optional)
                    cv2.imshow(f'Camera {camera_id}', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
        
        except KeyboardInterrupt:
            logger.info(f"Stopping video stream processing for camera {camera_id}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
    
    def process_video_file(self, camera_id: str, file_path: str, start_time: datetime):
        """Process video file"""
        logger.info(f"Starting video file processing: {file_path}")
        
        cap = cv2.VideoCapture(file_path)
        frame_count = 0
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                frame_count += 1
                if frame_count % self.frame_skip != 0:
                    continue
                
                # Calculate actual timestamp for this frame
                frame_time = start_time + datetime.timedelta(seconds=frame_count / fps)
                
                # Process frame
                events = self.process_frame(frame, camera_id, frame_time)
                
                # Send events to Kafka
                for event in events:
                    self.kafka_producer.send('insightcore-events', event)
                    logger.info(f"Event sent to Kafka: {event}")
        
        finally:
            cap.release()
            logger.info(f"Finished processing video file: {file_path}")


class AnalysisService:
    """Main analysis service that manages multiple video streams"""
    
    def __init__(self, config_path: str = 'config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.analyzer = VideoAnalyzer(self.config['analyzer'])
        self.kafka_consumer = KafkaConsumer(
            'insightcore-video-commands',
            bootstrap_servers=self.config['kafka']['bootstrap_servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        self.active_streams = {}
        self.processing_queue = queue.Queue()
        
        logger.info("AnalysisService initialized")
    
    def start(self):
        """Start the analysis service"""
        logger.info("Starting Analysis Service")
        
        # Start Kafka command listener
        command_thread = threading.Thread(target=self._listen_for_commands)
        command_thread.daemon = True
        command_thread.start()
        
        # Start processing queue
        processing_thread = threading.Thread(target=self._process_queue)
        processing_thread.daemon = True
        processing_thread.start()
        
        # Keep main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Shutting down Analysis Service")
            self.stop()
    
    def _listen_for_commands(self):
        """Listen for commands from Kafka"""
        for message in self.kafka_consumer:
            command = message.value
            logger.info(f"Received command: {command}")
            
            if command['type'] == 'start_stream':
                self.start_stream(command['camera_id'], command['stream_url'])
            elif command['type'] == 'stop_stream':
                self.stop_stream(command['camera_id'])
            elif command['type'] == 'process_file':
                self.process_file(command['camera_id'], command['file_path'], command['start_time'])
    
    def _process_queue(self):
        """Process items from the queue"""
        while True:
            try:
                item = self.processing_queue.get(timeout=1)
                if item['type'] == 'stream':
                    self.analyzer.process_video_stream(item['camera_id'], item['stream_url'])
                elif item['type'] == 'file':
                    self.analyzer.process_video_file(item['camera_id'], item['file_path'], item['start_time'])
                self.processing_queue.task_done()
            except queue.Empty:
                continue
    
    def start_stream(self, camera_id: str, stream_url: str):
        """Start processing video stream"""
        if camera_id in self.active_streams:
            logger.warning(f"Stream for camera {camera_id} already active")
            return
        
        stream_task = {
            'type': 'stream',
            'camera_id': camera_id,
            'stream_url': stream_url
        }
        self.processing_queue.put(stream_task)
        self.active_streams[camera_id] = stream_task
        
        logger.info(f"Started stream for camera {camera_id}")
    
    def stop_stream(self, camera_id: str):
        """Stop processing video stream"""
        if camera_id in self.active_streams:
            del self.active_streams[camera_id]
            logger.info(f"Stopped stream for camera {camera_id}")
    
    def process_file(self, camera_id: str, file_path: str, start_time: str):
        """Process video file"""
        file_task = {
            'type': 'file',
            'camera_id': camera_id,
            'file_path': file_path,
            'start_time': datetime.fromisoformat(start_time)
        }
        self.processing_queue.put(file_task)
        
        logger.info(f"Started file processing for camera {camera_id}")
    
    def stop(self):
        """Stop the analysis service"""
        for camera_id in list(self.active_streams.keys()):
            self.stop_stream(camera_id)


def main():
    """Main entry point"""
    config = {
        'analyzer': {
            'model_path': os.getenv('ANALYZER_MODEL_PATH', 'yolov8n.pt'),
            'confidence_threshold': float(os.getenv('ANALYZER_CONFIDENCE_THRESHOLD', 0.5)),
            'iou_threshold': float(os.getenv('ANALYZER_IOU_THRESHOLD', 0.5)),
            'frame_skip': int(os.getenv('ANALYZER_FRAME_SKIP', 1)),
            'draw_detections': os.getenv('ANALYZER_DRAW_DETECTIONS', 'false').lower() == 'true',
            'kafka_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092').split(','),
            'redis_host': os.getenv('REDIS_HOST', 'localhost'),
            'redis_port': int(os.getenv('REDIS_PORT', 6379)),
            'redis_db': int(os.getenv('REDIS_DB', 0)),
            'db_host': os.getenv('POSTGRES_HOST', 'localhost'),
            'db_port': int(os.getenv('POSTGRES_PORT', 5432)),
            'db_name': os.getenv('POSTGRES_DB', 'insightcore'),
            'db_user': os.getenv('POSTGRES_USER', 'insightcore_user'),
            'db_password': os.getenv('POSTGRES_PASSWORD', 'insightcore_password'),
            'minio_endpoint': os.getenv('MINIO_ENDPOINT', 'localhost:9000'),
            'minio_access_key': os.getenv('MINIO_ACCESS_KEY', 'minioadmin'),
            'minio_secret_key': os.getenv('MINIO_SECRET_KEY', 'minioadmin'),
            'minio_secure': os.getenv('MINIO_SECURE', 'false').lower() == 'true',
        },
        'kafka': {
            'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092').split(',')
        }
    }
    
    service = AnalysisService()
    service.config = config
    service.analyzer = VideoAnalyzer(config['analyzer'])
    
    service.start()


if __name__ == "__main__":
    main()