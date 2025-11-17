import React from 'react';
import { Card, Row, Col, Statistic, Table, Typography, Space, Tag, Progress } from 'antd';
import { 
  VideoCameraOutlined, 
  AlertOutlined, 
  CheckCircleOutlined, 
  ClockCircleOutlined,
  EyeOutlined,
  UserOutlined,
  CarOutlined,
  VideoCameraAddOutlined
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { AnalyticsData, EventByType, EventByHour, Event } from '../../types';

const Dashboard = () => {
  // Статистика панели управления для тестирования
  const { data: stats } = useQuery<AnalyticsData>({
    queryKey: ['dashboard-stats'],
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

  // Последние события для тестирования
  const { data: recentEvents = [] } = useQuery<Event[]>({
    queryKey: ['recent-events'],
    queryFn: async () => [
      { id: 1, cameraId: 1, cameraName: 'Камера 1 (вход)', objectType: 'Человек', timestamp: '2023-12-01 10:30:15', confidence: 0.95, severity: 'high' },
      { id: 2, cameraId: 2, cameraName: 'Камера 2 (парковка)', objectType: 'Автомобиль', timestamp: '2023-12-01 10:28:42', confidence: 0.87, severity: 'medium' },
      { id: 3, cameraId: 3, cameraName: 'Камера 3 (ворота)', objectType: 'Грузовик', timestamp: '2023-12-01 10:25:33', confidence: 0.92, severity: 'low' },
      { id: 4, cameraId: 4, cameraName: 'Камера 1 (склад)', objectType: 'Человек', timestamp: '2023-12-01 10:2:18', confidence: 0.89, severity: 'high' },
      { id: 5, cameraId: 5, cameraName: 'Камера 4 (периметр)', objectType: 'Транспорт', timestamp: '2023-12-01 10:20:05', confidence: 0.78, severity: 'medium' },
    ],
  });

  // Mock events by type
 const eventsByType: EventByType[] = [
    { name: 'Человек', value: 56 },
    { name: 'Транспорт', value: 32 },
    { name: 'Автомобиль', value: 28 },
    { name: 'Грузовик', value: 12 },
    { name: 'Велосипед', value: 8 },
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
    { hour: '10:00', events: 2 },
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

  const COLORS = ['#0088FE', '#0C49F', '#FFBB28', '#FF8042', '#8884D8'];

  const severityColors: Record<string, string> = {
    low: 'green',
    medium: 'orange',
    high: 'red',
    critical: 'red',
  };

  const columns = [
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
          {text === 'Человек' && <UserOutlined />}
          {text === 'Автомобиль' && <CarOutlined />}
          {text === 'Грузовик' && <CarOutlined />}
          {text === 'Транспорт' && <CarOutlined />}
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
        <Tag color={severityColors[severity]}>{severity.toUpperCase()}</Tag>
      ),
    },
  ];

  return (
    <div>
      <Typography.Title level={2}>Панель управления</Typography.Title>
      
      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Всего камер"
              value={stats?.totalCameras || 0}
              prefix={<VideoCameraOutlined />}
              suffix={`/ ${stats?.activeCameras || 0} активных`}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Всего событий"
              value={stats?.totalEvents || 0}
              prefix={<AlertOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Событий сегодня"
              value={stats?.eventsToday || 0}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Уведомлений сегодня"
              value={stats?.alertsToday || 0}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={16}>
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
        <Col span={8}>
          <Card title="События по типам" style={{ height: 300 }}>
            <ResponsiveContainer width="10%" height="100%">
              <PieChart>
                <Pie
                  data={eventsByType}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percent }) => `${name} ${(percent * 10).toFixed(0)}%`}
                  outerRadius={80}
                  fill="#884d8"
                  dataKey="value"
                >
                  {eventsByType.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={24}>
          <Card title="Последние события">
            <Table 
              columns={columns} 
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

export default Dashboard;