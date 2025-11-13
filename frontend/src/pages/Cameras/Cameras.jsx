import React, { useState } from 'react';
import {
  Card,
  Row,
  Col,
  Table,
  Typography,
  Space,
  Tag,
  Button,
  Modal,
  Form,
  Input,
  Select,
  InputNumber,
  Switch,
} from 'antd';
import {
  VideoCameraOutlined,
  PlusOutlined,
  EditOutlined,
  DeleteOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined,
  WarningOutlined,
  SyncOutlined,
} from '@ant-design/icons';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';

const { Title } = Typography;
const { Option } = Select;

const Cameras = () => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingCamera, setEditingCamera] = useState(null);
  const queryClient = useQueryClient();

  // Mock cameras data
  const { data: cameras, isLoading } = useQuery({
    queryKey: ['cameras'],
    queryFn: async () => [
      {
        id: 1,
        name: 'Entrance Cam 1',
        rtspUrl: 'rtsp://192.168.1.100:554/stream1',
        location: 'Main Entrance',
        status: 'active',
        vendor: 'Hikvision',
        streamSettings: { fps: 30, resolution: '1920x1080' },
        zones: 3,
        lines: 2,
        rules: 5,
      },
      {
        id: 2,
        name: 'Parking Cam 2',
        rtspUrl: 'rtsp://192.168.1.101:554/stream1',
        location: 'Parking Area',
        status: 'active',
        vendor: 'Dahua',
        streamSettings: { fps: 25, resolution: '1280x720' },
        zones: 2,
        lines: 1,
        rules: 3,
      },
      {
        id: 3,
        name: 'Gate Cam 3',
        rtspUrl: 'rtsp://192.168.1.102:554/stream1',
        location: 'Main Gate',
        status: 'inactive',
        vendor: 'Axis',
        streamSettings: { fps: 30, resolution: '1920x1080' },
        zones: 1,
        lines: 0,
        rules: 2,
      },
      {
        id: 4,
        name: 'Warehouse Cam 1',
        rtspUrl: 'rtsp://192.168.1.103:554/stream1',
        location: 'Warehouse',
        status: 'error',
        vendor: 'Bosch',
        streamSettings: { fps: 20, resolution: '1280x720' },
        zones: 4,
        lines: 3,
        rules: 6,
      },
    ],
  });

  const [form] = Form.useForm();

  const statusColors = {
    active: 'green',
    inactive: 'default',
    error: 'red',
    maintenance: 'orange',
  };

  const statusIcons = {
    active: <CheckCircleOutlined />,
    inactive: <CloseCircleOutlined />,
    error: <WarningOutlined />,
    maintenance: <SyncOutlined />,
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      sorter: (a, b) => a.name.localeCompare(b.name),
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
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
      filters: [
        { text: 'Active', value: 'active' },
        { text: 'Inactive', value: 'inactive' },
        { text: 'Error', value: 'error' },
        { text: 'Maintenance', value: 'maintenance' },
      ],
      onFilter: (value, record) => record.status === value,
    },
    {
      title: 'Vendor',
      dataIndex: 'vendor',
      key: 'vendor',
    },
    {
      title: 'Zones',
      dataIndex: 'zones',
      key: 'zones',
      sorter: (a, b) => a.zones - b.zones,
    },
    {
      title: 'Lines',
      dataIndex: 'lines',
      key: 'lines',
      sorter: (a, b) => a.lines - b.lines,
    },
    {
      title: 'Rules',
      dataIndex: 'rules',
      key: 'rules',
      sorter: (a, b) => a.rules - b.rules,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_, record) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<VideoCameraOutlined />}
            onClick={() => handleViewStream(record)}
          >
            Stream
          </Button>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Edit
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

  const handleViewStream = (camera) => {
    // Open stream in modal or new tab
    console.log('View stream for:', camera);
  };

  const handleEdit = (camera) => {
    setEditingCamera(camera);
    form.setFieldsValue({
      name: camera.name,
      rtspUrl: camera.rtspUrl,
      location: camera.location,
      status: camera.status,
      vendor: camera.vendor,
    });
    setIsModalVisible(true);
  };

  const handleDelete = (id) => {
    Modal.confirm({
      title: 'Delete Camera',
      content: 'Are you sure you want to delete this camera?',
      onOk: () => {
        // Delete camera mutation
        console.log('Delete camera:', id);
        queryClient.invalidateQueries(['cameras']);
      },
    });
 };

  const handleAddCamera = () => {
    setEditingCamera(null);
    form.resetFields();
    setIsModalVisible(true);
  };

  const handleOk = () => {
    form.validateFields().then((values) => {
      if (editingCamera) {
        // Update camera mutation
        console.log('Update camera:', { ...editingCamera, ...values });
      } else {
        // Create camera mutation
        console.log('Create camera:', values);
      }
      setIsModalVisible(false);
      queryClient.invalidateQueries(['cameras']);
    });
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setEditingCamera(null);
  };

  return (
    <div>
      <Row justify="space-between" align="middle" style={{ marginBottom: 24 }}>
        <Col>
          <Title level={2}>
            <VideoCameraOutlined /> Cameras
          </Title>
        </Col>
        <Col>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleAddCamera}
          >
            Add Camera
          </Button>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={cameras || []}
          loading={isLoading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title={editingCamera ? 'Edit Camera' : 'Add Camera'}
        open={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{ status: 'active' }}
        >
          <Form.Item
            name="name"
            label="Camera Name"
            rules={[{ required: true, message: 'Please input camera name!' }]}
          >
            <Input placeholder="Enter camera name" />
          </Form.Item>

          <Form.Item
            name="rtspUrl"
            label="RTSP URL"
            rules={[{ required: true, message: 'Please input RTSP URL!' }]}
          >
            <Input placeholder="rtsp://example.com/stream" />
          </Form.Item>

          <Form.Item
            name="location"
            label="Location"
            rules={[{ required: true, message: 'Please input location!' }]}
          >
            <Input placeholder="Enter location" />
          </Form.Item>

          <Form.Item
            name="status"
            label="Status"
            rules={[{ required: true, message: 'Please select status!' }]}
          >
            <Select placeholder="Select status">
              <Option value="active">Active</Option>
              <Option value="inactive">Inactive</Option>
              <Option value="error">Error</Option>
              <Option value="maintenance">Maintenance</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="vendor"
            label="Vendor"
            rules={[{ required: true, message: 'Please select vendor!' }]}
          >
            <Select placeholder="Select vendor">
              <Option value="Hikvision">Hikvision</Option>
              <Option value="Dahua">Dahua</Option>
              <Option value="Axis">Axis</Option>
              <Option value="Bosch">Bosch</Option>
              <Option value="Samsung">Samsung</Option>
              <Option value="Other">Other</Option>
            </Select>
          </Form.Item>

          <Form.Item name="enabled" label="Enabled" valuePropName="checked">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default Cameras;