# core/event_publisher.py
from typing import Dict, Any, List
from kafka import KafkaProducer
import json
import redis
from .config import Config


class EventPublisher:
    """Service for publishing events to Kafka and caching in Redis"""
    
    def __init__(self, config: Config):
        self.config = config
        
        # Initialize Kafka producer
        self.kafka_producer = KafkaProducer(
            bootstrap_servers=config.get_kafka_config()['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )
        
        # Initialize Redis client
        self.redis_client = redis.Redis(**config.get_redis_config())
    
    def publish_event(self, event: Dict[str, Any]) -> bool:
        """Publish a single event to Kafka"""
        try:
            self.kafka_producer.send('insightcore-events', event)
            self.kafka_producer.flush()  # Ensure the message is sent
            
            # Cache event in Redis for quick access
            event_key = f"event:{event['timestamp']}:{event.get('track_id', 'unknown')}"
            self.redis_client.setex(
                event_key, 
                3600,  # Expire after 1 hour
                json.dumps(event)
            )
            
            return True
        except Exception as e:
            print(f"Error publishing event: {e}")
            return False
    
    def publish_events(self, events: List[Dict[str, Any]]) -> int:
        """Publish multiple events to Kafka"""
        success_count = 0
        for event in events:
            if self.publish_event(event):
                success_count += 1
        return success_count
    
    def publish_command(self, command: Dict[str, Any]) -> bool:
        """Publish a command to Kafka command topic"""
        try:
            self.kafka_producer.send('insightcore-video-commands', command)
            self.kafka_producer.flush()
            return True
        except Exception as e:
            print(f"Error publishing command: {e}")
            return False
    
    def cache_camera_status(self, camera_id: str, status: str, ttl: int = 300) -> bool:
        """Cache camera status in Redis"""
        try:
            key = f"camera:{camera_id}:status"
            self.redis_client.setex(key, ttl, status)
            return True
        except Exception as e:
            print(f"Error caching camera status: {e}")
            return False
    
    def get_cached_event(self, event_key: str) -> Dict[str, Any]:
        """Get cached event from Redis"""
        try:
            cached_event = self.redis_client.get(event_key)
            if cached_event:
                return json.loads(cached_event)
            return None
        except Exception as e:
            print(f"Error getting cached event: {e}")
            return None