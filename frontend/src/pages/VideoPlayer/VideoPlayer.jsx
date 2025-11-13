import React, { useState, useRef, useEffect } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Space,
  Button,
  Slider,
  Select,
  Input,
  DatePicker,
  Badge,
  Tag,
  Timeline,
  List,
  Modal,
  Progress,
} from 'antd';
import {
  PlayCircleOutlined,
  PauseCircleOutlined,
  StepBackwardOutlined,
  StepForwardOutlined,
  SyncOutlined,
  DownloadOutlined,
  SearchOutlined,
  ClockCircleOutlined,
  VideoCameraOutlined,
  PlaySquareOutlined,
  PictureInPictureOutlined,
  ExpandOutlined,
} from '@ant-design/icons';
import videojs from 'video.js';
import 'video.js/dist/video-js.css';
import '@videojs/themes/fantasy/index.css';
import { useQuery } from '@tanstack/react-query';
import moment from 'moment';

const { Title, Text } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

const VideoPlayer = () => {
  const [videoUrl, setVideoUrl] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
 const [volume, setVolume] = useState(1);
  const [playbackRate, setPlaybackRate] = useState(1);
  const [isFullscreen, setIsFullscreen] = useState(false);
  const [selectedCamera, setSelectedCamera] = useState('');
  const [dateRange, setDateRange] = useState(null);
  const [selectedClip, setSelectedClip] = useState(null);
  const [showClips, setShowClips] = useState(false);
  const [clipModalVisible, setClipModalVisible] = useState(false);

  const videoRef = useRef(null);
  const playerRef = useRef(null);

  // Mock cameras data
  const { data: cameras } = useQuery({
    queryKey: ['cameras'],
    queryFn: async () => [
      { id: 1, name: 'Entrance Cam 1', location: 'Main Entrance', status: 'active' },
      { id: 2, name: 'Parking Cam 2', location: 'Parking Area', status: 'active' },
      { id: 3, name: 'Gate Cam 3', location: 'Main Gate', status: 'inactive' },
      { id: 4, name: 'Warehouse Cam 1', location: 'Warehouse', status: 'active' },
    ],
  });

  // Mock video files data
 const { data: videoFiles } = useQuery({
    queryKey: ['video-files', selectedCamera, dateRange],
    queryFn: async () => [
      {
        id: 1,
        name: 'Entrance Cam 1 - 2023-12-01 10:00:00',
        duration: 3600, // 1 hour in seconds
        size: '1.2 GB',
        resolution: '1920x1080',
        fps: 30,
        startTime: '2023-12-01 10:00',
        endTime: '2023-12-01 11:00',
        url: 'https://example.com/video1.mp4',
      },
      {
        id: 2,
        name: 'Entrance Cam 1 - 2023-12-01 09:00:00',
        duration: 3600,
        size: '1.1 GB',
        resolution: '1920x1080',
        fps: 30,
        startTime: '2023-12-01 09:00:00',
        endTime: '2023-12-01 10:00',
        url: 'https://example.com/video2.mp4',
      },
    ],
  });

  // Mock clips data
  const { data: clips } = useQuery({
    queryKey: ['clips', selectedCamera, dateRange],
    queryFn: async () => [
      {
        id: 1,
        name: 'Person detected at entrance',
        startTime: '2023-12-01 10:30:15',
        endTime: '2023-12-01 10:31:45',
        duration: 90,
        event: 'Person in restricted area',
        severity: 'high',
        confidence: 0.95,
        url: 'https://example.com/clip1.mp4',
      },
      {
        id: 2,
        name: 'Vehicle speed limit exceeded',
        startTime: '2023-12-01 10:28:42',
        endTime: '2023-12-01 10:30:12',
        duration: 90,
        event: 'Vehicle speed limit exceeded',
        severity: 'medium',
        confidence: 0.87,
        url: 'https://example.com/clip2.mp4',
      },
      {
        id: 3,
        name: 'Object left behind',
        startTime: '2023-12-01 10:25:33',
        endTime: '2023-12-01 10:27:03',
        duration: 90,
        event: 'Object left behind',
        severity: 'high',
        confidence: 0.92,
        url: 'https://example.com/clip3.mp4',
      },
    ],
  });

  // Initialize video player
  useEffect(() => {
    if (videoRef.current) {
      const player = videojs(videoRef.current, {
        controls: true,
        responsive: true,
        fluid: true,
        playbackRates: [0.5, 1, 1.5, 2, 4],
        language: 'en',
        theme: 'fantasy',
      });

      playerRef.current = player;

      player.on('loadstart', () => {
        console.log('Video loading started');
      });

      player.on('play', () => {
        setIsPlaying(true);
      });

      player.on('pause', () => {
        setIsPlaying(false);
      });

      player.on('timeupdate', () => {
        setCurrentTime(player.currentTime());
      });

      player.on('durationchange', () => {
        setDuration(player.duration());
      });

      player.on('volumechange', () => {
        setVolume(player.volume());
      });

      return () => {
        if (playerRef.current) {
          playerRef.current.dispose();
        }
      };
    }
  }, []);

  const handlePlay = () => {
    if (playerRef.current) {
      playerRef.current.play();
    }
  };

  const handlePause = () => {
    if (playerRef.current) {
      playerRef.current.pause();
    }
  };

  const handleSeek = (time) => {
    if (playerRef.current) {
      playerRef.current.currentTime(time);
    }
  };

  const handleVolumeChange = (value) => {
    if (playerRef.current) {
      playerRef.current.volume(value);
    }
  };

  const handlePlaybackRateChange = (rate) => {
    if (playerRef.current) {
      playerRef.current.playbackRate(rate);
    }
  };

  const handleFullscreen = () => {
    if (playerRef.current) {
      playerRef.current.requestFullscreen();
    }
  };

 const handleDownload = () => {
    // Download current video
    console.log('Download video:', videoUrl);
  };

 const handlePictureInPicture = () => {
    if (playerRef.current) {
      playerRef.current.requestPictureInPicture();
    }
 };

  const handleSelectVideo = (video) => {
    setVideoUrl(video.url);
    // In real app, you would load the video into the player
    console.log('Selected video:', video);
  };

  const handleSelectClip = (clip) => {
    setSelectedClip(clip);
    setVideoUrl(clip.url);
    setClipModalVisible(true);
    // In real app, you would load the clip into the player
    console.log('Selected clip:', clip);
  };

  const handleDateRangeChange = (dates) => {
    setDateRange(dates);
  };

  const formatTime = (seconds) => {
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    return [h, m, s]
      .map((v) => v.toString().padStart(2, '0'))
      .filter((v, i) => v !== '00' || i > 0)
      .join(':');
  };

  const severityColors = {
    low: 'green',
    medium: 'orange',
    high: 'red',
    critical: 'red',
  };

  const videoFilesColumns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Duration',
      dataIndex: 'duration',
      key: 'duration',
      render: (duration) => formatTime(duration),
    },
    {
      title: 'Size',
      dataIndex: 'size',
      key: 'size',
    },
    {
      title: 'Resolution',
      dataIndex: 'resolution',
      key: 'resolution',
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<PlaySquareOutlined />}
            onClick={() => handleSelectVideo(record)}
          >
            Play
          </Button>
          <Button
            type="link"
            icon={<DownloadOutlined />}
            onClick={() => console.log('Download:', record.url)}
          >
            Download
          </Button>
        </Space>
      ),
    },
  ];

  const clipsColumns = [
    {
      title: 'Event',
      dataIndex: 'event',
      key: 'event',
    },
    {
      title: 'Time',
      key: 'time',
      render: (_, record) => (
        <div>
          <div>{record.startTime}</div>
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {formatTime(record.duration)} duration
          </Text>
        </div>
      ),
    },
    {
      title: 'Severity',
      key: 'severity',
      render: (_, record) => (
        <Tag color={severityColors[record.severity]}>
          {record.severity.toUpperCase()}
        </Tag>
      ),
    },
    {
      title: 'Confidence',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence) => (
        <Space>
          <Progress percent={Math.round(confidence * 100)} size="small" />
          <Text>{(confidence * 100).toFixed(1)}%</Text>
        </Space>
      ),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space>
          <Button
            type="link"
            icon={<PlaySquareOutlined />}
            onClick={() => handleSelectClip(record)}
          >
            Play
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2}>
            <VideoCameraOutlined /> Video Player
          </Title>
        </Col>
        <Col>
          <Space>
            <Select
              placeholder="Select Camera"
              style={{ width: 200 }}
              onChange={setSelectedCamera}
              value={selectedCamera}
            >
              {cameras?.map((camera) => (
                <Option key={camera.id} value={camera.id}>
                  {camera.name} ({camera.location})
                </Option>
              ))}
            </Select>
            <RangePicker
              onChange={handleDateRangeChange}
              style={{ width: 280 }}
            />
          </Space>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={16}>
          <Card>
            <div data-vjs-player>
              <video
                ref={videoRef}
                className="video-js vjs-default-skin"
                controls
                preload="auto"
                width="100%"
                height="400"
              >
                {videoUrl && <source src={videoUrl} type="video/mp4" />}
              </video>
            </div>

            {/* Video Controls */}
            <div style={{ marginTop: 16 }}>
              <Row gutter={16} align="middle">
                <Col span={4}>
                  <Space>
                    <Button
                      icon={isPlaying ? <PauseCircleOutlined /> : <PlayCircleOutlined />}
                      onClick={isPlaying ? handlePause : handlePlay}
                    />
                    <Button
                      icon={<StepBackwardOutlined />}
                      onClick={() => handleSeek(currentTime - 10)}
                    />
                    <Button
                      icon={<StepForwardOutlined />}
                      onClick={() => handleSeek(currentTime + 10)}
                    />
                  </Space>
                </Col>
                <Col span={12}>
                  <Slider
                    min={0}
                    max={duration || 100}
                    value={currentTime}
                    onChange={handleSeek}
                    tipFormatter={formatTime}
                  />
                </Col>
                <Col span={4}>
                  <Text type="secondary">
                    {formatTime(currentTime)} / {formatTime(duration)}
                  </Text>
                </Col>
                <Col span={4}>
                  <Space>
                    <Select
                      value={playbackRate}
                      onChange={handlePlaybackRateChange}
                      size="small"
                      style={{ width: 80 }}
                    >
                      <Option value={0.5}>0.5x</Option>
                      <Option value={1}>1x</Option>
                      <Option value={1.5}>1.5x</Option>
                      <Option value={2}>2x</Option>
                      <Option value={4}>4x</Option>
                    </Select>
                    <Slider
                      min={0}
                      max={1}
                      value={volume}
                      onChange={handleVolumeChange}
                      vertical
                      style={{ height: 80 }}
                    />
                  </Space>
                </Col>
              </Row>

              <Row gutter={8} style={{ marginTop: 16 }}>
                <Col span={6}>
                  <Button
                    icon={<DownloadOutlined />}
                    onClick={handleDownload}
                    block
                  >
                    Download
                  </Button>
                </Col>
                <Col span={6}>
                  <Button
                    icon={<PictureInPictureOutlined />}
                    onClick={handlePictureInPicture}
                    block
                  >
                    PIP
                  </Button>
                </Col>
                <Col span={6}>
                  <Button
                    icon={<ExpandOutlined />}
                    onClick={handleFullscreen}
                    block
                  >
                    Fullscreen
                  </Button>
                </Col>
                <Col span={6}>
                  <Button
                    icon={<SyncOutlined />}
                    onClick={() => setShowClips(!showClips)}
                    type={showClips ? 'primary' : 'default'}
                    block
                  >
                    Show Clips
                  </Button>
                </Col>
              </Row>
            </div>
          </Card>
        </Col>

        <Col span={8}>
          <Card title="Video Files">
            <List
              dataSource={videoFiles || []}
              renderItem={(item) => (
                <List.Item
                  actions={[
                    <Button
                      type="link"
                      icon={<PlaySquareOutlined />}
                      onClick={() => handleSelectVideo(item)}
                    >
                      Play
                    </Button>,
                  ]}
                >
                  <List.Item.Meta
                    title={item.name}
                    description={
                      <div>
                        <div>{item.startTime} - {item.endTime}</div>
                        <Text type="secondary">
                          {item.duration}s • {item.size} • {item.resolution}
                        </Text>
                      </div>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>

          {showClips && (
            <Card title="Event Clips" style={{ marginTop: 16 }}>
              <List
                dataSource={clips || []}
                renderItem={(item) => (
                  <List.Item
                    actions={[
                      <Button
                        type="link"
                        icon={<PlaySquareOutlined />}
                        onClick={() => handleSelectClip(item)}
                      >
                        Play
                      </Button>,
                    ]}
                  >
                    <List.Item.Meta
                      title={
                        <Space>
                          {item.event}
                          <Tag color={severityColors[item.severity]}>
                            {item.severity.toUpperCase()}
                          </Tag>
                        </Space>
                      }
                      description={
                        <div>
                          <div>{item.startTime}</div>
                          <Text type="secondary">
                            {formatTime(item.duration)} • {(item.confidence * 100).toFixed(1)}%
                          </Text>
                        </div>
                      }
                    />
                  </List.Item>
                )}
              />
            </Card>
          )}
        </Col>
      </Row>

      <Modal
        title="Clip Details"
        open={clipModalVisible}
        onCancel={() => setClipModalVisible(false)}
        footer={null}
        width={800}
      >
        {selectedClip && (
          <div>
            <Card style={{ marginBottom: 16 }}>
              <Row gutter={16}>
                <Col span={16}>
                  <div data-vjs-player>
                    <video
                      className="video-js vjs-default-skin"
                      controls
                      preload="auto"
                      width="10%"
                      height="300"
                    >
                      <source src={selectedClip.url} type="video/mp4" />
                    </video>
                  </div>
                </Col>
                <Col span={8}>
                  <div>
                    <Text strong>Event: {selectedClip.event}</Text>
                    <br />
                    <Text type="secondary">Start: {selectedClip.startTime}</Text>
                    <br />
                    <Text type="secondary">End: {selectedClip.endTime}</Text>
                    <br />
                    <Text type="secondary">Duration: {formatTime(selectedClip.duration)}</Text>
                    <br />
                    <Text type="secondary">
                      Severity: <Tag color={severityColors[selectedClip.severity]}>{selectedClip.severity.toUpperCase()}</Tag>
                    </Text>
                    <br />
                    <Text type="secondary">
                      Confidence: {(selectedClip.confidence * 100).toFixed(1)}%
                    </Text>
                  </div>
                </Col>
              </Row>
            </Card>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default VideoPlayer;