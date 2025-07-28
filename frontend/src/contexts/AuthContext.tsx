import React, { createContext, useContext, useReducer, useEffect } from 'react'
import { User, UserRole } from '@/types'
import { authService } from '@/services/authService'
import { toast } from 'sonner'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: User }
  | { type: 'AUTH_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'UPDATE_USER'; payload: Partial<User> }
  | { type: 'CLEAR_ERROR' }

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,
}

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      }
    case 'AUTH_SUCCESS':
      return {
        ...state,
        user: action.payload,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      }
    case 'AUTH_FAILURE':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: action.payload,
      }
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      }
    case 'UPDATE_USER':
      return {
        ...state,
        user: state.user ? { ...state.user, ...action.payload } : null,
      }
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      }
    default:
      return state
  }
}

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  updateUser: (userData: Partial<User>) => void
  clearError: () => void
  hasRole: (roles: UserRole | UserRole[]) => boolean
  hasPermission: (permission: string) => boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState)

  // Check for existing session on mount
  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('accessToken')
        if (!token) {
          dispatch({ type: 'AUTH_FAILURE', payload: 'No token found' })
          return
        }

        dispatch({ type: 'AUTH_START' })
        const user = await authService.getCurrentUser()
        dispatch({ type: 'AUTH_SUCCESS', payload: user })
      } catch (error) {
        localStorage.removeItem('accessToken')
        localStorage.removeItem('refreshToken')
        dispatch({ type: 'AUTH_FAILURE', payload: 'Session expired' })
      }
    }

    checkAuth()
  }, [])

  const login = async (email: string, password: string) => {
    try {
      dispatch({ type: 'AUTH_START' })
      const response = await authService.login(email, password)
      
      localStorage.setItem('accessToken', response.accessToken)
      localStorage.setItem('refreshToken', response.refreshToken)
      
      dispatch({ type: 'AUTH_SUCCESS', payload: response.user })
      toast.success('Welcome back!')
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Login failed'
      dispatch({ type: 'AUTH_FAILURE', payload: message })
      toast.error(message)
      throw error
    }
  }

  const logout = async () => {
    try {
      await authService.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      dispatch({ type: 'LOGOUT' })
      toast.success('Logged out successfully')
    }
  }

  const updateUser = (userData: Partial<User>) => {
    dispatch({ type: 'UPDATE_USER', payload: userData })
  }

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' })
  }

  const hasRole = (roles: UserRole | UserRole[]): boolean => {
    if (!state.user) return false
    const roleArray = Array.isArray(roles) ? roles : [roles]
    return roleArray.includes(state.user.role)
  }

  const hasPermission = (permission: string): boolean => {
    if (!state.user) return false
    
    // Define role-based permissions
    const permissions: Record<UserRole, string[]> = {
      [UserRole.SUPER_ADMIN]: ['*'], // All permissions
      [UserRole.ADMIN]: [
        'manage_school',
        'manage_students',
        'manage_teachers',
        'manage_staff',
        'view_reports',
        'manage_fees',
        'manage_hostel',
        'manage_transport',
      ],
      [UserRole.TEACHER]: [
        'manage_classes',
        'manage_students',
        'take_attendance',
        'grade_assignments',
        'view_student_progress',
        'create_assignments',
        'send_notifications',
      ],
      [UserRole.STUDENT]: [
        'view_own_data',
        'submit_assignments',
        'view_grades',
        'view_schedule',
        'view_attendance',
      ],
      [UserRole.PARENT]: [
        'view_child_data',
        'view_child_grades',
        'view_child_attendance',
        'pay_fees',
        'receive_notifications',
      ],
      [UserRole.STAFF]: [
        'manage_attendance',
        'manage_fees',
        'view_reports',
        'send_notifications',
      ],
    }

    const userPermissions = permissions[state.user.role] || []
    return userPermissions.includes('*') || userPermissions.includes(permission)
  }

  const value: AuthContextType = {
    ...state,
    login,
    logout,
    updateUser,
    clearError,
    hasRole,
    hasPermission,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}