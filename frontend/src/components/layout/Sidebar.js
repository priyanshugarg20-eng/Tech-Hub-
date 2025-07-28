import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Box,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Typography,
  Collapse,
  Avatar,
} from '@mui/material';
import {
  Dashboard,
  People,
  School,
  Assignment,
  Payment,
  Assessment,
  Chat,
  Science,
  Security,
  Analytics,
  Schedule,
  Mic,
  Fingerprint,
  Home,
  ExpandLess,
  ExpandMore,
  Settings,
  Report,
  Book,
  Group,
  Person,
  Notifications,
  TrendingUp,
  SmartToy,
  Vr,
  Sensors,
  EmojiEvents,
  Timeline,
  ScheduleSend,
  RecordVoiceOver,
  Biometric,
  MeetingRoom,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';

const Sidebar = ({ onDrawerToggle, isMobile }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { user, hasRole } = useAuth();
  const [openMenus, setOpenMenus] = React.useState({
    management: false,
    academic: false,
    advanced: false,
  });

  const handleMenuToggle = (menu) => {
    setOpenMenus(prev => ({
      ...prev,
      [menu]: !prev[menu],
    }));
  };

  const handleNavigation = (path) => {
    navigate(path);
    if (isMobile) {
      onDrawerToggle();
    }
  };

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path + '/');
  };

  const menuItems = [
    {
      title: 'Dashboard',
      path: '/dashboard',
      icon: <Dashboard />,
      roles: ['super_admin', 'admin', 'teacher', 'student', 'parent'],
    },
    {
      title: 'Management',
      icon: <People />,
      roles: ['super_admin', 'admin'],
      subItems: [
        {
          title: 'Students',
          path: '/students',
          icon: <School />,
        },
        {
          title: 'Teachers',
          path: '/teachers',
          icon: <Person />,
        },
      ],
    },
    {
      title: 'Academic',
      icon: <Book />,
      roles: ['super_admin', 'admin', 'teacher'],
      subItems: [
        {
          title: 'Attendance',
          path: '/attendance',
          icon: <Assignment />,
        },
        {
          title: 'Courses',
          path: '/courses',
          icon: <Book />,
        },
        {
          title: 'Assignments',
          path: '/assignments',
          icon: <Assignment />,
        },
      ],
    },
    {
      title: 'Finance',
      icon: <Payment />,
      roles: ['super_admin', 'admin'],
      subItems: [
        {
          title: 'Fees',
          path: '/fees',
          icon: <Payment />,
        },
      ],
    },
    {
      title: 'AI Assistant',
      path: '/ai',
      icon: <SmartToy />,
      roles: ['super_admin', 'admin', 'teacher', 'student'],
    },
    {
      title: 'Advanced Features',
      icon: <Science />,
      roles: ['super_admin', 'admin'],
      subItems: [
        {
          title: 'Blockchain Certificates',
          path: '/advanced/certificates',
          icon: <Security />,
        },
        {
          title: 'AR/VR Content',
          path: '/advanced/arvr',
          icon: <Vr />,
        },
        {
          title: 'IoT Dashboard',
          path: '/advanced/iot',
          icon: <Sensors />,
        },
        {
          title: 'Gamification',
          path: '/advanced/gamification',
          icon: <EmojiEvents />,
        },
        {
          title: 'Analytics',
          path: '/advanced/analytics',
          icon: <Analytics />,
        },
        {
          title: 'Smart Scheduling',
          path: '/advanced/scheduling',
          icon: <ScheduleSend />,
        },
        {
          title: 'Voice Assistant',
          path: '/advanced/voice',
          icon: <RecordVoiceOver />,
        },
        {
          title: 'Biometric Attendance',
          path: '/advanced/biometric',
          icon: <Biometric />,
        },
        {
          title: 'Smart Classrooms',
          path: '/advanced/classrooms',
          icon: <MeetingRoom />,
        },
      ],
    },
    {
      title: 'Reports',
      path: '/reports',
      icon: <Report />,
      roles: ['super_admin', 'admin', 'teacher'],
    },
    {
      title: 'Settings',
      path: '/settings',
      icon: <Settings />,
      roles: ['super_admin', 'admin', 'teacher', 'student', 'parent'],
    },
  ];

  const renderMenuItem = (item) => {
    // Check if user has permission to see this menu item
    if (!hasRole(item.roles)) {
      return null;
    }

    if (item.subItems) {
      return (
        <Box key={item.title}>
          <ListItem disablePadding>
            <ListItemButton
              onClick={() => handleMenuToggle(item.title.toLowerCase().replace(' ', '_'))}
              sx={{
                backgroundColor: openMenus[item.title.toLowerCase().replace(' ', '_')] ? 'rgba(25, 118, 210, 0.08)' : 'transparent',
              }}
            >
              <ListItemIcon sx={{ color: 'inherit' }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText primary={item.title} />
              {openMenus[item.title.toLowerCase().replace(' ', '_')] ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
          </ListItem>
          <Collapse in={openMenus[item.title.toLowerCase().replace(' ', '_')]} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {item.subItems.map((subItem) => (
                <ListItem key={subItem.path} disablePadding>
                  <ListItemButton
                    sx={{ pl: 4 }}
                    onClick={() => handleNavigation(subItem.path)}
                    selected={isActive(subItem.path)}
                  >
                    <ListItemIcon sx={{ color: 'inherit' }}>
                      {subItem.icon}
                    </ListItemIcon>
                    <ListItemText primary={subItem.title} />
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Collapse>
        </Box>
      );
    }

    return (
      <ListItem key={item.path} disablePadding>
        <ListItemButton
          onClick={() => handleNavigation(item.path)}
          selected={isActive(item.path)}
        >
          <ListItemIcon sx={{ color: 'inherit' }}>
            {item.icon}
          </ListItemIcon>
          <ListItemText primary={item.title} />
        </ListItemButton>
      </ListItem>
    );
  };

  return (
    <Box sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      {/* Logo/Brand */}
      <Box
        sx={{
          p: 2,
          display: 'flex',
          alignItems: 'center',
          gap: 2,
          borderBottom: 1,
          borderColor: 'divider',
        }}
      >
        <Avatar
          sx={{
            bgcolor: 'primary.main',
            width: 40,
            height: 40,
          }}
        >
          <School />
        </Avatar>
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
            Aiqube SMS
          </Typography>
          <Typography variant="caption" color="text.secondary">
            School Management System
          </Typography>
        </Box>
      </Box>

      {/* User Info */}
      {user && (
        <Box
          sx={{
            p: 2,
            borderBottom: 1,
            borderColor: 'divider',
          }}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Avatar
              sx={{ width: 40, height: 40 }}
              alt={user.name}
            >
              {user.name?.charAt(0) || 'U'}
            </Avatar>
            <Box>
              <Typography variant="subtitle2" sx={{ fontWeight: 'bold' }}>
                {user.name}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {user.role?.replace('_', ' ').toUpperCase()}
              </Typography>
            </Box>
          </Box>
        </Box>
      )}

      {/* Navigation Menu */}
      <Box sx={{ flexGrow: 1, overflow: 'auto' }}>
        <List>
          {menuItems.map(renderMenuItem)}
        </List>
      </Box>

      {/* Footer */}
      <Box
        sx={{
          p: 2,
          borderTop: 1,
          borderColor: 'divider',
          textAlign: 'center',
        }}
      >
        <Typography variant="caption" color="text.secondary">
          Version 1.0.0
        </Typography>
      </Box>
    </Box>
  );
};

export default Sidebar;