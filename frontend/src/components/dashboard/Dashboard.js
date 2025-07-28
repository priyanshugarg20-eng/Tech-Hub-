import React from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Avatar,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Chip,
  Button,
  useTheme,
} from '@mui/material';
import {
  People,
  School,
  Assignment,
  Payment,
  TrendingUp,
  TrendingDown,
  Notifications,
  Event,
  CheckCircle,
  Warning,
  Error,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell } from 'recharts';
import { useAuth } from '../../contexts/AuthContext';

const Dashboard = () => {
  const theme = useTheme();
  const { user } = useAuth();

  // Mock data - in real app, this would come from API
  const stats = {
    totalStudents: 1250,
    totalTeachers: 85,
    attendanceRate: 94.5,
    feeCollection: 1250000,
    pendingFees: 150000,
    activeCourses: 45,
  };

  const attendanceData = [
    { name: 'Mon', present: 95, absent: 5 },
    { name: 'Tue', present: 92, absent: 8 },
    { name: 'Wed', present: 94, absent: 6 },
    { name: 'Thu', present: 96, absent: 4 },
    { name: 'Fri', present: 93, absent: 7 },
  ];

  const feeData = [
    { month: 'Jan', collected: 120000, pending: 30000 },
    { month: 'Feb', collected: 135000, pending: 25000 },
    { month: 'Mar', collected: 140000, pending: 20000 },
    { month: 'Apr', collected: 125000, pending: 35000 },
    { month: 'May', collected: 150000, pending: 15000 },
  ];

  const recentActivities = [
    {
      id: 1,
      type: 'attendance',
      message: 'Attendance marked for Class 10A',
      time: '2 minutes ago',
      status: 'success',
    },
    {
      id: 2,
      type: 'fee',
      message: 'Fee payment received from Student ID 12345',
      time: '15 minutes ago',
      status: 'success',
    },
    {
      id: 3,
      type: 'notification',
      message: 'New assignment posted for Mathematics',
      time: '1 hour ago',
      status: 'info',
    },
    {
      id: 4,
      type: 'warning',
      message: 'Low attendance alert for Class 9B',
      time: '2 hours ago',
      status: 'warning',
    },
  ];

  const getStatusIcon = (status) => {
    switch (status) {
      case 'success':
        return <CheckCircle color="success" />;
      case 'warning':
        return <Warning color="warning" />;
      case 'error':
        return <Error color="error" />;
      default:
        return <Notifications color="info" />;
    }
  };

  const StatCard = ({ title, value, icon, color, trend }) => (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <Box>
            <Typography color="text.secondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div" sx={{ fontWeight: 'bold' }}>
              {value}
            </Typography>
            {trend && (
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                {trend > 0 ? (
                  <TrendingUp color="success" sx={{ fontSize: 16, mr: 0.5 }} />
                ) : (
                  <TrendingDown color="error" sx={{ fontSize: 16, mr: 0.5 }} />
                )}
                <Typography
                  variant="body2"
                  color={trend > 0 ? 'success.main' : 'error.main'}
                >
                  {Math.abs(trend)}% from last month
                </Typography>
              </Box>
            )}
          </Box>
          <Avatar
            sx={{
              bgcolor: color,
              width: 56,
              height: 56,
            }}
          >
            {icon}
          </Avatar>
        </Box>
      </CardContent>
    </Card>
  );

  return (
    <Box>
      {/* Welcome Section */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Welcome back, {user?.name || 'User'}!
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Here's what's happening in your school today.
        </Typography>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Students"
            value={stats.totalStudents.toLocaleString()}
            icon={<People />}
            color="primary.main"
            trend={5.2}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Teachers"
            value={stats.totalTeachers}
            icon={<School />}
            color="secondary.main"
            trend={2.1}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Attendance Rate"
            value={`${stats.attendanceRate}%`}
            icon={<Assignment />}
            color="success.main"
            trend={1.5}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Fee Collection"
            value={`₹${(stats.feeCollection / 100000).toFixed(1)}L`}
            icon={<Payment />}
            color="warning.main"
            trend={-2.3}
          />
        </Grid>
      </Grid>

      {/* Charts Section */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        {/* Attendance Chart */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Weekly Attendance
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={attendanceData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="present"
                    stroke={theme.palette.primary.main}
                    strokeWidth={2}
                    name="Present"
                  />
                  <Line
                    type="monotone"
                    dataKey="absent"
                    stroke={theme.palette.error.main}
                    strokeWidth={2}
                    name="Absent"
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Fee Collection Chart */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Fee Collection Trend
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={feeData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="collected" fill={theme.palette.success.main} name="Collected" />
                  <Bar dataKey="pending" fill={theme.palette.warning.main} name="Pending" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Activities and Quick Actions */}
      <Grid container spacing={3}>
        {/* Recent Activities */}
        <Grid item xs={12} md={8}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Activities
              </Typography>
              <List>
                {recentActivities.map((activity) => (
                  <ListItem key={activity.id} divider>
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: 'background.paper' }}>
                        {getStatusIcon(activity.status)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={activity.message}
                      secondary={activity.time}
                    />
                    <Chip
                      label={activity.type}
                      size="small"
                      color={
                        activity.status === 'success'
                          ? 'success'
                          : activity.status === 'warning'
                          ? 'warning'
                          : 'info'
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                <Button
                  variant="contained"
                  startIcon={<Assignment />}
                  fullWidth
                  onClick={() => window.location.href = '/attendance/new'}
                >
                  Mark Attendance
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Payment />}
                  fullWidth
                  onClick={() => window.location.href = '/fees/new'}
                >
                  Record Fee Payment
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<School />}
                  fullWidth
                  onClick={() => window.location.href = '/students/new'}
                >
                  Add New Student
                </Button>
                <Button
                  variant="outlined"
                  startIcon={<Event />}
                  fullWidth
                  onClick={() => window.location.href = '/ai'}
                >
                  AI Assistant
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;