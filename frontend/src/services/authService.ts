import { apiClient } from './api'
import { User, LoginForm } from '@/types'

interface LoginResponse {
  accessToken: string
  refreshToken: string
  tokenType: string
  user: User
}

interface RegisterForm {
  email: string
  username?: string
  password: string
  confirmPassword: string
  firstName: string
  lastName: string
  phone?: string
  role?: string
}

export const authService = {
  // Authentication
  login: async (email: string, password: string): Promise<LoginResponse> => {
    return apiClient.post('/auth/login', { email, password })
  },

  register: async (data: RegisterForm): Promise<{ message: string; userId: string }> => {
    return apiClient.post('/auth/register', data)
  },

  logout: async (): Promise<void> => {
    return apiClient.post('/auth/logout')
  },

  refreshToken: async (refreshToken: string): Promise<LoginResponse> => {
    return apiClient.post('/auth/refresh', { refreshToken })
  },

  // Password management
  requestPasswordReset: async (email: string): Promise<{ message: string }> => {
    return apiClient.post('/auth/password-reset-request', { email })
  },

  confirmPasswordReset: async (
    token: string,
    newPassword: string,
    confirmPassword: string
  ): Promise<{ message: string }> => {
    return apiClient.post('/auth/password-reset-confirm', {
      token,
      newPassword,
      confirmPassword,
    })
  },

  changePassword: async (
    currentPassword: string,
    newPassword: string,
    confirmPassword: string
  ): Promise<{ message: string }> => {
    return apiClient.post('/auth/change-password', {
      currentPassword,
      newPassword,
      confirmPassword,
    })
  },

  // User profile
  getCurrentUser: async (): Promise<User> => {
    return apiClient.get('/auth/profile')
  },

  updateProfile: async (data: Partial<User>): Promise<User> => {
    return apiClient.put('/auth/profile', data)
  },

  // Email verification
  verifyEmail: async (token: string): Promise<{ message: string }> => {
    return apiClient.post(`/auth/verify-email/${token}`)
  },

  resendVerification: async (email: string): Promise<{ message: string }> => {
    return apiClient.post('/auth/resend-verification', { email })
  },

  // Utility methods
  isAuthenticated: (): boolean => {
    return !!localStorage.getItem('accessToken')
  },

  getToken: (): string | null => {
    return localStorage.getItem('accessToken')
  },

  removeTokens: (): void => {
    localStorage.removeItem('accessToken')
    localStorage.removeItem('refreshToken')
  },

  // Role and permission checks
  getRoles: async (): Promise<{ roles: Record<string, string> }> => {
    return apiClient.get('/auth/roles')
  },
}