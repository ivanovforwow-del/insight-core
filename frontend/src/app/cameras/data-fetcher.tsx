'use client';

import React, { useState } from 'react';
import {
  Card,
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
  notification,
  Row,
  Col,
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
import { Camera } from '@/types';
import { useCameras, useCreateCamera, useUpdateCamera, useDeleteCamera, useUpdateCameraStatus } from '@/hooks/data/useCameraData';

const { Title } = Typography;
const { Option } = Select;

interface CamerasDataFetcherProps {
  initialFilters?: Record<string, any>;
}

const CamerasDataFetcher: React.FC<CamerasDataFetcherProps> = ({ initialFilters = {} }) => {
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [editingCamera, setEditingCamera] = useState<Camera | null>(null);
  const [form] = Form.useForm();

  const { data: cameras = [], isLoading } = useCameras();
  const createCameraMutation = useCreateCamera();
  const updateCameraMutation = useUpdateCamera();
  const deleteCameraMutation = useDeleteCamera();
  const updateCameraStatusMutation = useUpdateCameraStatus();

  const statusColors: Record<string, string> = {
    active: 'green',
    inactive: 'default',
    error: 'red',
    maintenance: 'orange',
  };

  const statusIcons: Record<string, React.ReactNode> = {
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
      sorter: (a: Camera, b: Camera) => a.name.localeCompare(b.name),
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
      render: (status: string) => (
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
      onFilter: (value: boolean | React.Key, record: Camera) => record.status === String(value),
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
      sorter: (a: Camera, b: Camera) => a.zones - b.zones,
    },
    {
      title: 'Lines',
      dataIndex: 'lines',
      key: 'lines',
      sorter: (a: Camera, b: Camera) => a.lines - b.lines,
    },
    {
      title: 'Rules',
      dataIndex: 'rules',
      key: 'rules',
      sorter: (a: Camera, b: Camera) => a.rules - b.rules,
    },
    {
      title: 'Actions',
      key: 'actions',
      render: (_: any, record: Camera) => (
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
            loading={deleteCameraMutation.isPending && deleteCameraMutation.variables === record.id}
          >
            Delete
          </Button>
        </Space>
      ),
    },
  ];

  const handleViewStream = (camera: Camera) => {
    // Open stream in modal or new tab
    console.log('View stream for:', camera);
  };

  const handleEdit = (camera: Camera) => {
    setEditingCamera(camera);
    form.setFieldsValue({
      name: camera.name,
      rtspUrl: camera.rtspUrl,
      location: camera.location,
      status: camera.status,
      vendor: camera.vendor,
      enabled: camera.enabled,
    });
    setIsModalVisible(true);
  };

  const handleDelete = (id: number) => {
    Modal.confirm({
      title: 'Delete Camera',
      content: 'Are you sure you want to delete this camera?',
      onOk: () => {
        deleteCameraMutation.mutate(id);
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
        updateCameraMutation.mutate({
          id: editingCamera.id,
          data: values,
        });
      } else {
        createCameraMutation.mutate(values);
      }
      setIsModalVisible(false);
    });
  };

  const handleCancel = () => {
    setIsModalVisible(false);
    setEditingCamera(null);
  };

  const handleStatusToggle = (id: number, enabled: boolean) => {
    updateCameraStatusMutation.mutate({ id, enabled });
  };

  return (
    <div style={{ padding: '24px' }}>
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
            loading={createCameraMutation.isPending}
          >
            Add Camera
          </Button>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={cameras}
          loading={isLoading || createCameraMutation.isPending || updateCameraMutation.isPending || deleteCameraMutation.isPending}
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
        confirmLoading={editingCamera ? updateCameraMutation.isPending : createCameraMutation.isPending}
      >
        <Form
          form={form}
          layout="vertical"
          initialValues={{ status: 'active', enabled: true }}
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

export default CamerasDataFetcher;