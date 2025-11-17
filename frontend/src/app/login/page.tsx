'use client';

import React, { useState } from 'react';
import { Card, Form, Input, Button, Typography, message, Space } from 'antd';
import { UserOutlined, LockOutlined } from '@ant-design/icons';
import { useRouter } from 'next/navigation';
import { authService } from '../../services/authService';

const { Title, Text } = Typography;

const LoginPage = () => {
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const onFinish = async (values: { username: string; password: string }) => {
    setLoading(true);
    try {
      const { access, refresh } = await authService.login({
        username: values.username,
        password: values.password,
      });

      authService.setTokens(access, refresh);

      message.success('Вход выполнен успешно!');
      // Перенаправление на панель управления или предыдущую страницу
      router.push('/cameras');
      router.refresh();
    } catch (error: any) {
      console.error('Ошибка входа:', error);
      message.error(error.response?.data?.detail || 'Вход не выполнен. Пожалуйста, проверьте свои учетные данные.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)'
    }}>
      <Card 
        style={{ 
          width: 400, 
          boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
          borderRadius: '8px'
        }}
        title={
          <div style={{ textAlign: 'center' }}>
            <Title level={3} style={{ marginBottom: 0 }}>InsightCore</Title>
            <Text type="secondary">Платформа видеоаналитики</Text>
          </div>
        }
      >
        <Form
          name="login"
          initialValues={{ remember: true }}
          onFinish={onFinish}
          autoComplete="off"
          layout="vertical"
        >
          <Form.Item
            label="Имя пользователя"
            name="username"
            rules={[{ required: true, message: 'Пожалуйста, введите имя пользователя!' }]}
          >
            <Input
              prefix={<UserOutlined />}
              placeholder="Введите имя пользователя"
            />
          </Form.Item>

          <Form.Item
            label="Пароль"
            name="password"
            rules={[{ required: true, message: 'Пожалуйста, введите пароль!' }]}
          >
            <Input.Password
              prefix={<LockOutlined />}
              placeholder="Введите пароль"
            />
          </Form.Item>

          <Form.Item>
            <Button 
              type="primary" 
              htmlType="submit" 
              loading={loading}
              style={{ width: '100%' }}
            >
              Войти
            </Button>
          </Form.Item>
          
          <div style={{ textAlign: 'center' }}>
            <Text type="secondary">
              Демонстрационные учетные данные: admin / admin12345
            </Text>
          </div>
        </Form>
      </Card>
    </div>
  );
};

export default LoginPage;