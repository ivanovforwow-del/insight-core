# app.py
from typing import Dict, Any
import asyncio
import logging
import json
import time
import threading
from datetime import datetime
import queue
from .core.config import Config
from .core.analysis_engine import AnalysisEngine
from .core.event_publisher import EventPublisher
from kafka import KafkaConsumer


class AnalysisService:
    """Main analysis service that manages multiple video streams"""
    
    def __init__(self, config: Config = None):
        self.config = config or Config()
        self.analysis_engine = AnalysisEngine(self.config)
        self.event_publisher = EventPublisher(self.config)
        
        self.kafka_consumer = KafkaConsumer(
            'insightcore-video-commands',
            bootstrap_servers=self.config.get_kafka_config()['bootstrap_servers'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        self.active_streams = {}
        self.processing_queue = queue.Queue()
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self.logger.info("AnalysisService initialized")
    
    def start(self):
        """Start the analysis service"""
        self.logger.info("Starting Analysis Service")
        
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
            self.logger.info("Shutting down Analysis Service")
            self.stop()
    
    def _listen_for_commands(self):
        """Listen for commands from Kafka"""
        for message in self.kafka_consumer:
            command = message.value
            self.logger.info(f"Received command: {command}")
            
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
                    self.analysis_engine.process_video_stream(item['camera_id'], item['stream_url'])
                elif item['type'] == 'file':
                    from datetime import datetime
                    self.analysis_engine.process_video_file(
                        item['camera_id'], 
                        item['file_path'], 
                        datetime.fromisoformat(item['start_time'])
                    )
                self.processing_queue.task_done()
            except queue.Empty:
                continue
    
    def start_stream(self, camera_id: str, stream_url: str):
        """Start processing video stream"""
        if camera_id in self.active_streams:
            self.logger.warning(f"Stream for camera {camera_id} already active")
            return
        
        stream_task = {
            'type': 'stream',
            'camera_id': camera_id,
            'stream_url': stream_url
        }
        self.processing_queue.put(stream_task)
        self.active_streams[camera_id] = stream_task
        
        # Cache camera status
        self.event_publisher.cache_camera_status(camera_id, 'active')
        
        self.logger.info(f"Started stream for camera {camera_id}")
    
    def stop_stream(self, camera_id: str):
        """Stop processing video stream"""
        if camera_id in self.active_streams:
            del self.active_streams[camera_id]
            
            # Cache camera status
            self.event_publisher.cache_camera_status(camera_id, 'inactive')
            
            self.logger.info(f"Stopped stream for camera {camera_id}")
    
    def process_file(self, camera_id: str, file_path: str, start_time: str):
        """Process video file"""
        file_task = {
            'type': 'file',
            'camera_id': camera_id,
            'file_path': file_path,
            'start_time': start_time
        }
        self.processing_queue.put(file_task)
        
        self.logger.info(f"Started file processing for camera {camera_id}")
    
    def stop(self):
        """Stop the analysis service"""
        for camera_id in list(self.active_streams.keys()):
            self.stop_stream(camera_id)


def main():
    """Main entry point"""
    config = Config()
    service = AnalysisService(config)
    service.start()


if __name__ == "__main__":
    main()