import React, { useState, useRef, useEffect } from 'react';
import {
  Card,
  Row,
  Col,
  Button,
  Slider,
  Space,
  Typography,
  Select,
  InputNumber,
  Switch,
  Modal,
  Tag,
} from 'antd';
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  StepBackwardOutlined,
  StepForwardOutlined,
  FullscreenOutlined,
  FullscreenExitOutlined,
  SoundFilled,
  SettingOutlined,
  VideoCameraOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import type { Video } from '../../types';

const { Title, Text } = Typography;
const { Option } = Select;

// Define the video player props
interface VideoPlayerProps {
  video: Video;
}

const VideoPlayer: React.FC<VideoPlayerProps> = ({ video }) => {
  const videoRef = useRef<HTMLDivElement>(null);
  const playerRef = useRef<any | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [volume, setVolume] = useState(1.0);
  const [playbackRate, setPlaybackRate] = useState(1.0);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [showSettings, setShowSettings] = useState(false);

  useEffect(() => {
    if (!videoRef.current) return;

    const videoJsOptions: any = {
      autoplay: false,
      controls: true,
      responsive: true,
      fluid: true,
      sources: [
        {
          src: video.url,
          type: video.format,
        },
      ],
    };

    playerRef.current = videojs(videoRef.current, videoJsOptions, () => {
      console.log('Player is ready');
    });

    const player = playerRef.current;

    player.on('play', () => setIsPlaying(true));
    player.on('pause', () => setIsPlaying(false));
    player.on('timeupdate', () => {
      setCurrentTime(player.currentTime() || 0);
      setDuration(player.duration() || 0);
    });

    return () => {
      if (player) {
        player.dispose();
      }
    };
  }, [video.url, video.format]);

  const handlePlayPause = () => {
    const player = playerRef.current;
    if (player) {
      if (isPlaying) {
        player.pause();
      } else {
        player.play();
      }
    }
  };

  const handleFullscreen = () => {
    const player = playerRef.current;
    if (player) {
      if (isFullscreen) {
        player.exitFullscreen();
      } else {
        player.requestFullscreen();
      }
      setIsFullscreen(!isFullscreen);
    }
  };

  const handleVolumeChange = (value: number) => {
    setVolume(value);
    const player = playerRef.current;
    if (player) {
      player.volume(value);
    }
 };

  const handlePlaybackRateChange = (rate: number) => {
    setPlaybackRate(rate);
    const player = playerRef.current;
    if (player) {
      player.playbackRate(rate);
    }
  };

  const handleTimeChange = (time: number) => {
    setCurrentTime(time);
    const player = playerRef.current;
    if (player) {
      player.currentTime(time);
    }
  };

  const formatTime = (seconds: number): string => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    if (hours > 0) {
      return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
    }
    return `${minutes}:${secs.toString().padStart(2, '0')}`;
  };

  const mockVideo: Video = {
    id: 1,
    name: 'Test Video',
    cameraId: 1,
    cameraName: 'Entrance Cam 1',
    startTime: '2023-12-01 10:00:00',
    endTime: '2023-12-01 11:00:00',
    duration: 3600,
    size: 102400,
    format: 'mp4',
    url: 'https://example.com/test-video.mp4',
    thumbnailUrl: '',
  };

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2}>
            <VideoCameraOutlined /> Video Player
          </Title>
          <Text type="secondary">Playing: {video.name}</Text>
        </Col>
        <Col>
          <Space>
            <Tag icon={<ClockCircleOutlined />} color="blue">
              {video.startTime}
            </Tag>
            <Tag icon={<CheckCircleOutlined />} color="green">
              {video.cameraName}
            </Tag>
          </Space>
        </Col>
      </Row>

      <Card>
        <Row gutter={16}>
          <Col span={18}>
            <div data-vjs-player>
              <div ref={videoRef} />
            </div>

            {/* Custom Controls */}
            <div style={{ marginTop: 16, padding: '16px 0' }}>
              <Row align="middle" gutter={16}>
                <Col>
                  <Button
                    icon={isPlaying ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
                    onClick={handlePlayPause}
                    type="primary"
                  />
                </Col>
                <Col flex="auto">
                  <Slider
                    min={0}
                    max={duration}
                    value={currentTime}
                    onChange={handleTimeChange}
                    tooltip={{ formatter: (value) => value !== undefined ? formatTime(value) : '' }}
                  />
                </Col>
                <Col>
                  <Text type="secondary">
                    {formatTime(currentTime)} / {formatTime(duration)}
                  </Text>
                </Col>
              </Row>

              <Row align="middle" gutter={16} style={{ marginTop: 16 }}>
                <Col>
                  <Space>
                    <Button
                      icon={<StepBackwardOutlined />}
                      onClick={() => handleTimeChange(currentTime - 10)}
                    >
                      -10s
                    </Button>
                    <Button
                      icon={<StepForwardOutlined />}
                      onClick={() => handleTimeChange(currentTime + 10)}
                    >
                      +10s
                    </Button>
                  </Space>
                </Col>
                <Col>
                  <Space>
                    <SoundFilled />
                    <Slider
                      min={0}
                      max={1}
                      step={0.1}
                      value={volume}
                      onChange={handleVolumeChange}
                      style={{ width: 100 }}
                    />
                  </Space>
                </Col>
                <Col>
                  <Space>
                    <Select
                      value={playbackRate}
                      onChange={handlePlaybackRateChange}
                      style={{ width: 100 }}
                    >
                      <Option value={0.5}>0.5x</Option>
                      <Option value={1.0}>1x</Option>
                      <Option value={1.5}>1.5x</Option>
                      <Option value={2.0}>2x</Option>
                    </Select>
                  </Space>
                </Col>
                <Col>
                  <Button
                    icon={isFullscreen ? <FullscreenExitOutlined /> : <FullscreenOutlined />}
                    onClick={handleFullscreen}
                  />
                </Col>
                <Col>
                  <Button
                    icon={<SettingOutlined />}
                    onClick={() => setShowSettings(true)}
                  />
                </Col>
              </Row>
            </div>
          </Col>
          <Col span={6}>
            <Card title="Video Info" size="small">
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <Text strong>Camera:</Text>
                  <Text> {video.cameraName}</Text>
                </div>
                <div>
                  <Text strong>Start Time:</Text>
                  <Text> {video.startTime}</Text>
                </div>
                <div>
                  <Text strong>End Time:</Text>
                  <Text> {video.endTime}</Text>
                </div>
                <div>
                  <Text strong>Duration:</Text>
                  <Text> {formatTime(video.duration)}</Text>
                </div>
                <div>
                  <Text strong>Size:</Text>
                  <Text> {(video.size / (1024 * 1024)).toFixed(2)} MB</Text>
                </div>
                <div>
                  <Text strong>Format:</Text>
                  <Text> {video.format.toUpperCase()}</Text>
                </div>
              </Space>
            </Card>

            <Card title="Playback Settings" size="small" style={{ marginTop: 16 }}>
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <Text>Volume</Text>
                  <Slider
                    min={0}
                    max={1}
                    step={0.1}
                    value={volume}
                    onChange={handleVolumeChange}
                  />
                </div>
                <div>
                  <Text>Playback Speed</Text>
                  <Select
                    value={playbackRate}
                    onChange={handlePlaybackRateChange}
                    style={{ width: '100%' }}
                  >
                    <Option value={0.5}>0.5x</Option>
                    <Option value={1.0}>1x</Option>
                    <Option value={1.5}>1.5x</Option>
                    <Option value={2.0}>2x</Option>
                  </Select>
                </div>
              </Space>
            </Card>
          </Col>
        </Row>
      </Card>

      <Modal
        title="Video Settings"
        open={showSettings}
        onCancel={() => setShowSettings(false)}
        footer={[
          <Button key="close" onClick={() => setShowSettings(false)}>
            Close
          </Button>,
        ]}
      >
        <Space direction="vertical" style={{ width: '100%' }}>
          <div>
            <Text>Volume</Text>
            <Slider
              min={0}
              max={1}
              step={0.1}
              value={volume}
              onChange={handleVolumeChange}
            />
          </div>
          <div>
            <Text>Playback Speed</Text>
            <Select
              value={playbackRate}
              onChange={handlePlaybackRateChange}
              style={{ width: '100%' }}
            >
              <Option value={0.5}>0.5x</Option>
              <Option value={1.0}>1x</Option>
              <Option value={1.5}>1.5x</Option>
              <Option value={2.0}>2x</Option>
            </Select>
          </div>
          <div>
            <Text>Auto-play</Text>
            <Switch defaultChecked />
          </div>
        </Space>
      </Modal>
    </div>
  );
};

const VideoPlayerPage: React.FC = () => {
  // Mock video data
  const mockVideo: Video = {
    id: 1,
    name: 'Test Video',
    cameraId: 1,
    cameraName: 'Entrance Cam 1',
    startTime: '2023-12-01 10:00:00',
    endTime: '2023-12-01 11:00:00',
    duration: 3600,
    size: 1024000,
    format: 'mp4',
    url: 'https://example.com/test-video.mp4',
    thumbnailUrl: '',
  };

  return <VideoPlayer video={mockVideo} />;
};

export default VideoPlayerPage;