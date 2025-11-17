import React from 'react';
import {
  Card,
  Row,
  Col,
  Statistic,
  Table,
  Typography,
  Space,
  Tag,
  Progress,
  Select,
  DatePicker,
  Button,
} from 'antd';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  LineChart,
 Line,
} from 'recharts';
import {
  AreaChartOutlined,
  VideoCameraOutlined,
  AlertOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  EyeOutlined,
  UserOutlined,
  CarOutlined,
  VideoCameraAddOutlined,
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { AnalyticsData, EventByType, EventByHour, Event } from '../../types';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const Analytics = () => {
  const [timeRange, setTimeRange] = React.useState<string>('7d');
  const [dateRange, setDateRange] = React.useState<[string, string] | null>(null);

  // Данные аналитики для тестирования
  const { data: analyticsData } = useQuery<AnalyticsData>({
    queryKey: ['analytics-data', timeRange, dateRange],
    queryFn: async () => ({
      totalCameras: 45,
      activeCameras: 42,
      totalEvents: 128,
      eventsToday: 24,
      alertsToday: 8,
      totalVideos: 156,
      processingTime: '2.3s',
      systemUptime: '99.9%',
    }),
  });

  // Mock events by type
  const eventsByType: EventByType[] = [
    { name: 'Person', value: 56 },
    { name: 'Vehicle', value: 32 },
    { name: 'Car', value: 28 },
    { name: 'Truck', value: 12 },
    { name: 'Bicycle', value: 8 },
  ];

  // Mock events by hour
 const eventsByHour: EventByHour[] = [
    { hour: '00:00', events: 2 },
    { hour: '01:00', events: 1 },
    { hour: '02:00', events: 0 },
    { hour: '03:00', events: 1 },
    { hour: '04:00', events: 3 },
    { hour: '05:00', events: 5 },
    { hour: '06:00', events: 8 },
    { hour: '07:00', events: 12 },
    { hour: '08:00', events: 15 },
    { hour: '09:00', events: 18 },
    { hour: '10:00', events: 22 },
    { hour: '11:00', events: 19 },
    { hour: '12:00', events: 16 },
    { hour: '13:00', events: 14 },
    { hour: '14:00', events: 17 },
    { hour: '15:00', events: 20 },
    { hour: '16:00', events: 24 },
    { hour: '17:00', events: 21 },
    { hour: '18:00', events: 18 },
    { hour: '19:00', events: 15 },
    { hour: '20:00', events: 12 },
    { hour: '21:00', events: 9 },
    { hour: '22:00', events: 6 },
    { hour: '23:00', events: 4 },
  ];

  // Mock events by day for line chart
 const eventsByDay = [
    { date: '2023-12-01', events: 24 },
    { date: '2023-12-02', events: 18 },
    { date: '2023-12-03', events: 32 },
    { date: '2023-12-04', events: 27 },
    { date: '2023-12-05', events: 19 },
    { date: '2023-12-06', events: 25 },
    { date: '2023-12-07', events: 31 },
  ];

  // Последние события для тестирования
  const { data: recentEvents = [] } = useQuery<Event[]>({
    queryKey: ['recent-events', timeRange, dateRange],
    queryFn: async () => [
      {
        id: 1,
        cameraId: 1,
        cameraName: 'Entrance Cam 1',
        objectType: 'Person',
        timestamp: '2023-12-01 10:30:15',
        confidence: 0.95,
        severity: 'high',
      },
      {
        id: 2,
        cameraId: 2,
        cameraName: 'Parking Cam 2',
        objectType: 'Car',
        timestamp: '2023-12-01 10:28:42',
        confidence: 0.87,
        severity: 'medium',
      },
      {
        id: 3,
        cameraId: 3,
        cameraName: 'Gate Cam 3',
        objectType: 'Truck',
        timestamp: '2023-12-01 10:25:33',
        confidence: 0.92,
        severity: 'low',
      },
      {
        id: 4,
        cameraId: 4,
        cameraName: 'Warehouse Cam 1',
        objectType: 'Person',
        timestamp: '2023-12-01 10:22:18',
        confidence: 0.89,
        severity: 'high',
      },
      {
        id: 5,
        cameraId: 5,
        cameraName: 'Perimeter Cam 4',
        objectType: 'Vehicle',
        timestamp: '2023-12-01 10:20:05',
        confidence: 0.78,
        severity: 'medium',
      },
    ],
  });

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];
  const SEVERITY_COLORS: Record<string, string> = {
    low: 'green',
    medium: 'orange',
    high: 'red',
    critical: 'red',
  };

  const handleTimeRangeChange = (value: string) => {
    setTimeRange(value);
 };

  const handleDateRangeChange = (dates: any, dateStrings: [string, string]) => {
    setDateRange(dates ? dateStrings : null);
  };

  const statColumns = [
    {
      title: 'Метрика',
      dataIndex: 'metric',
      key: 'metric',
    },
    {
      title: 'Значение',
      dataIndex: 'value',
      key: 'value',
    },
    {
      title: 'Изменение',
      dataIndex: 'change',
      key: 'change',
      render: (change: number) => (
        <Tag color={change >= 0 ? 'green' : 'red'}>
          {change >= 0 ? '↑' : '↓'} {Math.abs(change)}%
        </Tag>
      ),
    },
  ];

  const statData = [
    {
      key: 1,
      metric: 'Всего камер',
      value: analyticsData?.totalCameras || 0,
      change: 5,
    },
    {
      key: 2,
      metric: 'Активных камер',
      value: analyticsData?.activeCameras || 0,
      change: 3,
    },
    {
      key: 3,
      metric: 'Всего событий',
      value: analyticsData?.totalEvents || 0,
      change: 12,
    },
    {
      key: 4,
      metric: 'Событий сегодня',
      value: analyticsData?.eventsToday || 0,
      change: -2,
    },
    {
      key: 5,
      metric: 'Оповещений сегодня',
      value: analyticsData?.alertsToday || 0,
      change: 8,
    },
    {
      key: 6,
      metric: 'Всего видео',
      value: analyticsData?.totalVideos || 0,
      change: 7,
    },
  ];

  const eventColumns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
    },
    {
      title: 'Камера',
      dataIndex: 'cameraName',
      key: 'cameraName',
    },
    {
      title: 'Объект',
      dataIndex: 'objectType',
      key: 'objectType',
      render: (text: string) => (
        <Space>
          {text === 'Person' && <UserOutlined />}
          {text === 'Car' && <CarOutlined />}
          {text === 'Truck' && <CarOutlined />}
          {text === 'Vehicle' && <CarOutlined />}
          {text}
        </Space>
      ),
    },
    {
      title: 'Время',
      dataIndex: 'timestamp',
      key: 'timestamp',
    },
    {
      title: 'Достоверность',
      dataIndex: 'confidence',
      key: 'confidence',
      render: (confidence: number) => (
        <div>
          <Progress percent={Math.round(confidence * 100)} size="small" />
        </div>
      ),
    },
    {
      title: 'Важность',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity: string) => (
        <Tag color={SEVERITY_COLORS[severity]}>{severity.toUpperCase()}</Tag>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2}>
            <AreaChartOutlined /> Аналитика
          </Title>
        </Col>
        <Col>
          <Space>
            <RangePicker onChange={handleDateRangeChange} />
            <Select
              defaultValue="7d"
              style={{ width: 120 }}
              onChange={handleTimeRangeChange}
            >
              <Option value="1d">1 день</Option>
              <Option value="7d">7 дней</Option>
              <Option value="30d">30 дней</Option>
              <Option value="90d">90 дней</Option>
            </Select>
          </Space>
        </Col>
      </Row>

      {/* Key Metrics */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={4}>
          <Card>
            <Statistic
              title="Всего камер"
              value={analyticsData?.totalCameras || 0}
              prefix={<VideoCameraOutlined />}
              suffix={`/ ${analyticsData?.activeCameras || 0} active`}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Всего событий"
              value={analyticsData?.totalEvents || 0}
              prefix={<AlertOutlined />}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Событий сегодня"
              value={analyticsData?.eventsToday || 0}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Оповещений сегодня"
              value={analyticsData?.alertsToday || 0}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Всего видео"
              value={analyticsData?.totalVideos || 0}
              prefix={<VideoCameraAddOutlined />}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Время работы системы"
              value={analyticsData?.systemUptime || '0%'}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {/* Charts Section */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={16}>
          <Card title="События во времени" style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={eventsByDay}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="events"
                  stroke="#1890ff"
                  activeDot={{ r: 8 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col span={8}>
          <Card title="События по типам" style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={eventsByType}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) =>
                    `${name} ${(percent * 100).toFixed(0)}%`
                  }
                  outerRadius={80}
                  fill="#884d8"
                  dataKey="value"
                >
                  {eventsByType.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={COLORS[index % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card title="События по часам" style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={eventsByHour}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="events" fill="#1890ff" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Распределение событий" style={{ height: 300 }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={eventsByType}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 20, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" />
                <Tooltip />
                <Legend />
                <Bar dataKey="value" fill="#8884d8" />
              </BarChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      {/* Recent Events */}
      <Row gutter={16}>
        <Col span={24}>
          <Card title="Последние события">
            <Table
              columns={eventColumns}
              dataSource={recentEvents}
              rowKey="id"
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Analytics;