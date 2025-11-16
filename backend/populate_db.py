#!/usr/bin/env python
"""Script to populate database with test data"""

import os
import sys
import django
from django.conf import settings

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

django.setup()

from django.contrib.auth.models import User
from cameras.models import Camera, Zone, Line
from events.models import Rule, Event
from alerts.models import Alert, AlertChannel
from videos.models import VideoFile, Clip, VideoAnnotation
from factories import (
    UserFactory, CameraFactory, ZoneFactory, LineFactory,
    EventRuleFactory, AnalyticsRuleFactory, EventFactory, AnalyticsEventFactory,
    AlertFactory, AlertChannelFactory, VideoFileFactory, ClipFactory, VideoAnnotationFactory
)
from django.db import transaction

def populate_database(clear_first=False):
    if clear_first:
        print('Clearing existing data...')
        with transaction.atomic():
            Alert.objects.all().delete()
            Event.objects.all().delete()
            Clip.objects.all().delete()
            VideoFile.objects.all().delete()
            VideoAnnotation.objects.all().delete()
            Rule.objects.all().delete()
            Zone.objects.all().delete()
            Line.objects.all().delete()
            AlertChannel.objects.all().delete()
            Camera.objects.all().delete()
            User.objects.all().delete()

    print('Seeding database...')
    
    # Create users
    users = UserFactory.create_batch(5)
    
    # Create cameras
    cameras = CameraFactory.create_batch(10)
    
    # Create zones
    zones = []
    for camera in cameras:
        zones.extend(ZoneFactory.create_batch(2, camera=camera))
    
    # Create lines
    lines = []
    for camera in cameras:
        lines.extend(LineFactory.create_batch(2, camera=camera))
    
    # Create alert channels
    alert_channels = AlertChannelFactory.create_batch(5)
    
    # Create rules
    event_rules = []
    analytics_rules = []
    for camera in cameras:
        event_rules.extend(EventRuleFactory.create_batch(2, camera=camera))
        analytics_rules.extend(AnalyticsRuleFactory.create_batch(1, camera=camera))
    
    # Create video files
    video_files = []
    for camera in cameras:
        video_files.extend(VideoFileFactory.create_batch(3, camera=camera))
    
    # Create clips
    clips = []
    for video_file in video_files:
        clips.extend(ClipFactory.create_batch(2, video_file=video_file))
    
    # Create video annotations
    video_annotations = []
    for clip in clips[:20]:  # Limit to avoid too many annotations
        video_annotations.extend(VideoAnnotationFactory.create_batch(3, clip=clip))
    
    # Create events
    events = EventFactory.create_batch(30)
    analytics_events = AnalyticsEventFactory.create_batch(20)
    
    # Create alerts
    alerts = []
    for event in events:
        for channel in alert_channels[:2]:
            alerts.append(AlertFactory(event=event, channel=channel))
    
    print(
        f'Successfully seeded database with:\n'
        f'- {len(users)} users\n'
        f'- {len(cameras)} cameras\n'
        f'- {len(zones)} zones\n'
        f'- {len(lines)} lines\n'
        f'- {len(alert_channels)} alert channels\n'
        f'- {len(event_rules)} event rules\n'
        f'- {len(analytics_rules)} analytics rules\n'
        f'- {len(video_files)} video files\n'
        f'- {len(clips)} clips\n'
        f'- {len(video_annotations)} video annotations\n'
        f'- {len(events)} events\n'
        f'- {len(analytics_events)} analytics events\n'
        f'- {len(alerts)} alerts'
    )

if __name__ == '__main__':
    populate_database(clear_first=True)