import React, { useState } from 'react';
import {
  Layout as AntLayout,
  Menu,
  theme,
  Badge,
  Avatar,
  Dropdown,
  Space,
  Button,
  Drawer,
  List,
  Typography,
} from 'antd';
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  DashboardOutlined,
  VideoCameraOutlined,
  AlertOutlined,
  BarChartOutlined,
  SettingOutlined,
  BellOutlined,
  UserOutlined,
  LogoutOutlined,
} from '@ant-design/icons';
import { Link, Outlet, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { Alert } from '../../types';

const { Header, Sider, Content } = AntLayout;
const { Text } = Typography;

const Layout = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  // Данные пользователя для тестирования - в реальном приложении будут из контекста аутентификации
  const user = {
    name: 'Администратор',
    email: 'admin@insightcore.com',
  };

  // Данные уведомлений для тестирования
  const { data: notifications = [] } = useQuery<Alert[]>({
    queryKey: ['notifications'],
    queryFn: async () => [
      { id: 1, title: 'Обнаружено новое событие', message: 'Обнаружен человек в запретной зоне', timestamp: '2 мин назад', type: 'warning', read: false },
      { id: 2, title: 'Системное предупреждение', message: 'Камера отключена: Входная камера 1', timestamp: '5 мин назад', type: 'error', read: false },
      { id: 3, title: 'Обновление аналитики', message: 'Сформирован ежедневный отчет', timestamp: '1 час назад', type: 'info', read: false },
    ],
    staleTime: 30000, // 30 seconds
  });

  const menuItems = [
    {
      key: 'dashboard',
      icon: <DashboardOutlined />,
      label: <Link to="/dashboard">Панель управления</Link>,
    },
    {
      key: 'cameras',
      icon: <VideoCameraOutlined />,
      label: <Link to="/cameras">Камеры</Link>,
    },
    {
      key: 'events',
      icon: <AlertOutlined />,
      label: <Link to="/events">События</Link>,
    },
    {
      key: 'analytics',
      icon: <BarChartOutlined />,
      label: <Link to="/analytics">Аналитика</Link>,
    },
    {
      key: 'alerts',
      icon: <BellOutlined />,
      label: <Link to="/alerts">Оповещения</Link>,
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: <Link to="/settings">Настройки</Link>,
    },
  ];

  const userMenuItems = [
    {
      key: 'profile',
      label: 'Профиль',
      icon: <UserOutlined />,
    },
    {
      key: 'logout',
      label: 'Выйти',
      icon: <LogoutOutlined />,
      onClick: () => {
        // Handle logout
        navigate('/login');
      },
    },
  ];

  const [notificationsVisible, setNotificationsVisible] = useState(false);

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider
        collapsible
        collapsed={collapsed}
        onCollapse={(value) => setCollapsed(value)}
        style={{
          overflow: 'auto',
          height: '100vh',
          position: 'fixed',
          left: 0,
          top: 0,
          bottom: 0,
        }}
      >
        <div
          style={{
            height: 32,
            margin: 16,
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: borderRadiusLG,
          }}
        />
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={['dashboard']}
          items={menuItems}
        />
      </Sider>

      <AntLayout style={{ marginLeft: collapsed ? 80 : 20 }}>
        <Header
          style={{
            padding: 0,
            background: colorBgContainer,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          }}
        >
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            style={{
              fontSize: '16px',
              width: 64,
              height: 64,
            }}
          />
          
          <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
            {/* Notifications dropdown */}
            <Dropdown
              overlay={
                <List
                  size="small"
                  header={<Text strong>Уведомления</Text>}
                  footer={
                    <Button type="link" size="small" onClick={() => setNotificationsVisible(false)}>
                      Просмотреть все
                    </Button>
                  }
                  bordered
                  dataSource={notifications}
                  renderItem={(item) => (
                    <List.Item key={item.id}>
                      <List.Item.Meta
                        title={item.title}
                        description={
                          <div>
                            <div>{item.message}</div>
                            <Text type="secondary" style={{ fontSize: '12px' }}>
                              {item.timestamp}
                            </Text>
                          </div>
                        }
                      />
                    </List.Item>
                  )}
                />
              }
              trigger={['click']}
              placement="bottomRight"
            >
              <Badge count={notifications.length}>
                <Button
                  type="text"
                  icon={<BellOutlined />}
                  size="large"
                  onClick={(e) => e.preventDefault()}
                />
              </Badge>
            </Dropdown>

            {/* User dropdown */}
            <Dropdown
              menu={{ items: userMenuItems }}
              trigger={['click']}
            >
              <Space style={{ cursor: 'pointer' }}>
                <Avatar icon={<UserOutlined />} />
                <span style={{ display: collapsed ? 'none' : 'inline' }}>
                  {user.name}
                </span>
              </Space>
            </Dropdown>
          </div>
        </Header>

        <Content
          style={{
            margin: '24px 16px',
            padding: 24,
            minHeight: 280,
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
        >
          <Outlet />
        </Content>
      </AntLayout>

      {/* Notifications drawer */}
      <Drawer
        title="Уведомления"
        placement="right"
        closable
        onClose={() => setNotificationsVisible(false)}
        open={notificationsVisible}
        width={380}
      >
        <List
          dataSource={notifications}
          renderItem={(item) => (
            <List.Item key={item.id}>
              <List.Item.Meta
                avatar={<Avatar icon={<BellOutlined />} />}
                title={item.title}
                description={
                  <div>
                    <div>{item.message}</div>
                    <Text type="secondary" style={{ fontSize: '12px' }}>
                      {item.timestamp}
                    </Text>
                  </div>
                }
              />
            </List.Item>
          )}
        />
      </Drawer>
    </AntLayout>
 );
};

export default Layout;