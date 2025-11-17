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
      title: 'Правило',
      dataIndex: ['metadata', 'rule'],
      key: 'rule',
      sorter: (a: Event, b: Event) => (a.metadata?.rule || '').localeCompare(b.metadata?.rule || ''),
    },
    {
      title: 'Камера',
      dataIndex: 'cameraName',
      key: 'cameraName',
      sorter: (a: Event, b: Event) => a.cameraName.localeCompare(b.cameraName),
    },
    {
      title: 'Объект',
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
      title: 'Время',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: (a: Event, b: Event) => moment(a.timestamp).diff(moment(b.timestamp)),
    },
    {
      title: 'Достоверность',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence: number) => `${(confidence * 100).toFixed(1)}%`,
      sorter: (a: Event, b: Event) => a.confidence - b.confidence,
    },
    {
      title: 'Важность',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity: string) => (
        <Tag color={severityColors[severity]}>
          {severity.toUpperCase()}
        </Tag>
      ),
      sorter: (a: Event, b: Event) => a.severity.localeCompare(b.severity),
      filters: [
        { text: 'Низкая', value: 'low' },
        { text: 'Средняя', value: 'medium' },
        { text: 'Высокая', value: 'high' },
        { text: 'Критическая', value: 'critical' },
      ],
      onFilter: (value: boolean | React.Key, record: Event) => record.severity === value,
    },
    {
      title: 'Статус',
      key: 'resolved',
      render: (_: any, record: Event) => (
        <Badge
          status={record.metadata?.resolved ? 'success' : 'error'}
          text={record.metadata?.resolved ? 'Решено' : 'В ожидании'}
        />
      ),
      filters: [
        { text: 'Решено', value: true },
        { text: 'В ожидании', value: false },
      ],
      onFilter: (value: boolean | React.Key, record: Event) => record.metadata?.resolved === value,
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_: any, record: Event) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => setSelectedEvent(record)}
          >
            Просмотр
          </Button>
          <Button
            type="link"
            icon={<DownloadOutlined />}
            onClick={() => handleDownloadClip(record)}
          >
            Клип
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
            <AlertOutlined /> События
          </Title>
        </Col>
        <Col>
          <Space>
            <RangePicker onChange={handleDateRangeChange} />
            <Button
              icon={<FilterOutlined />}
              onClick={() => setFilterVisible(!filterVisible)}
            >
              Фильтры
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
                placeholder="Фильтр по камере"
                onChange={(value) => handleFilterChange({ cameraId: value })}
                allowClear
              >
                <Option value="Entrance Cam 1">Камера входа 1</Option>
                <Option value="Parking Cam 2">Камера парковки 2</Option>
                <Option value="Gate Cam 3">Камера ворот 3</Option>
                <Option value="Warehouse Cam 1">Камера склада 1</Option>
                <Option value="Perimeter Cam 4">Камера периметра 4</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Select
                style={{ width: '100%' }}
                placeholder="Фильтр по типу объекта"
                onChange={(value) => handleFilterChange({ objectType: value })}
                allowClear
              >
                <Option value="Person">Человек</Option>
                <Option value="Car">Автомобиль</Option>
                <Option value="Truck">Грузовик</Option>
                <Option value="Bag">Сумка</Option>
                <Option value="Bicycle">Велосипед</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Input
                placeholder="Поиск событий..."
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
        title="Детали события"
        open={!!selectedEvent}
        onCancel={() => setSelectedEvent(null)}
        footer={[
          <Button key="close" onClick={() => setSelectedEvent(null)}>
            Закрыть
          </Button>,
        ]}
      >
        {selectedEvent && (
          <div>
            <Typography.Title level={4}>{selectedEvent.cameraName}</Typography.Title>
            <Typography.Paragraph>
              <strong>Объект:</strong> {selectedEvent.objectType}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Время:</strong> {selectedEvent.timestamp}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Достоверность:</strong> {(selectedEvent.confidence * 100).toFixed(1)}%
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Важность:</strong> {selectedEvent.severity.toUpperCase()}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Статус:</strong> {selectedEvent.metadata?.resolved ? 'Решено' : 'В ожидании'}
            </Typography.Paragraph>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default EventsDataFetcher;