import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';

// Layout Components
import Layout from './components/layout/Layout';
import Dashboard from './components/dashboard/Dashboard';

// Authentication
import Login from './components/auth/Login';
import Register from './components/auth/Register';
import ForgotPassword from './components/auth/ForgotPassword';
import ResetPassword from './components/auth/ResetPassword';

// Student Management
import StudentList from './components/students/StudentList';
import StudentDetail from './components/students/StudentDetail';
import StudentForm from './components/students/StudentForm';

// Teacher Management
import TeacherList from './components/teachers/TeacherList';
import TeacherDetail from './components/teachers/TeacherDetail';
import TeacherForm from './components/teachers/TeacherForm';

// Attendance
import AttendanceList from './components/attendance/AttendanceList';
import AttendanceForm from './components/attendance/AttendanceForm';
import AttendanceReport from './components/attendance/AttendanceReport';

// Fees Management
import FeeList from './components/fees/FeeList';
import FeeForm from './components/fees/FeeForm';
import FeeReport from './components/fees/FeeReport';

// LMS (Learning Management System)
import CourseList from './components/lms/CourseList';
import CourseDetail from './components/lms/CourseDetail';
import AssignmentList from './components/lms/AssignmentList';

// AI Assistant
import AIAssistant from './components/ai/AIAssistant';
import AIConversations from './components/ai/AIConversations';
import AIKnowledgeBase from './components/ai/AIKnowledgeBase';

// Advanced Features
import BlockchainCertificates from './components/advanced/BlockchainCertificates';
import ARVRContent from './components/advanced/ARVRContent';
import IoTDashboard from './components/advanced/IoTDashboard';
import Gamification from './components/advanced/Gamification';
import Analytics from './components/advanced/Analytics';
import SmartScheduling from './components/advanced/SmartScheduling';
import VoiceAssistant from './components/advanced/VoiceAssistant';
import BiometricAttendance from './components/advanced/BiometricAttendance';
import SmartClassrooms from './components/advanced/SmartClassrooms';

// Reports
import Reports from './components/reports/Reports';

// Settings
import Settings from './components/settings/Settings';
import Profile from './components/settings/Profile';

// Context
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider as CustomThemeProvider } from './contexts/ThemeContext';

// Protected Route Component
const ProtectedRoute = ({ children, roles = [] }) => {
  const { user, isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  if (roles.length > 0 && user && !roles.includes(user.role)) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
};

// Create Material-UI theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
      light: '#42a5f5',
      dark: '#1565c0',
    },
    secondary: {
      main: '#dc004e',
      light: '#ff5983',
      dark: '#9a0036',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: 'none',
          borderRadius: 8,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
        },
      },
    },
  },
});

// Create React Query client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CustomThemeProvider>
          <CssBaseline />
          <AuthProvider>
            <Router>
              <Box sx={{ display: 'flex', minHeight: '100vh' }}>
                <Routes>
                  {/* Public Routes */}
                  <Route path="/login" element={<Login />} />
                  <Route path="/register" element={<Register />} />
                  <Route path="/forgot-password" element={<ForgotPassword />} />
                  <Route path="/reset-password" element={<ResetPassword />} />
                  
                  {/* Protected Routes */}
                  <Route path="/" element={
                    <ProtectedRoute>
                      <Layout />
                    </ProtectedRoute>
                  }>
                    <Route index element={<Navigate to="/dashboard" replace />} />
                    <Route path="dashboard" element={<Dashboard />} />
                    
                    {/* Student Management */}
                    <Route path="students" element={<StudentList />} />
                    <Route path="students/new" element={<StudentForm />} />
                    <Route path="students/:id" element={<StudentDetail />} />
                    <Route path="students/:id/edit" element={<StudentForm />} />
                    
                    {/* Teacher Management */}
                    <Route path="teachers" element={<TeacherList />} />
                    <Route path="teachers/new" element={<TeacherForm />} />
                    <Route path="teachers/:id" element={<TeacherDetail />} />
                    <Route path="teachers/:id/edit" element={<TeacherForm />} />
                    
                    {/* Attendance */}
                    <Route path="attendance" element={<AttendanceList />} />
                    <Route path="attendance/new" element={<AttendanceForm />} />
                    <Route path="attendance/report" element={<AttendanceReport />} />
                    
                    {/* Fees */}
                    <Route path="fees" element={<FeeList />} />
                    <Route path="fees/new" element={<FeeForm />} />
                    <Route path="fees/report" element={<FeeReport />} />
                    
                    {/* LMS */}
                    <Route path="courses" element={<CourseList />} />
                    <Route path="courses/:id" element={<CourseDetail />} />
                    <Route path="assignments" element={<AssignmentList />} />
                    
                    {/* AI Assistant */}
                    <Route path="ai" element={<AIAssistant />} />
                    <Route path="ai/conversations" element={<AIConversations />} />
                    <Route path="ai/knowledge-base" element={<AIKnowledgeBase />} />
                    
                    {/* Advanced Features */}
                    <Route path="advanced/certificates" element={<BlockchainCertificates />} />
                    <Route path="advanced/arvr" element={<ARVRContent />} />
                    <Route path="advanced/iot" element={<IoTDashboard />} />
                    <Route path="advanced/gamification" element={<Gamification />} />
                    <Route path="advanced/analytics" element={<Analytics />} />
                    <Route path="advanced/scheduling" element={<SmartScheduling />} />
                    <Route path="advanced/voice" element={<VoiceAssistant />} />
                    <Route path="advanced/biometric" element={<BiometricAttendance />} />
                    <Route path="advanced/classrooms" element={<SmartClassrooms />} />
                    
                    {/* Reports */}
                    <Route path="reports" element={<Reports />} />
                    
                    {/* Settings */}
                    <Route path="settings" element={<Settings />} />
                    <Route path="profile" element={<Profile />} />
                  </Route>
                  
                  {/* Catch all route */}
                  <Route path="*" element={<Navigate to="/dashboard" replace />} />
                </Routes>
              </Box>
            </Router>
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: '#363636',
                  color: '#fff',
                },
              }}
            />
          </AuthProvider>
        </CustomThemeProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;