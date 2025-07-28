import React, { useState } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import {
  Box,
  Drawer,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  useTheme,
  useMediaQuery,
  Avatar,
  Menu,
  MenuItem,
  Divider,
  Badge,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Dashboard,
  People,
  School,
  Assignment,
  Payment,
  Assessment,
  Notifications,
  Settings,
  Person,
  Logout,
  Brightness4,
  Brightness7,
  Chat,
  Science,
  Security,
  Analytics,
  Schedule,
  Mic,
  Fingerprint,
  Home,
} from '@mui/icons-material';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme as useCustomTheme } from '../../contexts/ThemeContext';
import Sidebar from './Sidebar';

const drawerWidth = 280;

const Layout = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [mobileOpen, setMobileOpen] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const { user, logout } = useAuth();
  const { darkMode, toggleDarkMode } = useCustomTheme();
  const location = useLocation();

  const handleDrawerToggle = () => {
    setMobileOpen(!mobileOpen);
  };

  const handleProfileMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleProfileMenuClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    handleProfileMenuClose();
    logout();
  };

  const getPageTitle = () => {
    const path = location.pathname;
    const pathMap = {
      '/dashboard': 'Dashboard',
      '/students': 'Students',
      '/teachers': 'Teachers',
      '/attendance': 'Attendance',
      '/fees': 'Fees',
      '/courses': 'Courses',
      '/assignments': 'Assignments',
      '/ai': 'AI Assistant',
      '/reports': 'Reports',
      '/settings': 'Settings',
      '/profile': 'Profile',
    };

    // Check for dynamic routes
    if (path.startsWith('/students/')) return 'Student Details';
    if (path.startsWith('/teachers/')) return 'Teacher Details';
    if (path.startsWith('/courses/')) return 'Course Details';
    if (path.startsWith('/advanced/')) return 'Advanced Features';

    return pathMap[path] || 'School Management';
  };

  const drawer = (
    <Sidebar
      onDrawerToggle={handleDrawerToggle}
      isMobile={isMobile}
    />
  );

  return (
    <Box sx={{ display: 'flex' }}>
      {/* App Bar */}
      <AppBar
        position="fixed"
        sx={{
          width: { md: `calc(100% - ${drawerWidth}px)` },
          ml: { md: `${drawerWidth}px` },
          zIndex: theme.zIndex.drawer + 1,
        }}
      >
        <Toolbar>
          <IconButton
            color="inherit"
            aria-label="open drawer"
            edge="start"
            onClick={handleDrawerToggle}
            sx={{ mr: 2, display: { md: 'none' } }}
          >
            <MenuIcon />
          </IconButton>

          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            {getPageTitle()}
          </Typography>

          {/* Theme Toggle */}
          <IconButton color="inherit" onClick={toggleDarkMode}>
            {darkMode ? <Brightness7 /> : <Brightness4 />}
          </IconButton>

          {/* Notifications */}
          <IconButton color="inherit">
            <Badge badgeContent={4} color="error">
              <Notifications />
            </Badge>
          </IconButton>

          {/* User Menu */}
          <IconButton
            onClick={handleProfileMenuOpen}
            sx={{ ml: 1 }}
          >
            <Avatar
              sx={{ width: 32, height: 32 }}
              alt={user?.name || 'User'}
            >
              {user?.name?.charAt(0) || 'U'}
            </Avatar>
          </IconButton>

          {/* Profile Menu */}
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={handleProfileMenuClose}
            onClick={handleProfileMenuClose}
            PaperProps={{
              elevation: 0,
              sx: {
                overflow: 'visible',
                filter: 'drop-shadow(0px 2px 8px rgba(0,0,0,0.32))',
                mt: 1.5,
                '& .MuiAvatar-root': {
                  width: 32,
                  height: 32,
                  ml: -0.5,
                  mr: 1,
                },
                '&:before': {
                  content: '""',
                  display: 'block',
                  position: 'absolute',
                  top: 0,
                  right: 14,
                  width: 10,
                  height: 10,
                  bgcolor: 'background.paper',
                  transform: 'translateY(-50%) rotate(45deg)',
                  zIndex: 0,
                },
              },
            }}
            transformOrigin={{ horizontal: 'right', vertical: 'top' }}
            anchorOrigin={{ horizontal: 'right', vertical: 'bottom' }}
          >
            <MenuItem onClick={() => window.location.href = '/profile'}>
              <Person />
              Profile
            </MenuItem>
            <MenuItem onClick={() => window.location.href = '/settings'}>
              <Settings />
              Settings
            </MenuItem>
            <Divider />
            <MenuItem onClick={handleLogout}>
              <Logout />
              Logout
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      {/* Sidebar */}
      <Box
        component="nav"
        sx={{ width: { md: drawerWidth }, flexShrink: { md: 0 } }}
      >
        {/* Mobile drawer */}
        <Drawer
          variant="temporary"
          open={mobileOpen}
          onClose={handleDrawerToggle}
          ModalProps={{
            keepMounted: true, // Better open performance on mobile.
          }}
          sx={{
            display: { xs: 'block', md: 'none' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
        >
          {drawer}
        </Drawer>

        {/* Desktop drawer */}
        <Drawer
          variant="permanent"
          sx={{
            display: { xs: 'none', md: 'block' },
            '& .MuiDrawer-paper': {
              boxSizing: 'border-box',
              width: drawerWidth,
            },
          }}
          open
        >
          {drawer}
        </Drawer>
      </Box>

      {/* Main content */}
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          p: 3,
          width: { md: `calc(100% - ${drawerWidth}px)` },
          mt: '64px', // AppBar height
        }}
      >
        <Outlet />
      </Box>
    </Box>
  );
};

export default Layout;