import React from 'react'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '@/utils/cn'
import { Loader2 } from 'lucide-react'

const spinnerVariants = cva(
  'animate-spin',
  {
    variants: {
      size: {
        sm: 'h-4 w-4',
        default: 'h-6 w-6',
        lg: 'h-8 w-8',
        xl: 'h-12 w-12',
      },
      variant: {
        default: 'text-primary',
        muted: 'text-muted-foreground',
        white: 'text-white',
      },
    },
    defaultVariants: {
      size: 'default',
      variant: 'default',
    },
  }
)

interface LoadingSpinnerProps extends VariantProps<typeof spinnerVariants> {
  className?: string
  text?: string
}

export default function LoadingSpinner({ 
  size, 
  variant, 
  className, 
  text 
}: LoadingSpinnerProps) {
  return (
    <div className="flex flex-col items-center justify-center space-y-2">
      <Loader2 className={cn(spinnerVariants({ size, variant }), className)} />
      {text && (
        <p className="text-sm text-muted-foreground animate-pulse">{text}</p>
      )}
    </div>
  )
}

// Alternative spinner designs
export function DotsSpinner({ className }: { className?: string }) {
  return (
    <div className={cn('flex space-x-1', className)}>
      {[0, 1, 2].map((i) => (
        <div
          key={i}
          className="h-2 w-2 bg-primary rounded-full animate-pulse"
          style={{
            animationDelay: `${i * 0.2}s`,
            animationDuration: '1s',
          }}
        />
      ))}
    </div>
  )
}

export function PulseSpinner({ className }: { className?: string }) {
  return (
    <div className={cn('relative', className)}>
      <div className="h-8 w-8 rounded-full bg-primary/20 animate-ping" />
      <div className="absolute inset-0 h-8 w-8 rounded-full bg-primary/40 animate-pulse" />
      <div className="absolute inset-2 h-4 w-4 rounded-full bg-primary" />
    </div>
  )
}

export function BarSpinner({ className }: { className?: string }) {
  return (
    <div className={cn('flex space-x-1', className)}>
      {[0, 1, 2, 3, 4].map((i) => (
        <div
          key={i}
          className="w-1 bg-primary rounded-full animate-pulse"
          style={{
            height: `${Math.random() * 20 + 10}px`,
            animationDelay: `${i * 0.1}s`,
            animationDuration: '1.2s',
          }}
        />
      ))}
    </div>
  )
}