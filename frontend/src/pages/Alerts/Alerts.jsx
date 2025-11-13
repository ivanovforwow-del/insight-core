import React, { useState } from 'react';
import {
  Card,
  Table,
  Typography,
  Space,
  Tag,
  Button,
  Modal,
  Select,
  DatePicker,
  Input,
  Badge,
  Row,
  Col,
  Statistic,
  Form,
} from 'antd';
import {
  BellOutlined,
  SendOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  FilterOutlined,
  SearchOutlined,
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
} from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import moment from 'moment';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;
const { TextArea } = Input;

const Alerts = () => {
  const [filterVisible, setFilterVisible] = useState(false);
  const [filters, setFilters] = useState({});
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [modalMode, setModalMode] = useState('create'); // 'create' or 'edit'
  const [selectedAlert, setSelectedAlert] = useState(null);
  const queryClient = useQueryClient();

  // Mock alerts data
  const { data: alerts, isLoading } = useQuery({
    queryKey: ['alerts', filters],
    queryFn: async () => [
      {
        id: 1,
        eventId: 1,
        channel: 'Telegram',
        message: 'Person detected in restricted area at Entrance Cam 1',
        status: 'sent',
        sentAt: '2023-12-01 10:30:20',
        event: {
          rule: 'Person in restricted area',
          camera: 'Entrance Cam 1',
          objectClass: 'Person',
          timestamp: '2023-12-01 10:30:15',
          severity: 'high',
        },
      },
      {
        id: 2,
        eventId: 2,
        channel: 'Email',
        message: 'Vehicle speed limit exceeded at Parking Cam 2',
        status: 'delivered',
        sentAt: '2023-12-01 10:28:45',
        event: {
          rule: 'Vehicle speed limit exceeded',
          camera: 'Parking Cam 2',
          objectClass: 'Car',
          timestamp: '2023-12-01 10:28:42',
          severity: 'medium',
        },
      },
      {
        id: 3,
        eventId: 3,
        channel: 'Webhook',
        message: 'Object left behind detected at Gate Cam 3',
        status: 'pending',
        sentAt: null,
        event: {
          rule: 'Object left behind',
          camera: 'Gate Cam 3',
          objectClass: 'Bag',
          timestamp: '2023-12-01 10:25:33',
          severity: 'high',
        },
      },
      {
        id: 4,
        eventId: 4,
        channel: 'Telegram',
        message: 'Line crossing detected at Warehouse Cam 1',
        status: 'failed',
        sentAt: '2023-12-01 10:22:20',
        error: 'Connection timeout',
        event: {
          rule: 'Line crossing',
          camera: 'Warehouse Cam 1',
          objectClass: 'Person',
          timestamp: '2023-12-01 10:22:18',
          severity: 'medium',
        },
      },
      {
        id: 5,
        eventId: 5,
        channel: 'Email',
        message: 'Loitering detection at Perimeter Cam 4',
        status: 'sent',
        sentAt: '2023-12-01 10:20:10',
        event: {
          rule: 'Loitering detection',
          camera: 'Perimeter Cam 4',
          objectClass: 'Person',
          timestamp: '2023-12-01 10:20:05',
          severity: 'low',
        },
      },
    ],
  });

  // Mock alert channels data
  const { data: channels } = useQuery({
    queryKey: ['alert-channels'],
    queryFn: async () => [
      { id: 1, name: 'Telegram Bot', type: 'telegram', enabled: true },
      { id: 2, name: 'Email Notifications', type: 'email', enabled: true },
      { id: 3, name: 'Webhook API', type: 'webhook', enabled: true },
      { id: 4, name: 'SMS Gateway', type: 'sms', enabled: false },
    ],
  });

  const [form] = Form.useForm();

  const statusColors = {
    pending: 'orange',
    sent: 'blue',
    failed: 'red',
    delivered: 'green',
  };

 const statusIcons = {
    pending: <ClockCircleOutlined />,
    sent: <SendOutlined />,
    failed: <DeleteOutlined />,
    delivered: <CheckCircleOutlined />,
  };

  const severityColors = {
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
      sorter: (a, b) => a.id - b.id,
    },
    {
      title: 'Event',
      key: 'event',
      render: (_, record) => (
        <div>
          <Text strong>{record.event.rule}</Text>
          <br />
          <Text type="secondary" style={{ fontSize: '12px' }}>
            {record.event.camera} • {record.event.objectClass}
          </Text>
        </div>
      ),
    },
    {
      title: 'Channel',
      dataIndex: 'channel',
      key: 'channel',
      render: (channel) => <Tag color="default">{channel}</Tag>,
      sorter: (a, b) => a.channel.localeCompare(b.channel),
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status) => (
        <Tag color={statusColors[status]} icon={statusIcons[status]}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </Tag>
      ),
      sorter: (a, b) => a.status.localeCompare(b.status),
      filters: [
        { text: 'Pending', value: 'pending' },
        { text: 'Sent', value: 'sent' },
        { text: 'Failed', value: 'failed' },
        { text: 'Delivered', value: 'delivered' },
      ],
      onFilter: (value, record) => record.status === value,
    },
    {
      title: 'Severity',
      key: 'severity',
      render: (_, record) => (
        <Tag color={severityColors[record.event.severity]}>
          {record.event.severity.toUpperCase()}
        </Tag>
      ),
      sorter: (a, b) => a.event.severity.localeCompare(b.event.severity),
    },
    {
      title: 'Sent At',
      dataIndex: 'sentAt',
      key: 'sentAt',
      render: (sentAt) => sentAt ? moment(sentAt).format('YYYY-MM-DD HH:mm:ss') : '-',
      sorter: (a, b) => moment(a.sentAt).diff(moment(b.sentAt)),
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            View
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          >
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  const handleEdit = (alert) => {
    setSelectedAlert(alert);
    setModalMode('edit');
    form.setFieldsValue({
      channel: alert.channel,
      message: alert.message,
    });
    setIsModalVisible(true);
  };

 const handleDelete = (id) => {
    Modal.confirm({
      title: 'Delete Alert',
      content: 'Are you sure you want to delete this alert?',
      onOk: () => {
        console.log('Delete alert:', id);
        queryClient.invalidateQueries(['alerts']);
      },
    });
  };

  const handleCreateAlert = () => {
    setModalMode('create');
    setSelectedAlert(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  const handleResend = (alertId) => {
    Modal.confirm({
      title: 'Resend Alert',
      content: 'Are you sure you want to resend this alert?',
      onOk: () => {
        console.log('Resend alert:', alertId);
        queryClient.invalidateQueries(['alerts']);
      },
    });
  };

 const handleOk = () => {
    form.validateFields().then((values) => {
      if (modalMode === 'create') {
        console.log('Create alert:', values);
      } else {
        console.log('Update alert:', { ...selectedAlert, ...values });
      }
      setIsModalVisible(false);
      queryClient.invalidateQueries(['alerts']);
    });
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setSelectedAlert(null);
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

  const handleFilterChange = (changedValues) => {
    setFilters({ ...filters, ...changedValues });
  };

  // Statistics data
 const totalAlerts = alerts?.length || 0;
  const sentAlerts = alerts?.filter(alert => alert.status === 'sent' || alert.status === 'delivered').length || 0;
  const failedAlerts = alerts?.filter(alert => alert.status === 'failed').length || 0;
  const pendingAlerts = alerts?.filter(alert => alert.status === 'pending').length || 0;

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2}>
            <BellOutlined /> Alerts
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
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={handleCreateAlert}
            >
              Create Alert
            </Button>
          </Space>
        </Col>
      </Row>

      {/* Statistics Cards */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Alerts"
              value={totalAlerts}
              prefix={<BellOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Sent Alerts"
              value={sentAlerts}
              prefix={<SendOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Failed Alerts"
              value={failedAlerts}
              prefix={<DeleteOutlined />}
              valueStyle={{ color: '#ff4d4f' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Pending Alerts"
              value={pendingAlerts}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      {filterVisible && (
        <Card style={{ marginBottom: 24 }}>
          <Row gutter={16}>
            <Col span={6}>
              <Select
                style={{ width: '100%' }}
                placeholder="Filter by channel"
                onChange={(value) => handleFilterChange({ channel: value })}
                allowClear
              >
                <Option value="Telegram">Telegram</Option>
                <Option value="Email">Email</Option>
                <Option value="Webhook">Webhook</Option>
              </Select>
            </Col>
            <Col span={6}>
              <Select
                style={{ width: '100%' }}
                placeholder="Filter by status"
                onChange={(value) => handleFilterChange({ status: value })}
                allowClear
              >
                <Option value="pending">Pending</Option>
                <Option value="sent">Sent</Option>
                <Option value="failed">Failed</Option>
                <Option value="delivered">Delivered</Option>
              </Select>
            </Col>
            <Col span={6}>
              <Select
                style={{ width: '100%' }}
                placeholder="Filter by severity"
                onChange={(value) => handleFilterChange({ severity: value })}
                allowClear
              >
                <Option value="low">Low</Option>
                <Option value="medium">Medium</Option>
                <Option value="high">High</Option>
                <Option value="critical">Critical</Option>
              </Select>
            </Col>
            <Col span={6}>
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
          dataSource={alerts || []}
          loading={isLoading}
          rowKey="id"
          pagination={{ pageSize: 15 }}
          scroll={{ x: 1000 }}
        />
      </Card>

      <Modal
        title={modalMode === 'create' ? 'Create Alert' : 'Edit Alert'}
        open={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        width={600}
        footer={[
          <Button key="back" onClick={handleCancel}>
            Cancel
          </Button>,
          modalMode === 'edit' && (
            <Button
              key="resend"
              onClick={() => handleResend(selectedAlert?.id)}
              type="primary"
            >
              Resend
            </Button>
          ),
          <Button key="submit" type="primary" onClick={handleOk}>
            {modalMode === 'create' ? 'Create' : 'Update'}
          </Button>,
        ]}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{
            channel: selectedAlert?.channel || '',
            message: selectedAlert?.message || '',
          }}
        >
          <Form.Item
            name="channel"
            label="Channel"
            rules={[{ required: true, message: 'Please select a channel!' }]}
          >
            <Select placeholder="Select alert channel">
              {channels?.map((channel) => (
                <Option key={channel.id} value={channel.name}>
                  {channel.name} ({channel.type})
                </Option>
              ))}
            </Select>
          </Form.Item>

          <Form.Item
            name="message"
            label="Message"
            rules={[{ required: true, message: 'Please enter a message!' }]}
          >
            <TextArea
              rows={4}
              placeholder="Enter alert message"
              disabled={modalMode === 'edit'}
            />
          </Form.Item>

          {selectedAlert && modalMode === 'edit' && (
            <div>
              <Text strong>Event Details:</Text>
              <br />
              <Text type="secondary">
                Rule: {selectedAlert.event.rule}
              </Text>
              <br />
              <Text type="secondary">
                Camera: {selectedAlert.event.camera}
              </Text>
              <br />
              <Text type="secondary">
                Object: {selectedAlert.event.objectClass}
              </Text>
              <br />
              <Text type="secondary">
                Timestamp: {moment(selectedAlert.event.timestamp).format('YYYY-MM-DD HH:mm:ss')}
              </Text>
              <br />
              <Text type="secondary">
                Severity: {selectedAlert.event.severity.toUpperCase()}
              </Text>
            </div>
          )}
        </Form>
      </Modal>
    </div>
  );
};

export default Alerts;