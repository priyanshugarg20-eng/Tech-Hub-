import React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/utils/cn'

const badgeVariants = cva(
  'inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2',
  {
    variants: {
      variant: {
        default: 'border-transparent bg-primary text-primary-foreground hover:bg-primary/80',
        secondary: 'border-transparent bg-secondary text-secondary-foreground hover:bg-secondary/80',
        destructive: 'border-transparent bg-destructive text-destructive-foreground hover:bg-destructive/80',
        outline: 'text-foreground',
        success: 'border-transparent bg-success-100 text-success-800 dark:bg-success-900 dark:text-success-200',
        warning: 'border-transparent bg-warning-100 text-warning-800 dark:bg-warning-900 dark:text-warning-200',
        error: 'border-transparent bg-error-100 text-error-800 dark:bg-error-900 dark:text-error-200',
        info: 'border-transparent bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
        gradient: 'border-transparent bg-gradient-to-r from-primary-500 to-primary-700 text-white',
      },
      size: {
        default: 'px-2.5 py-0.5 text-xs',
        sm: 'px-2 py-0.5 text-xs',
        lg: 'px-3 py-1 text-sm',
        xl: 'px-4 py-1.5 text-base',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
)

export interface BadgeProps
  extends React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {
  icon?: React.ReactNode
  dot?: boolean
}

function Badge({ className, variant, size, icon, dot, children, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant, size }), className)} {...props}>
      {dot && (
        <span className="mr-1 h-1.5 w-1.5 rounded-full bg-current" />
      )}
      {icon && <span className="mr-1">{icon}</span>}
      {children}
    </div>
  )
}

export { Badge, badgeVariants }

// Predefined status badges
export function StatusBadge({ 
  status, 
  className, 
  ...props 
}: { 
  status: 'active' | 'inactive' | 'pending' | 'error' | 'success' | 'warning'
  className?: string 
} & Omit<BadgeProps, 'variant'>) {
  const variants = {
    active: 'success',
    inactive: 'secondary',
    pending: 'warning',
    error: 'error',
    success: 'success',
    warning: 'warning',
  } as const

  const labels = {
    active: 'Active',
    inactive: 'Inactive',
    pending: 'Pending',
    error: 'Error',
    success: 'Success',
    warning: 'Warning',
  }

  return (
    <Badge 
      variant={variants[status]} 
      className={className} 
      dot
      {...props}
    >
      {labels[status]}
    </Badge>
  )
}

export function AttendanceBadge({ 
  status, 
  className, 
  ...props 
}: { 
  status: 'present' | 'absent' | 'late' | 'leave' | 'holiday'
  className?: string 
} & Omit<BadgeProps, 'variant'>) {
  const variants = {
    present: 'success',
    absent: 'error',
    late: 'warning',
    leave: 'info',
    holiday: 'secondary',
  } as const

  const labels = {
    present: 'Present',
    absent: 'Absent',
    late: 'Late',
    leave: 'Leave',
    holiday: 'Holiday',
  }

  return (
    <Badge 
      variant={variants[status]} 
      className={className} 
      dot
      {...props}
    >
      {labels[status]}
    </Badge>
  )
}

export function PaymentBadge({ 
  status, 
  className, 
  ...props 
}: { 
  status: 'paid' | 'pending' | 'overdue' | 'partial' | 'cancelled' | 'refunded'
  className?: string 
} & Omit<BadgeProps, 'variant'>) {
  const variants = {
    paid: 'success',
    pending: 'warning',
    overdue: 'error',
    partial: 'info',
    cancelled: 'secondary',
    refunded: 'outline',
  } as const

  const labels = {
    paid: 'Paid',
    pending: 'Pending',
    overdue: 'Overdue',
    partial: 'Partial',
    cancelled: 'Cancelled',
    refunded: 'Refunded',
  }

  return (
    <Badge 
      variant={variants[status]} 
      className={className} 
      dot
      {...props}
    >
      {labels[status]}
    </Badge>
  )
}