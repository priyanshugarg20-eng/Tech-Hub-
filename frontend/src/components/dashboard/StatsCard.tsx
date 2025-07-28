import React from 'react'
import { motion } from 'framer-motion'
import { LucideIcon, TrendingUp, TrendingDown, Minus } from 'lucide-react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card'
import { cn } from '@/utils/cn'

interface StatsCardProps {
  title: string
  value: string | number
  change?: number
  changeLabel?: string
  icon: LucideIcon
  trend?: 'up' | 'down' | 'stable'
  color?: 'blue' | 'green' | 'purple' | 'orange' | 'red'
  loading?: boolean
}

const colorVariants = {
  blue: {
    bg: 'bg-blue-500/10',
    text: 'text-blue-600',
    icon: 'text-blue-600',
  },
  green: {
    bg: 'bg-green-500/10',
    text: 'text-green-600',
    icon: 'text-green-600',
  },
  purple: {
    bg: 'bg-purple-500/10',
    text: 'text-purple-600',
    icon: 'text-purple-600',
  },
  orange: {
    bg: 'bg-orange-500/10',
    text: 'text-orange-600',
    icon: 'text-orange-600',
  },
  red: {
    bg: 'bg-red-500/10',
    text: 'text-red-600',
    icon: 'text-red-600',
  },
}

export default function StatsCard({
  title,
  value,
  change,
  changeLabel,
  icon: Icon,
  trend = 'stable',
  color = 'blue',
  loading = false,
}: StatsCardProps) {
  const colors = colorVariants[color]

  const TrendIcon = trend === 'up' ? TrendingUp : trend === 'down' ? TrendingDown : Minus

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.3 }}
      whileHover={{ scale: 1.02 }}
      className="group"
    >
      <Card className="relative overflow-hidden transition-all duration-300 hover:shadow-lg">
        <div className="absolute inset-0 bg-gradient-to-br from-transparent to-primary/5 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
        
        <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
          <CardTitle className="text-sm font-medium text-muted-foreground">
            {title}
          </CardTitle>
          <div className={cn('flex h-8 w-8 items-center justify-center rounded-lg', colors.bg)}>
            <Icon className={cn('h-4 w-4', colors.icon)} />
          </div>
        </CardHeader>
        
        <CardContent>
          <div className="space-y-2">
            {loading ? (
              <div className="h-8 w-24 animate-pulse rounded bg-muted" />
            ) : (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.1 }}
                className="text-2xl font-bold"
              >
                {typeof value === 'number' ? value.toLocaleString() : value}
              </motion.div>
            )}
            
            {change !== undefined && changeLabel && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="flex items-center space-x-1 text-xs"
              >
                <TrendIcon
                  className={cn(
                    'h-3 w-3',
                    trend === 'up' && 'text-green-600',
                    trend === 'down' && 'text-red-600',
                    trend === 'stable' && 'text-muted-foreground'
                  )}
                />
                <span
                  className={cn(
                    'font-medium',
                    trend === 'up' && 'text-green-600',
                    trend === 'down' && 'text-red-600',
                    trend === 'stable' && 'text-muted-foreground'
                  )}
                >
                  {change > 0 && trend !== 'down' ? '+' : ''}
                  {change}
                  {typeof change === 'number' && change % 1 !== 0 ? '%' : ''}
                </span>
                <span className="text-muted-foreground">{changeLabel}</span>
              </motion.div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}