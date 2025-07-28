import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import toast from 'react-hot-toast';

// Create context
const AuthContext = createContext();

// Initial state
const initialState = {
  user: null,
  isAuthenticated: false,
  loading: true,
  token: localStorage.getItem('token'),
};

// Action types
const AUTH_ACTIONS = {
  LOGIN_START: 'LOGIN_START',
  LOGIN_SUCCESS: 'LOGIN_SUCCESS',
  LOGIN_FAILURE: 'LOGIN_FAILURE',
  LOGOUT: 'LOGOUT',
  SET_LOADING: 'SET_LOADING',
  UPDATE_USER: 'UPDATE_USER',
};

// Reducer
const authReducer = (state, action) => {
  switch (action.type) {
    case AUTH_ACTIONS.LOGIN_START:
      return {
        ...state,
        loading: true,
      };
    case AUTH_ACTIONS.LOGIN_SUCCESS:
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.token,
        isAuthenticated: true,
        loading: false,
      };
    case AUTH_ACTIONS.LOGIN_FAILURE:
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
      };
    case AUTH_ACTIONS.LOGOUT:
      return {
        ...state,
        user: null,
        token: null,
        isAuthenticated: false,
        loading: false,
      };
    case AUTH_ACTIONS.SET_LOADING:
      return {
        ...state,
        loading: action.payload,
      };
    case AUTH_ACTIONS.UPDATE_USER:
      return {
        ...state,
        user: action.payload,
      };
    default:
      return state;
  }
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const navigate = useNavigate();

  // Set up axios defaults
  useEffect(() => {
    if (state.token) {
      axios.defaults.headers.common['Authorization'] = `Bearer ${state.token}`;
    } else {
      delete axios.defaults.headers.common['Authorization'];
    }
  }, [state.token]);

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      if (state.token) {
        try {
          const response = await axios.get('/api/v1/auth/me');
          dispatch({
            type: AUTH_ACTIONS.LOGIN_SUCCESS,
            payload: {
              user: response.data,
              token: state.token,
            },
          });
        } catch (error) {
          console.error('Auth check failed:', error);
          dispatch({ type: AUTH_ACTIONS.LOGOUT });
          localStorage.removeItem('token');
        }
      } else {
        dispatch({ type: AUTH_ACTIONS.SET_LOADING, payload: false });
      }
    };

    checkAuth();
  }, []);

  // Login function
  const login = async (email, password) => {
    dispatch({ type: AUTH_ACTIONS.LOGIN_START });
    
    try {
      const response = await axios.post('/api/v1/auth/login', {
        email,
        password,
      });

      const { user, access_token } = response.data;
      
      localStorage.setItem('token', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      dispatch({
        type: AUTH_ACTIONS.LOGIN_SUCCESS,
        payload: {
          user,
          token: access_token,
        },
      });

      toast.success('Login successful!');
      navigate('/dashboard');
      
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Login failed';
      toast.error(message);
      
      dispatch({ type: AUTH_ACTIONS.LOGIN_FAILURE });
      
      return { success: false, error: message };
    }
  };

  // Register function
  const register = async (userData) => {
    try {
      const response = await axios.post('/api/v1/auth/register', userData);
      
      toast.success('Registration successful! Please login.');
      navigate('/login');
      
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Registration failed';
      toast.error(message);
      
      return { success: false, error: message };
    }
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('token');
    delete axios.defaults.headers.common['Authorization'];
    
    dispatch({ type: AUTH_ACTIONS.LOGOUT });
    
    toast.success('Logged out successfully');
    navigate('/login');
  };

  // Update user profile
  const updateProfile = async (userData) => {
    try {
      const response = await axios.put('/api/v1/auth/profile', userData);
      
      dispatch({
        type: AUTH_ACTIONS.UPDATE_USER,
        payload: response.data,
      });
      
      toast.success('Profile updated successfully!');
      
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Profile update failed';
      toast.error(message);
      
      return { success: false, error: message };
    }
  };

  // Change password
  const changePassword = async (currentPassword, newPassword) => {
    try {
      await axios.put('/api/v1/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      });
      
      toast.success('Password changed successfully!');
      
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Password change failed';
      toast.error(message);
      
      return { success: false, error: message };
    }
  };

  // Forgot password
  const forgotPassword = async (email) => {
    try {
      await axios.post('/api/v1/auth/forgot-password', { email });
      
      toast.success('Password reset email sent!');
      
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Password reset failed';
      toast.error(message);
      
      return { success: false, error: message };
    }
  };

  // Reset password
  const resetPassword = async (token, newPassword) => {
    try {
      await axios.post('/api/v1/auth/reset-password', {
        token,
        new_password: newPassword,
      });
      
      toast.success('Password reset successfully!');
      navigate('/login');
      
      return { success: true };
    } catch (error) {
      const message = error.response?.data?.detail || 'Password reset failed';
      toast.error(message);
      
      return { success: false, error: message };
    }
  };

  // Check if user has specific role
  const hasRole = (roles) => {
    if (!state.user) return false;
    
    if (Array.isArray(roles)) {
      return roles.includes(state.user.role);
    }
    
    return state.user.role === roles;
  };

  // Check if user has specific permission
  const hasPermission = (permission) => {
    if (!state.user || !state.user.permissions) return false;
    
    return state.user.permissions.includes(permission);
  };

  const value = {
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    loading: state.loading,
    token: state.token,
    login,
    register,
    logout,
    updateProfile,
    changePassword,
    forgotPassword,
    resetPassword,
    hasRole,
    hasPermission,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
};