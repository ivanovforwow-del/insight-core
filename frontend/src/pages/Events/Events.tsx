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
import { Event } from '../../types';

const { Title } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const Events = () => {
  const [filterVisible, setFilterVisible] = useState(false);
  const [filters, setFilters] = useState<Record<string, any>>({});

  // Данные событий для тестирования
  const { data: events = [], isLoading } = useQuery<Event[]>({
    queryKey: ['events', filters],
    queryFn: async () => [
      {
        id: 1,
        cameraId: 1,
        cameraName: 'Камера 1 (вход)',
        objectType: 'Человек',
        timestamp: '2023-12-01 10:30:15',
        confidence: 0.95,
        severity: 'high',
        imageUrl: '',
        metadata: {
          rule: 'Person in restricted area',
          resolved: false,
          bbox: { x: 100, y: 200, w: 50, h: 100 },
          trackId: 'track_001',
        }
      },
      {
        id: 2,
        cameraId: 2,
        cameraName: 'Камера 2 (парковка)',
        objectType: 'Автомобиль',
        timestamp: '2023-12-01 10:28:42',
        confidence: 0.87,
        severity: 'medium',
        imageUrl: '',
        metadata: {
          rule: 'Vehicle speed limit exceeded',
          resolved: true,
          bbox: { x: 150, y: 250, w: 80, h: 60 },
          trackId: 'track_002',
        }
      },
      {
        id: 3,
        cameraId: 3,
        cameraName: 'Камера 3 (ворота)',
        objectType: 'Сумка',
        timestamp: '2023-12-01 10:25:33',
        confidence: 0.92,
        severity: 'high',
        imageUrl: '',
        metadata: {
          rule: 'Object left behind',
          resolved: false,
          bbox: { x: 300, y: 150, w: 40, h: 30 },
          trackId: 'track_003',
        }
      },
      {
        id: 4,
        cameraId: 4,
        cameraName: 'Камера 1 (склад)',
        objectType: 'Человек',
        timestamp: '2023-12-01 10:22:18',
        confidence: 0.89,
        severity: 'medium',
        imageUrl: '',
        metadata: {
          rule: 'Line crossing',
          resolved: true,
          bbox: { x: 20, y: 180, w: 45, h: 90 },
          trackId: 'track_004',
        }
      },
      {
        id: 5,
        cameraId: 5,
        cameraName: 'Камера 4 (периметр)',
        objectType: 'Человек',
        timestamp: '2023-12-01 10:20:05',
        confidence: 0.78,
        severity: 'low',
        imageUrl: '',
        metadata: {
          rule: 'Loitering detection',
          resolved: false,
          bbox: { x: 250, y: 220, w: 55, h: 95 },
          trackId: 'track_005',
        }
      },
    ],
  });

  const severityColors: Record<string, string> = {
    low: 'green',
    medium: 'orange',
    high: 'red',
    critical: 'red',
  };

  const objectColors: Record<string, string> = {
    Человек: '#1890ff',
    Автомобиль: '#52c41a',
    Грузовик: '#faad14',
    Bag: '#f5222d',
    Велосипед: '#722ed1',
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
            onClick={() => handleViewEvent(record)}
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
    console.log('View event:', event);
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
    <div>
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
                onChange={(value) => handleFilterChange({ camera: value })}
                allowClear
              >
                <Option value="Камера 1 (вход)">Камера 1 (вход)</Option>
                <Option value="Камера 2 (парковка)">Камера 2 (парковка)</Option>
                <Option value="Камера 3 (ворота)">Камера 3 (ворота)</Option>
                <Option value="Камера 1 (склад)">Камера 1 (склад)</Option>
                <Option value="Камера 4 (периметр)">Камера 4 (периметр)</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Select
                style={{ width: '100%' }}
                placeholder="Фильтр по типу объекта"
                onChange={(value) => handleFilterChange({ objectClass: value })}
                allowClear
              >
                <Option value="Человек">Человек</Option>
                <Option value="Автомобиль">Автомобиль</Option>
                <Option value="Грузовик">Грузовик</Option>
                <Option value="Сумка">Сумка</Option>
                <Option value="Велосипед">Велосипед</Option>
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
          dataSource={events}
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