'use client';

import React from 'react';
import {
  Card,
  Table,
  Typography,
  Space,
  Tag,
  Button,
  Row,
  Col,
} from 'antd';
import {
  VideoCameraOutlined,
  EyeOutlined,
  EditOutlined,
  DeleteOutlined,
} from '@ant-design/icons';
import { Camera } from '@/types';

const { Title } = Typography;

interface SSRCamerasProps {
  cameras: Camera[];
  loading?: boolean;
}

const SSRCameras: React.FC<SSRCamerasProps> = ({ cameras, loading = false }) => {
  const statusColors: Record<string, string> = {
    active: 'green',
    inactive: 'default',
    error: 'red',
    maintenance: 'orange',
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
        <Tag color={statusColors[status]}>
          {status.charAt(0).toUpperCase() + status.slice(1)}
        </Tag>
      ),
      filters: [
        { text: 'Активна', value: 'active' },
        { text: 'Неактивна', value: 'inactive' },
        { text: 'Ошибка', value: 'error' },
        { text: 'Обслуживание', value: 'maintenance' },
      ],
      onFilter: (value: boolean | React.Key, record: Camera) => record.status === value,
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
            icon={<EyeOutlined />}
            onClick={() => console.log('View stream for:', record)}
          >
            Поток
          </Button>
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => console.log('Edit camera:', record)}
          >
            Редактировать
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => console.log('Delete camera:', record.id)}
          >
            Удалить
          </Button>
        </Space>
      ),
    },
  ];

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
            icon={<EditOutlined />}
            onClick={() => console.log('Add Camera clicked')}
          >
            Добавить камеру
          </Button>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={cameras}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1200 }}
        />
      </Card>
    </div>
  );
};

export default SSRCameras;