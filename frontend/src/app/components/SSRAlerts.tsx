'use client';

import React from 'react';
import {
  Card,
  Table,
  Typography,
  Space,
  Tag,
  Button,
  Badge,
  Row,
  Col,
  Modal,
} from 'antd';
import {
  AlertOutlined,
  EyeOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  FilterOutlined,
  SearchOutlined,
  DownloadOutlined,
} from '@ant-design/icons';
import { Alert } from '@/types';

const { Title } = Typography;

interface SSRAlertsProps {
  alerts: Alert[];
  loading?: boolean;
}

const SSRAlerts: React.FC<SSRAlertsProps> = ({ alerts, loading = false }) => {
  const typeColors: Record<string, string> = {
    info: 'blue',
    warning: 'orange',
    error: 'red',
    success: 'green',
  };

  const typeIcons: Record<string, React.ReactNode> = {
    info: <CheckCircleOutlined />,
    warning: <AlertOutlined />,
    error: <ClockCircleOutlined />,
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
      title: 'Заголовок',
      dataIndex: 'title',
      key: 'title',
      sorter: (a: Alert, b: Alert) => a.title.localeCompare(b.title),
    },
    {
      title: 'Сообщение',
      dataIndex: 'message',
      key: 'message',
    },
    {
      title: 'Тип',
      dataIndex: 'type',
      key: 'type',
      render: (type: string) => (
        <Tag color={typeColors[type]} icon={typeIcons[type]}>
          {type.toUpperCase()}
        </Tag>
      ),
      sorter: (a: Alert, b: Alert) => a.type.localeCompare(b.type),
      filters: [
        { text: 'Информация', value: 'info' },
        { text: 'Предупреждение', value: 'warning' },
        { text: 'Ошибка', value: 'error' },
        { text: 'Успех', value: 'success' },
      ],
      onFilter: (value: boolean | React.Key, record: Alert) => record.type === value,
    },
    {
      title: 'Время',
      dataIndex: 'timestamp',
      key: 'timestamp',
      sorter: (a: Alert, b: Alert) => new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
    },
    {
      title: 'Статус',
      key: 'read',
      render: (_: any, record: Alert) => (
        <Badge
          status={record.read ? 'success' : 'error'}
          text={record.read ? 'Прочитано' : 'Непрочитано'}
        />
      ),
      filters: [
        { text: 'Прочитано', value: true },
        { text: 'Непрочитано', value: false },
      ],
      onFilter: (value: boolean | React.Key, record: Alert) => record.read === value,
    },
    {
      title: 'Действия',
      key: 'actions',
      render: (_: any, record: Alert) => (
        <Space size="middle">
          <Button
            type="link"
            icon={<EyeOutlined />}
            onClick={() => console.log('View alert:', record)}
          >
            Просмотр
          </Button>
          <Button
            type="link"
            icon={<DownloadOutlined />}
            onClick={() => console.log('Download alert:', record)}
          >
            Экспорт
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
            <AlertOutlined /> Оповещения
          </Title>
        </Col>
        <Col>
          <Space>
            <Button
              type="primary"
              onClick={() => console.log('Mark all as read')}
            >
              Отметить все прочитанными
            </Button>
            <Button
              danger
              onClick={() => console.log('Clear all alerts')}
            >
              Очистить все
            </Button>
          </Space>
        </Col>
      </Row>

      <Card>
        <Table
          columns={columns}
          dataSource={alerts}
          loading={loading}
          rowKey="id"
          pagination={{ pageSize: 15 }}
          scroll={{ x: 1200 }}
        />
      </Card>

      <Modal
        title="Детали оповещения"
        open={false}
        onCancel={() => {}}
        footer={null}
      >
        {/* Modal content will be handled by client-side */}
      </Modal>
    </div>
  );
};

export default SSRAlerts;