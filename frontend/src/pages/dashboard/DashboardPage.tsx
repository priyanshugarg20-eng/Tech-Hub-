import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { motion } from 'framer-motion'
import { 
  Users, 
  GraduationCap, 
  Calendar, 
  DollarSign, 
  TrendingUp, 
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Clock,
  BookOpen,
  Brain,
  Zap,
} from 'lucide-react'

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/Card'
import { Badge } from '@/components/ui/Badge'
import LoadingSpinner from '@/components/ui/LoadingSpinner'
import { DashboardStats } from '@/types'
import { apiClient } from '@/services/api'
import StatsCard from '@/components/dashboard/StatsCard'
import AttendanceChart from '@/components/dashboard/AttendanceChart'
import FeeCollectionChart from '@/components/dashboard/FeeCollectionChart'
import RecentActivities from '@/components/dashboard/RecentActivities'
import AlertsPanel from '@/components/dashboard/AlertsPanel'
import QuickActions from '@/components/dashboard/QuickActions'
import AIInsights from '@/components/dashboard/AIInsights'

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  show: { opacity: 1, y: 0 }
}

export default function DashboardPage() {
  const { data: stats, isLoading, error } = useQuery<DashboardStats>({
    queryKey: ['dashboard-stats'],
    queryFn: () => apiClient.get('/reports/dashboard'),
    refetchInterval: 30000, // Refresh every 30 seconds
  })

  if (isLoading) {
    return (
      <div className="flex h-96 items-center justify-center">
        <LoadingSpinner size="lg" text="Loading dashboard..." />
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex h-96 items-center justify-center">
        <Card className="p-6">
          <div className="flex items-center space-x-2 text-error-600">
            <AlertTriangle className="h-5 w-5" />
            <span>Failed to load dashboard data</span>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="space-y-6"
    >
      {/* Header */}
      <motion.div variants={item}>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-muted-foreground">
              Welcome back! Here's what's happening at your school today.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="success" className="animate-pulse">
              <div className="mr-1 h-2 w-2 rounded-full bg-current" />
              Live Data
            </Badge>
          </div>
        </div>
      </motion.div>

      {/* Stats Cards */}
      <motion.div variants={item}>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
          <StatsCard
            title="Total Students"
            value={stats?.totalStudents || 0}
            change={stats?.newStudentsThisMonth || 0}
            changeLabel="new this month"
            icon={Users}
            trend="up"
            color="blue"
          />
          <StatsCard
            title="Total Teachers"
            value={stats?.totalTeachers || 0}
            change={5}
            changeLabel="active teachers"
            icon={GraduationCap}
            trend="stable"
            color="green"
          />
          <StatsCard
            title="Attendance Rate"
            value={`${stats?.attendanceStats?.attendanceRate || 0}%`}
            change={2.5}
            changeLabel="vs last week"
            icon={Calendar}
            trend="up"
            color="purple"
          />
          <StatsCard
            title="Fee Collection"
            value={`${stats?.feeStats?.collectionRate || 0}%`}
            change={-1.2}
            changeLabel="vs last month"
            icon={DollarSign}
            trend="down"
            color="orange"
          />
        </div>
      </motion.div>

      {/* AI Insights */}
      <motion.div variants={item}>
        <AIInsights />
      </motion.div>

      {/* Charts and Analytics */}
      <motion.div variants={item}>
        <div className="grid gap-6 lg:grid-cols-2">
          <Card className="col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <Calendar className="h-5 w-5" />
                <span>Attendance Trends</span>
              </CardTitle>
              <CardDescription>
                Daily attendance patterns over the last 30 days
              </CardDescription>
            </CardHeader>
            <CardContent>
              <AttendanceChart />
            </CardContent>
          </Card>

          <Card className="col-span-1">
            <CardHeader>
              <CardTitle className="flex items-center space-x-2">
                <DollarSign className="h-5 w-5" />
                <span>Fee Collection</span>
              </CardTitle>
              <CardDescription>
                Monthly fee collection progress
              </CardDescription>
            </CardHeader>
            <CardContent>
              <FeeCollectionChart />
            </CardContent>
          </Card>
        </div>
      </motion.div>

      {/* Quick Actions */}
      <motion.div variants={item}>
        <QuickActions />
      </motion.div>

      {/* Activities and Alerts */}
      <motion.div variants={item}>
        <div className="grid gap-6 lg:grid-cols-3">
          <div className="lg:col-span-2">
            <RecentActivities activities={stats?.recentActivities || []} />
          </div>
          <div className="lg:col-span-1">
            <AlertsPanel alerts={stats?.alerts || []} />
          </div>
        </div>
      </motion.div>

      {/* Advanced Features Preview */}
      <motion.div variants={item}>
        <Card className="bg-gradient-to-br from-primary/5 to-primary/10 border-primary/20">
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Brain className="h-5 w-5 text-primary" />
              <span>AI-Powered Features</span>
              <Badge variant="gradient" size="sm">New</Badge>
            </CardTitle>
            <CardDescription>
              Explore our cutting-edge AI and advanced features
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid gap-4 md:grid-cols-3">
              <div className="flex items-center space-x-3 p-3 rounded-lg bg-background/50">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10">
                  <Brain className="h-5 w-5 text-primary" />
                </div>
                <div>
                  <h4 className="font-medium">AI Doubt Solving</h4>
                  <p className="text-sm text-muted-foreground">24/7 AI tutoring</p>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 rounded-lg bg-background/50">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-success-500/10">
                  <CheckCircle className="h-5 w-5 text-success-600" />
                </div>
                <div>
                  <h4 className="font-medium">Blockchain Certificates</h4>
                  <p className="text-sm text-muted-foreground">Secure credentials</p>
                </div>
              </div>
              <div className="flex items-center space-x-3 p-3 rounded-lg bg-background/50">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-warning-500/10">
                  <Zap className="h-5 w-5 text-warning-600" />
                </div>
                <div>
                  <h4 className="font-medium">Smart IoT Campus</h4>
                  <p className="text-sm text-muted-foreground">Connected devices</p>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </motion.div>
  )
}