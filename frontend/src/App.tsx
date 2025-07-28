import React, { Suspense } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import { Helmet } from 'react-helmet-async'
import { motion, AnimatePresence } from 'framer-motion'

import { useAuth } from './hooks/useAuth'
import { useTheme } from './hooks/useTheme'
import LoadingSpinner from './components/ui/LoadingSpinner'
import ProtectedRoute from './components/auth/ProtectedRoute'

// Lazy load pages for better performance
const LoginPage = React.lazy(() => import('./pages/auth/LoginPage'))
const DashboardPage = React.lazy(() => import('./pages/dashboard/DashboardPage'))
const StudentsPage = React.lazy(() => import('./pages/students/StudentsPage'))
const TeachersPage = React.lazy(() => import('./pages/teachers/TeachersPage'))
const AttendancePage = React.lazy(() => import('./pages/attendance/AttendancePage'))
const FeesPage = React.lazy(() => import('./pages/fees/FeesPage'))
const ReportsPage = React.lazy(() => import('./pages/reports/ReportsPage'))
const AIAssistantPage = React.lazy(() => import('./pages/ai/AIAssistantPage'))
const AdvancedFeaturesPage = React.lazy(() => import('./pages/advanced/AdvancedFeaturesPage'))
const SettingsPage = React.lazy(() => import('./pages/settings/SettingsPage'))
const ProfilePage = React.lazy(() => import('./pages/profile/ProfilePage'))
const NotFoundPage = React.lazy(() => import('./pages/NotFoundPage'))

// Layout components
const DashboardLayout = React.lazy(() => import('./layouts/DashboardLayout'))
const AuthLayout = React.lazy(() => import('./layouts/AuthLayout'))

function App() {
  const { isAuthenticated, isLoading } = useAuth()
  const { theme } = useTheme()

  if (isLoading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <LoadingSpinner size="lg" />
      </div>
    )
  }

  return (
    <>
      <Helmet>
        <title>Aiqube School Management System</title>
        <meta name="description" content="Modern, AI-powered school management system" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <meta name="theme-color" content={theme === 'dark' ? '#1e293b' : '#ffffff'} />
      </Helmet>

      <div className={`min-h-screen bg-background text-foreground ${theme}`}>
        <AnimatePresence mode="wait">
          <Suspense
            fallback={
              <div className="flex h-screen items-center justify-center">
                <LoadingSpinner size="lg" />
              </div>
            }
          >
            <Routes>
              {/* Public routes */}
              <Route
                path="/auth/*"
                element={
                  <AuthLayout>
                    <Routes>
                      <Route path="login" element={<LoginPage />} />
                      <Route path="*" element={<Navigate to="/auth/login" replace />} />
                    </Routes>
                  </AuthLayout>
                }
              />

              {/* Protected routes */}
              <Route
                path="/*"
                element={
                  <ProtectedRoute>
                    <DashboardLayout>
                      <Routes>
                        <Route path="/" element={<Navigate to="/dashboard" replace />} />
                        <Route
                          path="/dashboard"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <DashboardPage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/students/*"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <StudentsPage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/teachers/*"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <TeachersPage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/attendance/*"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <AttendancePage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/fees/*"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <FeesPage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/reports/*"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <ReportsPage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/ai-assistant/*"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <AIAssistantPage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/advanced/*"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <AdvancedFeaturesPage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/settings/*"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <SettingsPage />
                            </motion.div>
                          }
                        />
                        <Route
                          path="/profile"
                          element={
                            <motion.div
                              initial={{ opacity: 0, y: 20 }}
                              animate={{ opacity: 1, y: 0 }}
                              exit={{ opacity: 0, y: -20 }}
                              transition={{ duration: 0.3 }}
                            >
                              <ProfilePage />
                            </motion.div>
                          }
                        />
                        <Route path="*" element={<NotFoundPage />} />
                      </Routes>
                    </DashboardLayout>
                  </ProtectedRoute>
                }
              />

              {/* Redirect to dashboard if authenticated, otherwise to login */}
              <Route
                path="*"
                element={
                  <Navigate
                    to={isAuthenticated ? "/dashboard" : "/auth/login"}
                    replace
                  />
                }
              />
            </Routes>
          </Suspense>
        </AnimatePresence>
      </div>
    </>
  )
}

export default App