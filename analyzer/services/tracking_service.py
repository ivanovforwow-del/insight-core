# services/tracking_service.py
from typing import List, Dict, Any, Tuple
from datetime import datetime
from dataclasses import dataclass
import numpy as np
from .detection_service import Detection


@dataclass
class Track:
    """Object tracking information"""
    track_id: int
    class_name: str
    bbox_history: List[Tuple[float, float, float, float]]
    center_history: List[Tuple[float, float]]
    first_seen: datetime
    last_seen: datetime
    confidence: float
    is_active: bool = True


class TrackingService:
    """Service class for handling object tracking logic"""
    
    def __init__(self, max_inactive_time: int = 30):  # 30 seconds timeout
        self.tracks: Dict[int, Track] = {}
        self.next_track_id = 1
        self.max_inactive_time = max_inactive_time
    
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
            if (current_time - track.last_seen).seconds > self.max_inactive_time:
                track.is_active = False
        
        # Keep only active tracks
        active_tracks = [track for track in current_tracks if track.is_active]
        return active_tracks
    
    def get_all_tracks(self) -> List[Track]:
        """Get all current tracks"""
        return list(self.tracks.values())
    
    def get_active_tracks(self) -> List[Track]:
        """Get only active tracks"""
        return [track for track in self.tracks.values() if track.is_active]
    
    def reset_tracks(self):
        """Reset all tracks"""
        self.tracks = {}
        self.next_track_id = 1