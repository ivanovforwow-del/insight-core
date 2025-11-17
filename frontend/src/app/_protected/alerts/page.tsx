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
import { useQuery } from '@tanstack/react-query';
import moment from 'moment';
import { Alert } from '@/types';
import { useAlerts, useAlert, useUnreadAlertsCount, useRecentAlerts, useMarkAlertAsRead, useMarkAllAlertsAsRead, useDeleteAlert, useDeleteAllAlerts } from '@/hooks/data/useAlertData';

const { Title } = Typography;
const { RangePicker } = DatePicker;
const { Option } = Select;

const AlertsPage = () => {
  const [filterVisible, setFilterVisible] = useState(false);
  const [filters, setFilters] = useState<Record<string, any>>({});
  const [selectedAlert, setSelectedAlert] = useState<Alert | null>(null);

  const { data: alerts = { data: [], total: 0, page: 1, limit: 10 }, isLoading } = useAlerts(filters);
 const markAsReadMutation = useMarkAlertAsRead();
  const markAllAsReadMutation = useMarkAllAlertsAsRead();
  const deleteAlertMutation = useDeleteAlert();
  const deleteAllAlertsMutation = useDeleteAllAlerts();

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
      title: 'Название',
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
      sorter: (a: Alert, b: Alert) => moment(a.timestamp).diff(moment(b.timestamp)),
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
            onClick={() => setSelectedAlert(record)}
          >
            Просмотр
          </Button>
          {!record.read && (
            <Button
              type="link"
              icon={<CheckCircleOutlined />}
              onClick={() => markAsReadMutation.mutate(record.id)}
              loading={markAsReadMutation.isPending && markAsReadMutation.variables === record.id}
            >
              Отметить как прочитанное
            </Button>
          )}
          <Button
            type="link"
            icon={<DownloadOutlined />}
            onClick={() => console.log('Download alert details:', record)}
          >
            Экспорт
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
      title: 'Очистить все уведомления',
      content: 'Вы уверены, что хотите очистить все уведомления?',
      onOk: () => deleteAllAlertsMutation.mutate(),
    });
  };

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
              danger
              onClick={handleClearAll}
              loading={deleteAllAlertsMutation.isPending}
            >
              Очистить все
            </Button>
            <RangePicker onChange={handleDateRangeChange} />
            <Button
              icon={<FilterOutlined />}
              onClick={() => setFilterVisible(!filterVisible)}
            >
              Фильтры
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
                placeholder="Фильтр по типу"
                onChange={(value) => handleFilterChange({ type: value })}
                allowClear
              >
                <Option value="info">Информация</Option>
                <Option value="warning">Предупреждение</Option>
                <Option value="error">Ошибка</Option>
                <Option value="success">Успех</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Select
                style={{ width: '100%' }}
                placeholder="Фильтр по статусу"
                onChange={(value) => handleFilterChange({ read: value })}
                allowClear
              >
                <Option value={true}>Прочитано</Option>
                <Option value={false}>Непрочитано</Option>
              </Select>
            </Col>
            <Col span={8}>
              <Input
                placeholder="Поиск уведомлений..."
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
          dataSource={alerts.data}
          loading={isLoading || markAsReadMutation.isPending}
          rowKey="id"
          pagination={{ 
            pageSize: alerts.limit, 
            total: alerts.total,
            current: alerts.page,
            onChange: (page, pageSize) => setFilters({ ...filters, page, limit: pageSize })
          }}
          scroll={{ x: 1200 }}
        />
      </Card>

      <Modal
        title="Детали уведомления"
        open={!!selectedAlert}
        onCancel={() => setSelectedAlert(null)}
        footer={[
          <Button key="close" onClick={() => setSelectedAlert(null)}>
            Закрыть
          </Button>,
        ]}
      >
        {selectedAlert && (
          <div>
            <Typography.Title level={4}>{selectedAlert.title}</Typography.Title>
            <Typography.Paragraph>
              <strong>Сообщение:</strong> {selectedAlert.message}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Тип:</strong> {selectedAlert.type.toUpperCase()}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Время:</strong> {selectedAlert.timestamp}
            </Typography.Paragraph>
            <Typography.Paragraph>
              <strong>Статус:</strong> {selectedAlert.read ? 'Прочитано' : 'Непрочитано'}
            </Typography.Paragraph>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default AlertsPage;