import React from 'react';
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
  notification,
} from 'antd';
import {
  AlertOutlined,
  EyeOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  FilterOutlined,
  SearchOutlined,
  DownloadOutlined,
  CloseCircleOutlined,
  InfoCircleOutlined,
} from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import moment from 'moment';
import { Alert } from '../../types';

const { Title } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const Alerts = () => {
  const [filterVisible, setFilterVisible] = React.useState(false);
  const [filters, setFilters] = React.useState<Record<string, any>>({});
  const [selectedAlert, setSelectedAlert] = React.useState<Alert | null>(null);
  const queryClient = useQueryClient();

  // Mock alerts data
  const { data: alerts = [], isLoading } = useQuery<Alert[]>({
    queryKey: ['alerts', filters],
    queryFn: async () => [
      {
        id: 1,
        title: 'High Severity Alert',
        message: 'Motion detected in restricted area',
        type: 'error',
        timestamp: '2023-12-01 10:30:15',
        read: false,
        eventId: 1,
      },
      {
        id: 2,
        title: 'Camera Offline',
        message: 'Camera "Entrance Cam 1" is offline',
        type: 'warning',
        timestamp: '2023-12-01 10:28:42',
        read: true,
        eventId: undefined,
      },
      {
        id: 3,
        title: 'System Maintenance',
        message: 'Scheduled maintenance in 2 hours',
        type: 'info',
        timestamp: '2023-12-01 10:25:33',
        read: false,
        eventId: undefined,
      },
      {
        id: 4,
        title: 'Low Severity Alert',
        message: 'Unusual activity detected',
        type: 'warning',
        timestamp: '2023-12-01 10:22:18',
        read: false,
        eventId: 2,
      },
      {
        id: 5,
        title: 'Critical Alert',
        message: 'Multiple cameras offline',
        type: 'error',
        timestamp: '2023-12-01 10:20:05',
        read: true,
        eventId: undefined,
      },
    ],
  });

  const markAsReadMutation = useMutation({
    mutationFn: async (alertId: number) => {
      // API call to mark alert as read
      console.log('Marking alert as read:', alertId);
      return { id: alertId, read: true };
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
    },
  });

  const clearAllMutation = useMutation({
    mutationFn: async () => {
      // API call to clear all alerts
      console.log('Clearing all alerts');
      return true;
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['alerts'] });
      notification.success({
        message: 'Success',
        description: 'All alerts cleared',
      });
    },
  });

  const typeColors: Record<string, string> = {
    info: 'blue',
    warning: 'orange',
    error: 'red',
    success: 'green',
  };

  const typeIcons: Record<string, React.ReactNode> = {
    info: <InfoCircleOutlined />,
    warning: <AlertOutlined />,
    error: <CloseCircleOutlined />,
    success: <CheckCircleOutlined />,
  };

  const columns = [
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      sorter: (a: Alert, b: Alert) => a.id - b.id,
    },
    {
      title: 'Title',
      dataIndex: 'title',
      key: 'title',
      sorter: (a: Alert, b: Alert) => a.title.localeCompare(b.title),
    },
    {
      title: 'Message',
      dataIndex: 'message',
      key: 'message',
    },
    {
      title: 'Type',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => (
        <Tag color={typeColors[type]} icon={typeIcons[type]}>
          {type.toUpperCase()}
        </Tag>
      ),
      sorter: (a: Alert, b: Alert) => a.type.localeCompare(b.type),
      filters: [
        { text: 'Info', value: 'info' },
        { text: 'Warning', value: 'warning' },
        { text: 'Error', value: 'error' },
        { text: 'Success', value: 'success' },
      ],
      onFilter: (value: boolean | React.Key, record: Alert) => record.type === value,
    },
    {
      title: 'Timestamp',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: (a: Alert, b: Alert) => moment(a.timestamp).diff(moment(b.timestamp)),
    },
    {
      title: 'Status',
      key: 'read',
      render: (_: any, record: Alert) => (
        <Badge
          status={record.read ? 'success' : 'error'}
          text={record.read ? 'Read' : 'Unread'}
        />
      ),
      filters: [
        { text: 'Read', value: true },
        { text: 'Unread', value: false },
      ],
      onFilter: (value: boolean | React.Key, record: Alert) => record.read === value,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Alert) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => setSelectedAlert(record)}
          >
            View
          </Button>
          {!record.read && (
            <Button
              type="link"
              icon={<CheckCircleOutlined />}
              onClick={() => markAsReadMutation.mutate(record.id)}
              loading={markAsReadMutation.isPending}
            >
              Mark Read
            </Button>
          )}
          <Button
            type="link"
            icon={<DownloadOutlined />}
            onClick={() => console.log('Download alert details:', record)}
          >
            Export
          </Button>
        </Space>
      ),
    },
  ];

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

  const handleClearAll = () => {
    Modal.confirm({
      title: 'Clear All Alerts',
      content: 'Are you sure you want to clear all alerts?',
      onOk: () => clearAllMutation.mutate(),
    });
  };

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2}>
            <AlertOutlined /> Alerts
          </Title>
        </Col>
        <Col>
          <Space>
            <Button
              danger
              onClick={handleClearAll}
              loading={clearAllMutation.isPending}
            >
              Clear All
            </Button>
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
                placeholder="Filter by type"
                onChange={(value) => handleFilterChange({ type: value })}
                allowClear
              >
                <Option value="info">Info</Option>
                <Option value="warning">Warning</Option>
                <Option value="error">Error</Option>
                <Option value="success">Success</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Select
                style={{ width: '100%' }}
                placeholder="Filter by status"
                onChange={(value) => handleFilterChange({ read: value })}
                allowClear
              >
                <Option value={true}>Read</Option>
                <Option value={false}>Unread</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Input
                placeholder="Search alerts..."
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
          dataSource={alerts}
          loading={isLoading || markAsReadMutation.isPending}
          rowKey="id"
          pagination={{ pageSize: 15 }}
          scroll={{ x: 1200 }}
        />
      </Card>

      <Modal
        title="Alert Details"
        open={!!selectedAlert}
        onCancel={() => setSelectedAlert(null)}
        footer={[
          <Button key="close" onClick={() => setSelectedAlert(null)}>
            Close
          </Button>,
        ]}
      >
        {selectedAlert && (
          <div>
            <Typography.Title level={4}>{selectedAlert.title}</Typography.Title>
            <Typography.Paragraph>
              <strong>Message:</strong> {selectedAlert.message}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Type:</strong> {selectedAlert.type.toUpperCase()}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Timestamp:</strong> {selectedAlert.timestamp}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Status:</strong> {selectedAlert.read ? 'Read' : 'Unread'}
            </Typography.Paragraph>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Alerts;