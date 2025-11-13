import React, { useState } from 'react';
import {
  Card,
  Table,
  Typography,
  Space,
  Tag,
  Button,
  Modal,
  DatePicker,
  Select,
  Input,
  Badge,
  Row,
  Col,
} from 'antd';
import {
  AlertOutlined,
  EyeOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  FilterOutlined,
  SearchOutlined,
  DownloadOutlined,
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import moment from 'moment';

const { Title } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const Events = () => {
  const [filterVisible, setFilterVisible] = useState(false);
  const [filters, setFilters] = useState({});

  // Mock events data
  const { data: events, isLoading } = useQuery({
    queryKey: ['events', filters],
    queryFn: async () => [
      {
        id: 1,
        rule: 'Person in restricted area',
        camera: 'Entrance Cam 1',
        objectClass: 'Person',
        timestamp: '2023-12-01 10:30:15',
        confidence: 0.95,
        severity: 'high',
        resolved: false,
        bbox: { x: 100, y: 200, w: 50, h: 100 },
        trackId: 'track_001',
      },
      {
        id: 2,
        rule: 'Vehicle speed limit exceeded',
        camera: 'Parking Cam 2',
        objectClass: 'Car',
        timestamp: '2023-12-01 10:28:42',
        confidence: 0.87,
        severity: 'medium',
        resolved: true,
        bbox: { x: 150, y: 250, w: 80, h: 60 },
        trackId: 'track_002',
      },
      {
        id: 3,
        rule: 'Object left behind',
        camera: 'Gate Cam 3',
        objectClass: 'Bag',
        timestamp: '2023-12-01 10:25:33',
        confidence: 0.92,
        severity: 'high',
        resolved: false,
        bbox: { x: 300, y: 150, w: 40, h: 30 },
        trackId: 'track_003',
      },
      {
        id: 4,
        rule: 'Line crossing',
        camera: 'Warehouse Cam 1',
        objectClass: 'Person',
        timestamp: '2023-12-01 10:22:18',
        confidence: 0.89,
        severity: 'medium',
        resolved: true,
        bbox: { x: 20, y: 180, w: 45, h: 90 },
        trackId: 'track_004',
      },
      {
        id: 5,
        rule: 'Loitering detection',
        camera: 'Perimeter Cam 4',
        objectClass: 'Person',
        timestamp: '2023-12-01 10:20:05',
        confidence: 0.78,
        severity: 'low',
        resolved: false,
        bbox: { x: 250, y: 220, w: 55, h: 95 },
        trackId: 'track_005',
      },
    ],
  });

  const severityColors = {
    low: 'green',
    medium: 'orange',
    high: 'red',
    critical: 'red',
  };

  const objectColors = {
    Person: '#1890ff',
    Car: '#52c41a',
    Truck: '#faad14',
    Bag: '#f5222d',
    Bicycle: '#722ed1',
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      sorter: (a, b) => a.id - b.id,
    },
    {
      title: 'Rule',
      dataIndex: 'rule',
      key: 'rule',
      sorter: (a, b) => a.rule.localeCompare(b.rule),
    },
    {
      title: 'Camera',
      dataIndex: 'camera',
      key: 'camera',
      sorter: (a, b) => a.camera.localeCompare(b.camera),
    },
    {
      title: 'Object',
      dataIndex: 'objectClass',
      key: 'objectClass',
      render: (objectClass) => (
        <Tag color={objectColors[objectClass] || 'default'}>
          {objectClass}
        </Tag>
      ),
      sorter: (a, b) => a.objectClass.localeCompare(b.objectClass),
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: (a, b) => moment(a.timestamp).diff(moment(b.timestamp)),
    },
    {
      title: 'Confidence',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence) => `${(confidence * 100).toFixed(1)}%`,
      sorter: (a, b) => a.confidence - b.confidence,
    },
    {
      title: 'Severity',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity) => (
        <Tag color={severityColors[severity]}>
          {severity.toUpperCase()}
        </Tag>
      ),
      sorter: (a, b) => a.severity.localeCompare(b.severity),
      filters: [
        { text: 'Low', value: 'low' },
        { text: 'Medium', value: 'medium' },
        { text: 'High', value: 'high' },
        { text: 'Critical', value: 'critical' },
      ],
      onFilter: (value, record) => record.severity === value,
    },
    {
      title: 'Status',
      key: 'resolved',
      render: (_, record) => (
        <Badge
          status={record.resolved ? 'success' : 'error'}
          text={record.resolved ? 'Resolved' : 'Pending'}
        />
      ),
      filters: [
        { text: 'Resolved', value: true },
        { text: 'Pending', value: false },
      ],
      onFilter: (value, record) => record.resolved === value,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => handleViewEvent(record)}
          >
            View
          </Button>
          <Button
            type="link"
            icon={<DownloadOutlined />}
            onClick={() => handleDownloadClip(record)}
          >
            Clip
          </Button>
        </Space>
      ),
    },
  ];

  const handleViewEvent = (event) => {
    console.log('View event:', event);
  };

  const handleDownloadClip = (event) => {
    console.log('Download clip for event:', event);
  };

  const handleFilterChange = (changedValues) => {
    setFilters({ ...filters, ...changedValues });
  };

  const handleDateRangeChange = (dates, dateStrings) => {
    if (dates) {
      handleFilterChange({
        startDate: dateStrings[0],
        endDate: dateStrings[1],
      });
    } else {
      const newFilters = { ...filters };
      delete newFilters.startDate;
      delete newFilters.endDate;
      setFilters(newFilters);
    }
  };

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2}>
            <AlertOutlined /> Events
          </Title>
        </Col>
        <Col>
          <Space>
            <RangePicker onChange={handleDateRangeChange} />
            <Button
              icon={<FilterOutlined />}
              onClick={() => setFilterVisible(!filterVisible)}
            >
              Filters
            </Button>
          </Space>
        </Col>
      </Row>

      {filterVisible && (
        <Card style={{ marginBottom: 24 }}>
          <Row gutter={16}>
            <Col span={8}>
              <Select
                style={{ width: '100%' }}
                placeholder="Filter by camera"
                onChange={(value) => handleFilterChange({ camera: value })}
                allowClear
              >
                <Option value="Entrance Cam 1">Entrance Cam 1</Option>
                <Option value="Parking Cam 2">Parking Cam 2</Option>
                <Option value="Gate Cam 3">Gate Cam 3</Option>
                <Option value="Warehouse Cam 1">Warehouse Cam 1</Option>
                <Option value="Perimeter Cam 4">Perimeter Cam 4</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Select
                style={{ width: '100%' }}
                placeholder="Filter by object type"
                onChange={(value) => handleFilterChange({ objectClass: value })}
                allowClear
              >
                <Option value="Person">Person</Option>
                <Option value="Car">Car</Option>
                <Option value="Truck">Truck</Option>
                <Option value="Bag">Bag</Option>
                <Option value="Bicycle">Bicycle</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Input
                placeholder="Search events..."
                prefix={<SearchOutlined />}
                onChange={(e) => handleFilterChange({ search: e.target.value })}
              />
            </Col>
          </Row>
        </Card>
      )}

      <Card>
        <Table
          columns={columns}
          dataSource={events || []}
          loading={isLoading}
          rowKey="id"
          pagination={{ pageSize: 15 }}
          scroll={{ x: 1200 }}
        />
      </Card>
    </div>
  );
};

export default Events;