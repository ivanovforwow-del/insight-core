'use client';

import React from 'react';
import { useQuery } from '@tanstack/react-query';
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
import moment from 'moment';
import { Event } from '@/types';
import { useEvents, useEvent, useRecentEvents, useUpdateEventStatus, useDeleteEvent } from '@/hooks/data/useEventData';

const { Title } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

interface EventsDataFetcherProps {
  initialFilters?: Record<string, any>;
}

const EventsDataFetcher: React.FC<EventsDataFetcherProps> = ({ initialFilters = {} }) => {
  const [filterVisible, setFilterVisible] = React.useState(false);
  const [filters, setFilters] = React.useState<Record<string, any>>(initialFilters);
  const [selectedEvent, setSelectedEvent] = React.useState<Event | null>(null);

  const { data: events = { data: [], total: 0, page: 1, limit: 10 }, isLoading } = useEvents(filters);
  const updateEventStatusMutation = useUpdateEventStatus();
  const deleteEventMutation = useDeleteEvent();

  const severityColors: Record<string, string> = {
    low: 'green',
    medium: 'orange',
    high: 'red',
    critical: 'red',
  };

  const objectColors: Record<string, string> = {
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
      sorter: (a: Event, b: Event) => a.id - b.id,
    },
    {
      title: 'Rule',
      dataIndex: ['metadata', 'rule'],
      key: 'rule',
      sorter: (a: Event, b: Event) => (a.metadata?.rule || '').localeCompare(b.metadata?.rule || ''),
    },
    {
      title: 'Camera',
      dataIndex: 'cameraName',
      key: 'cameraName',
      sorter: (a: Event, b: Event) => a.cameraName.localeCompare(b.cameraName),
    },
    {
      title: 'Object',
      dataIndex: 'objectType',
      key: 'objectType',
      render: (objectType: string) => (
        <Tag color={objectColors[objectType] || 'default'}>
          {objectType}
        </Tag>
      ),
      sorter: (a: Event, b: Event) => a.objectType.localeCompare(b.objectType),
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: (a: Event, b: Event) => moment(a.timestamp).diff(moment(b.timestamp)),
    },
    {
      title: 'Confidence',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence: number) => `${(confidence * 100).toFixed(1)}%`,
      sorter: (a: Event, b: Event) => a.confidence - b.confidence,
    },
    {
      title: 'Severity',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity: string) => (
        <Tag color={severityColors[severity]}>
          {severity.toUpperCase()}
        </Tag>
      ),
      sorter: (a: Event, b: Event) => a.severity.localeCompare(b.severity),
      filters: [
        { text: 'Low', value: 'low' },
        { text: 'Medium', value: 'medium' },
        { text: 'High', value: 'high' },
        { text: 'Critical', value: 'critical' },
      ],
      onFilter: (value: boolean | React.Key, record: Event) => record.severity === value,
    },
    {
      title: 'Status',
      key: 'resolved',
      render: (_: any, record: Event) => (
        <Badge
          status={record.metadata?.resolved ? 'success' : 'error'}
          text={record.metadata?.resolved ? 'Resolved' : 'Pending'}
        />
      ),
      filters: [
        { text: 'Resolved', value: true },
        { text: 'Pending', value: false },
      ],
      onFilter: (value: boolean | React.Key, record: Event) => record.metadata?.resolved === value,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Event) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => setSelectedEvent(record)}
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

  const handleViewEvent = (event: Event) => {
    setSelectedEvent(event);
  };

  const handleDownloadClip = (event: Event) => {
    console.log('Download clip for event:', event);
  };

  const handleFilterChange = (changedValues: Record<string, any>) => {
    setFilters({ ...filters, ...changedValues });
  };

  const handleDateRangeChange = (dates: any, dateStrings: [string, string]) => {
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
    <div style={{ padding: '24px' }}>
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
                onChange={(value) => handleFilterChange({ cameraId: value })}
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
                onChange={(value) => handleFilterChange({ objectType: value })}
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
          dataSource={events.data}
          loading={isLoading}
          rowKey="id"
          pagination={{ 
            pageSize: events.limit, 
            total: events.total,
            current: events.page,
            onChange: (page, pageSize) => setFilters({ ...filters, page, limit: pageSize })
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      <Modal
        title="Event Details"
        open={!!selectedEvent}
        onCancel={() => setSelectedEvent(null)}
        footer={[
          <Button key="close" onClick={() => setSelectedEvent(null)}>
            Close
          </Button>,
        ]}
      >
        {selectedEvent && (
          <div>
            <Typography.Title level={4}>{selectedEvent.cameraName}</Typography.Title>
            <Typography.Paragraph>
              <strong>Object:</strong> {selectedEvent.objectType}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Timestamp:</strong> {selectedEvent.timestamp}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Confidence:</strong> {(selectedEvent.confidence * 100).toFixed(1)}%
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Severity:</strong> {selectedEvent.severity.toUpperCase()}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Status:</strong> {selectedEvent.metadata?.resolved ? 'Resolved' : 'Pending'}
            </Typography.Paragraph>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default EventsDataFetcher;