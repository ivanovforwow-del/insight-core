import apiClient from './api';

interface LoginCredentials {
  username: string;
  password: string;
}

interface LoginResponse {
  access: string;
  refresh: string;
}

export const authService = {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    const response = await apiClient.post('/auth/token/', credentials);
    return response.data;
  },

  async refreshToken(refreshToken: string): Promise<{ access: string }> {
    const response = await apiClient.post('/auth/token/refresh/', { refresh: refreshToken });
    return response.data;
  },

  async verifyToken(token: string): Promise<any> {
    const response = await apiClient.post('/auth/token/verify/', { token });
    return response.data;
 },

  setTokens(access: string, refresh: string): void {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  },

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  },

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  },

  clearTokens(): void {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  },

  isAuthenticated(): boolean {
    const token = this.getAccessToken();
    return token !== null && token !== '';
  }
};