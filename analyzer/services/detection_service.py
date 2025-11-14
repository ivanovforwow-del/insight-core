# services/detection_service.py
from typing import List, Dict, Any, Tuple
import numpy as np
import cv2
from ultralytics import YOLO
from dataclasses import dataclass
from enum import Enum


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


class DetectionService:
    """Service class for handling object detection logic"""
    
    def __init__(self, model_path: str = 'yolov8n.pt', confidence_threshold: float = 0.5, iou_threshold: float = 0.5):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.iou_threshold = iou_threshold
        self.class_names = self.model.names
    
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
            print(f"Error in object detection: {e}")
            return []
    
    def draw_detections(self, frame: np.ndarray, detections: List[Detection], confidence_threshold: float = 0.7) -> np.ndarray:
        """Draw detections on frame for visualization"""
        for detection in detections:
            if detection.confidence > confidence_threshold:
                x1, y1, x2, y2 = map(int, detection.bbox)
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, f"{detection.class_name} {detection.confidence:.2f}", 
                          (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return frame