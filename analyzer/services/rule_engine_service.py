# services/rule_engine_service.py
from typing import List, Dict, Any, Tuple
from datetime import datetime
import psycopg2
from psycopg2.extras import RealDictCursor
import numpy as np
from .detection_service import Detection
from .tracking_service import Track


class RuleEngineService:
    """Service class for handling rule evaluation and event generation"""
    
    def __init__(self, db_connection_params: Dict[str, Any]):
        self.db_connection_params = db_connection_params
        self.db_connection = psycopg2.connect(**db_connection_params)
    
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