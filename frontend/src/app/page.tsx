'use client';

import React from 'react';
import { App as AntdApp, Card, Row, Col, Statistic, Space, Typography, Tag } from 'antd';
import { 
 VideoCameraOutlined, 
  AlertOutlined, 
  CheckCircleOutlined, 
  ClockCircleOutlined,
  EyeOutlined,
  UserOutlined,
  CarOutlined,
  VideoCameraAddOutlined,
  DashboardOutlined
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { AnalyticsData, EventByType, EventByHour, Event } from '@/types';
import { useCameras } from '@/hooks/data/useCameraData';
import { useEvents } from '@/hooks/data/useEventData';
import { useAlerts } from '@/hooks/data/useAlertData';

const { Title, Text } = Typography;

// Данные для графиков для тестирования - в реальном приложении они будут из хуков
const eventsByType: EventByType[] = [
  { name: 'Person', value: 56 },
  { name: 'Vehicle', value: 32 },
  { name: 'Car', value: 28 },
  { name: 'Truck', value: 12 },
  { name: 'Bicycle', value: 8 },
];

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

const COLORS = ['#008FE', '#0C49F', '#FFBB28', '#FF8042', '#8884D8'];

const severityColors: Record<string, string> = {
  low: 'green',
  medium: 'orange',
  high: 'red',
  critical: 'red',
};

const DashboardPage = () => {
  // Использование новых хуков вместо тестовых данных
  const { data: cameras, isLoading: camerasLoading } = useCameras();
  const { data: events, isLoading: eventsLoading } = useEvents({ limit: 5 });
  const { data: alerts, isLoading: alertsLoading } = useAlerts({ limit: 5 });

  // Статистика панели управления для тестирования - в реальном приложении будет из API
  const { data: stats } = useQuery<AnalyticsData>({
    queryKey: ['dashboard-stats'],
    queryFn: async () => ({
      totalCameras: cameras?.length || 0,
      activeCameras: cameras?.filter(c => c.status === 'active').length || 0,
      totalEvents: events?.total || 0,
      eventsToday: 24,
      alertsToday: alerts?.total || 0,
      totalVideos: 156,
      processingTime: '2.3s',
      systemUptime: '99.9%',
    }),
  });

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
      title: 'Важность',
      dataIndex: 'severity',
      key: 'severity',
      render: (severity: string) => (
        <Tag color={severityColors[severity]}>{severity.toUpperCase()}</Tag>
      ),
    },
  ];

  return (
    <div style={{ padding: '24px' }}>
      <Title level={2}>
        <DashboardOutlined /> Панель управления
      </Title>
      
      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Всего камер"
              value={stats?.totalCameras || 0}
              prefix={<VideoCameraOutlined />}
              suffix={`/ ${stats?.activeCameras || 0} active`}
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
              title="Оповещений сегодня"
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
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
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
            <div>
              {events?.data && events.data.length > 0 ? (
                <div>
                  {events.data.map((event) => (
                    <div key={event.id} style={{ padding: '8px 0', borderBottom: '1px solid #f0f0' }}>
                      <Text strong>ID: {event.id}</Text> - 
                      <Text> {event.cameraName}</Text> - 
                      <Text> {event.objectType}</Text> - 
                      <Text> {event.timestamp}</Text> - 
                      <Tag color={severityColors[event.severity]}>{event.severity.toUpperCase()}</Tag>
                    </div>
                  ))}
                </div>
              ) : (
                <Text>Нет последних событий</Text>
              )}
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default DashboardPage;