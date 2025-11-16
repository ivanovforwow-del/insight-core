# factories.py
import factory
from django.contrib.auth.models import User
from cameras.models import Camera, Zone, Line
from events.models import Rule, Event
from alerts.models import Alert, AlertChannel
from videos.models import VideoFile, Clip, VideoAnnotation
from django.utils import timezone
from uuid import uuid4


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class CameraFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Camera

    name = factory.Sequence(lambda n: f"Camera {n}")
    rtsp_url = factory.LazyAttribute(lambda obj: f"rtsp://example.com/camera{obj.id}")
    location = factory.Faker('address')
    status = factory.Iterator(['active', 'inactive', 'error', 'maintenance'])
    vendor = factory.Faker('company')


class ZoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Zone

    name = factory.Sequence(lambda n: f"Zone {n}")
    camera = factory.SubFactory(CameraFactory)
    polygon = factory.LazyAttribute(lambda obj: [{'x': 0, 'y': 0}, {'x': 100, 'y': 0}, {'x': 100, 'y': 100}, {'x': 0, 'y': 100}])
    zone_type = factory.Iterator(['entry', 'exit', 'restricted', 'counting', 'detection', 'custom'])
    allowed_objects = factory.LazyAttribute(lambda obj: ['person', 'car'])
    forbidden_objects = factory.LazyAttribute(lambda obj: [])


class LineFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Line

    name = factory.Sequence(lambda n: f"Line {n}")
    camera = factory.SubFactory(CameraFactory)
    points = factory.LazyAttribute(lambda obj: [{'x': 0, 'y': 50}, {'x': 100, 'y': 50}])
    direction = factory.Iterator(['horizontal', 'vertical', 'custom'])
    allowed_objects = factory.LazyAttribute(lambda obj: ['person', 'car'])


class EventRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Rule

    name = factory.Sequence(lambda n: f"Event Rule {n}")
    camera = factory.SubFactory(CameraFactory)
    rule_type = factory.Iterator(['line_crossing', 'zone_violation', 'behavior_detection', 'loitering', 'object_left_behind', 'speed_detection', 'counting', 'custom'])
    conditions = factory.LazyAttribute(lambda obj: {"min_confidence": 0.5, "min_area": 100})
    severity = factory.Iterator(['low', 'medium', 'high', 'critical'])
    enabled = True


class AnalyticsRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'analytics.Rule'

    name = factory.Sequence(lambda n: f"Analytics Rule {n}")
    camera = factory.SubFactory(CameraFactory)
    rule_type = factory.Iterator(['line_crossing', 'zone_violation', 'behavior_detection', 'loitering', 'object_left_behind', 'speed_detection', 'counting', 'custom'])
    conditions = factory.LazyAttribute(lambda obj: {"min_confidence": 0.5, "min_area": 100})
    severity = factory.Iterator(['low', 'medium', 'high', 'critical'])
    enabled = True


class VideoFileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoFile

    camera = factory.SubFactory(CameraFactory)
    start_time = factory.LazyAttribute(lambda obj: timezone.now() - timezone.timedelta(hours=1))
    end_time = factory.LazyAttribute(lambda obj: timezone.now())
    duration = 3600.0
    storage_path = factory.LazyAttribute(lambda obj: f"videos/camera_{obj.camera.id}/video_{uuid4()}.mp4")
    file_size = factory.LazyAttribute(lambda obj: 100000000)  # 100MB
    fps = 30.0
    resolution = "1920x1080"


class ClipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Clip

    video_file = factory.SubFactory(VideoFileFactory)
    start_offset = 10.0
    end_offset = 20.0
    label = factory.Faker('word')


class VideoAnnotationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = VideoAnnotation

    clip = factory.SubFactory(ClipFactory)
    label = factory.Faker('word')
    start_time = 0.0
    end_time = 5.0
    bbox = factory.LazyAttribute(lambda obj: {'x': 10, 'y': 10, 'w': 50, 'h': 50})
    confidence = 0.9
    created_by = factory.SubFactory(UserFactory)


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    rule = factory.SubFactory(EventRuleFactory)
    camera = factory.SubFactory(CameraFactory)
    timestamp = factory.LazyAttribute(lambda obj: timezone.now())
    object_class = factory.Iterator(['person', 'car', 'truck', 'bicycle'])
    track_id = factory.Sequence(lambda n: f"track_{n}")
    bbox = factory.LazyAttribute(lambda obj: {'x': 10, 'y': 10, 'w': 50, 'h': 50})
    confidence = 0.8
    severity = factory.Iterator(['low', 'medium', 'high', 'critical'])
    clip = factory.SubFactory(ClipFactory)


class AnalyticsEventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'analytics.Event'

    rule = factory.SubFactory(AnalyticsRuleFactory)
    camera = factory.SubFactory(CameraFactory)
    timestamp = factory.LazyAttribute(lambda obj: timezone.now())
    object_class = factory.Iterator(['person', 'car', 'truck', 'bicycle'])
    track_id = factory.Sequence(lambda n: f"track_{n}")
    bbox = factory.LazyAttribute(lambda obj: {'x': 10, 'y': 10, 'w': 50, 'h': 50})
    confidence = 0.8
    severity = factory.Iterator(['low', 'medium', 'high', 'critical'])
    clip = factory.SubFactory(ClipFactory)


class AlertChannelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = AlertChannel

    name = factory.Sequence(lambda n: f"Alert Channel {n}")
    channel_type = factory.Iterator(['telegram', 'email', 'webhook', 'sms', 'push'])
    config = factory.LazyAttribute(lambda obj: {"token": "test_token", "chat_id": "test_chat_id"})


class AlertFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Alert

    event = factory.SubFactory(EventFactory)
    channel = factory.SubFactory(AlertChannelFactory)
    status = factory.Iterator(['pending', 'sent', 'failed', 'delivered'])
    message = factory.Faker('sentence')