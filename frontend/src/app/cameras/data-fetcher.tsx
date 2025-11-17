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
      title: 'Имя',
      dataIndex: 'name',
      key: 'name',
      sorter: (a: Camera, b: Camera) => a.name.localeCompare(b.name),
    },
    {
      title: 'Местоположение',
      dataIndex: 'location',
      key: 'location',
    },
    {
      title: 'Статус',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={statusColors[status]} icon={statusIcons[status]}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </Tag>
      ),
      filters: [
        { text: 'Активна', value: 'active' },
        { text: 'Неактивна', value: 'inactive' },
        { text: 'Ошибка', value: 'error' },
        { text: 'Обслуживание', value: 'maintenance' },
      ],
      onFilter: (value: boolean | React.Key, record: Camera) => record.status === String(value),
    },
    {
      title: 'Производитель',
      dataIndex: 'vendor',
      key: 'vendor',
    },
    {
      title: 'Зоны',
      dataIndex: 'zones',
      key: 'zones',
      sorter: (a: Camera, b: Camera) => a.zones - b.zones,
    },
    {
      title: 'Линии',
      dataIndex: 'lines',
      key: 'lines',
      sorter: (a: Camera, b: Camera) => a.lines - b.lines,
    },
    {
      title: 'Правила',
      dataIndex: 'rules',
      key: 'rules',
      sorter: (a: Camera, b: Camera) => a.rules - b.rules,
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_: any, record: Camera) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<VideoCameraOutlined />}
            onClick={() => handleViewStream(record)}
          >
            Поток
          </Button>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            Редактировать
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
            loading={deleteCameraMutation.isPending && deleteCameraMutation.variables === record.id}
          >
            Удалить
          </Button>
        </Space>
      ),
    },
  ];

  const handleViewStream = (camera: Camera) => {
    // Открытие потока в модальном окне или новой вкладке
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
      title: 'Удалить камеру',
      content: 'Вы уверены, что хотите удалить эту камеру?',
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
            <VideoCameraOutlined /> Камеры
          </Title>
        </Col>
        <Col>
          <Button
            type="primary"
            icon={<PlusOutlined />}
            onClick={handleAddCamera}
            loading={createCameraMutation.isPending}
          >
            Добавить камеру
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
        title={editingCamera ? 'Редактировать камеру' : 'Добавить камеру'}
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
            label="Имя камеры"
            rules={[{ required: true, message: 'Пожалуйста, введите имя камеры!' }]}
          >
            <Input placeholder="Enter camera name" />
          </Form.Item>

          <Form.Item
            name="rtspUrl"
            label="RTSP URL"
            rules={[{ required: true, message: 'Пожалуйста, введите RTSP URL!' }]}
          >
            <Input placeholder="rtsp://example.com/stream" />
          </Form.Item>

          <Form.Item
            name="location"
            label="Местоположение"
            rules={[{ required: true, message: 'Пожалуйста, введите местоположение!' }]}
          >
            <Input placeholder="Enter location" />
          </Form.Item>

          <Form.Item
            name="status"
            label="Статус"
            rules={[{ required: true, message: 'Пожалуйста, выберите статус!' }]}
          >
            <Select placeholder="Выберите статус">
              <Option value="active">Активна</Option>
              <Option value="inactive">Неактивна</Option>
              <Option value="error">Ошибка</Option>
              <Option value="maintenance">Обслуживание</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="vendor"
            label="Производитель"
            rules={[{ required: true, message: 'Пожалуйста, выберите производителя!' }]}
          >
            <Select placeholder="Выберите производителя">
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