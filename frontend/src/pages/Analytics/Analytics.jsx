import React, { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Typography,
  Space,
  Select,
  DatePicker,
  Button,
  Tabs,
  Statistic,
  Table,
  Tag,
  Progress,
  Badge,
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
  BarChartOutlined,
  LineChartOutlined,
  PieChartOutlined,
  CalendarOutlined,
  ClockCircleOutlined,
  AlertOutlined,
  VideoCameraOutlined,
  UserOutlined,
  CarOutlined,
  CheckCircleOutlined,
} from '@ant-design/icons';
import { useQuery } from '@tanstack/react-query';
import moment from 'moment';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { TabPane } = Tabs;
const { Option } = Select;

const Analytics = () => {
  const [dateRange, setDateRange] = useState([
    moment().subtract(7, 'days'),
    moment(),
  ]);
  const [selectedCamera, setSelectedCamera] = useState('all');

  // Mock analytics data
  const { data: analyticsData } = useQuery({
    queryKey: ['analytics', dateRange, selectedCamera],
    queryFn: async () => ({
      totalEvents: 128,
      totalAlerts: 24,
      totalVideos: 156,
      processingTime: 2.3,
      accuracy: 0.92,
      eventsByDay: [
        { date: '2023-11-25', events: 15, alerts: 3 },
        { date: '2023-11-26', events: 18, alerts: 2 },
        { date: '2023-11-27', events: 22, alerts: 5 },
        { date: '2023-11-28', events: 12, alerts: 1 },
        { date: '2023-11-29', events: 25, alerts: 4 },
        { date: '2023-11-30', events: 20, alerts: 3 },
        { date: '2023-12-01', events: 16, alerts: 6 },
      ],
      eventsByHour: [
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
      ],
      eventsByType: [
        { name: 'Person', value: 56 },
        { name: 'Vehicle', value: 32 },
        { name: 'Car', value: 28 },
        { name: 'Truck', value: 12 },
        { name: 'Bicycle', value: 8 },
      ],
      eventsByCamera: [
        { name: 'Entrance Cam 1', events: 45 },
        { name: 'Parking Cam 2', events: 32 },
        { name: 'Gate Cam 3', events: 28 },
        { name: 'Warehouse Cam 1', events: 23 },
      ],
      topRules: [
        { name: 'Person in restricted area', count: 32 },
        { name: 'Line crossing', count: 28 },
        { name: 'Vehicle speed limit', count: 18 },
        { name: 'Object left behind', count: 15 },
        { name: 'Loitering detection', count: 12 },
      ],
      accuracyByClass: [
        { name: 'Person', accuracy: 0.95 },
        { name: 'Car', accuracy: 0.92 },
        { name: 'Truck', accuracy: 0.89 },
        { name: 'Bicycle', accuracy: 0.85 },
        { name: 'Bag', accuracy: 0.91 },
      ],
    }),
  });

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#884D8'];
  const CAMERA_COLORS = ['#775DD0', '#00B894', '#FDCB6E', '#E17055'];

  const handleDateChange = (dates) => {
    setDateRange(dates);
 };

  const handleCameraChange = (value) => {
    setSelectedCamera(value);
  };

  const renderCustomBarLabel = (props) => {
    const { x, y, width, value } = props;
    return (
      <text x={x + width / 2} y={y - 10} fill="#666" textAnchor="middle" fontSize={12}>
        {value}
      </text>
    );
  };

  const topRulesColumns = [
    {
      title: 'Rule Name',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Count',
      dataIndex: 'count',
      key: 'count',
      sorter: (a, b) => a.count - b.count,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: () => (
        <Button type="link" size="small">
          View Details
        </Button>
      ),
    },
  ];

  const accuracyColumns = [
    {
      title: 'Object Class',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Accuracy',
      dataIndex: 'accuracy',
      key: 'accuracy',
      render: (accuracy) => (
        <Space>
          <Progress percent={Math.round(accuracy * 100)} size="small" />
          <Text>{(accuracy * 10).toFixed(1)}%</Text>
        </Space>
      ),
      sorter: (a, b) => a.accuracy - b.accuracy,
    },
  ];

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2}>
            <BarChartOutlined /> Analytics
          </Title>
        </Col>
        <Col>
          <Space>
            <Select
              defaultValue="all"
              style={{ width: 200 }}
              onChange={handleCameraChange}
            >
              <Option value="all">All Cameras</Option>
              <Option value="Entrance Cam 1">Entrance Cam 1</Option>
              <Option value="Parking Cam 2">Parking Cam 2</Option>
              <Option value="Gate Cam 3">Gate Cam 3</Option>
              <Option value="Warehouse Cam 1">Warehouse Cam 1</Option>
            </Select>
            <RangePicker
              value={dateRange}
              onChange={handleDateChange}
              style={{ width: 280 }}
              suffixIcon={<CalendarOutlined />}
            />
          </Space>
        </Col>
      </Row>

      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={4}>
          <Card>
            <Statistic
              title="Total Events"
              value={analyticsData?.totalEvents || 0}
              prefix={<AlertOutlined />}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Total Alerts"
              value={analyticsData?.totalAlerts || 0}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Videos Processed"
              value={analyticsData?.totalVideos || 0}
              prefix={<VideoCameraOutlined />}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Avg Processing"
              value={analyticsData?.processingTime || 0}
              suffix="s"
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Accuracy"
              value={analyticsData?.accuracy ? (analyticsData.accuracy * 100).toFixed(1) : 0}
              suffix="%"
              precision={1}
            />
          </Card>
        </Col>
        <Col span={4}>
          <Card>
            <Statistic
              title="Success Rate"
              value={95.2}
              suffix="%"
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="overview" style={{ marginBottom: 24 }}>
        <TabPane tab="Overview" key="overview">
          <Row gutter={16} style={{ marginBottom: 24 }}>
            <Col span={16}>
              <Card title="Events by Day">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={analyticsData?.eventsByDay || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="events" fill="#1890ff" name="Events" />
                    <Bar dataKey="alerts" fill="#f5222d" name="Alerts" />
                  </BarChart>
                </ResponsiveContainer>
              </Card>
            </Col>
            <Col span={8}>
              <Card title="Events by Type">
                <ResponsiveContainer width="10%" height={300}>
                  <PieChart>
                    <Pie
                      data={analyticsData?.eventsByType || []}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent }) => `${name} ${(percent * 10).toFixed(0)}%`}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                    >
                      {analyticsData?.eventsByType?.map((entry, index) => (
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
            <Col span={12}>
              <Card title="Events by Hour">
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={analyticsData?.eventsByHour || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hour" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="events" fill="#52c41a" />
                  </BarChart>
                </ResponsiveContainer>
              </Card>
            </Col>
            <Col span={12}>
              <Card title="Events by Camera">
                <ResponsiveContainer width="10%" height={300}>
                  <BarChart data={analyticsData?.eventsByCamera || []}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="events" fill="#722ed1">
                      {analyticsData?.eventsByCamera?.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={CAMERA_COLORS[index % CAMERA_COLORS.length]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Rules Performance" key="rules">
          <Row gutter={16}>
            <Col span={16}>
              <Card title="Top Rules">
                <Table
                  columns={topRulesColumns}
                  dataSource={analyticsData?.topRules || []}
                  rowKey="name"
                  pagination={{ pageSize: 10 }}
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card title="Model Accuracy by Class">
                <Table
                  columns={accuracyColumns}
                  dataSource={analyticsData?.accuracyByClass || []}
                  rowKey="name"
                  pagination={false}
                  size="small"
                />
              </Card>
            </Col>
          </Row>
        </TabPane>

        <TabPane tab="Time Series" key="timeseries">
          <Card title="Events Timeline">
            <ResponsiveContainer width="10%" height={400}>
              <LineChart data={analyticsData?.eventsByHour || []}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="hour" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="events" stroke="#1890ff" activeDot={{ r: 8 }} />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default Analytics;