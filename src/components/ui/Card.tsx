// AI人生模拟器 - Card组件
// 基于设计系统的现代化卡片组件

import React from 'react'
import { motion, HTMLMotionProps } from 'framer-motion'
import { colors, opacityColors } from '../../design-system/colors'
import { spacing, borderRadius } from '../../design-system/spacing'

// 卡片变体类型
export type CardVariant = 'default' | 'elevated' | 'outlined' | 'filled'
export type CardPadding = 'none' | 'sm' | 'base' | 'lg'

// 卡片属性接口
export interface CardProps extends HTMLMotionProps<'div'> {
  variant?: CardVariant
  padding?: CardPadding
  children?: React.ReactNode
  interactive?: boolean
  selected?: boolean
}

// 卡片样式配置
const cardStyles = {
  // 基础样式
  base: {
    backgroundColor: colors.slate[800],
    borderRadius: borderRadius.xl,
    transition: 'all 0.3s ease-in-out',
    overflow: 'hidden',
  },
  
  // 变体样式
  variants: {
    default: {
      backgroundColor: colors.slate[800],
      boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    },
    elevated: {
      backgroundColor: colors.slate[700],
      boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    },
    outlined: {
      backgroundColor: colors.slate[800],
      border: `1px solid ${colors.slate[600]}`,
    },
    filled: {
      backgroundColor: colors.slate[700],
    },
  },
  
  // 内边距样式
  paddings: {
    none: {
      padding: 0,
    },
    sm: {
      padding: spacing[4],
    },
    base: {
      padding: spacing[6],
    },
    lg: {
      padding: spacing[8],
    },
  },
}

// Card组件
export const Card: React.FC<CardProps> = ({
  variant = 'default',
  padding = 'base',
  children,
  interactive = false,
  selected = false,
  className = '',
  style,
  ...props
}) => {
  // 样式计算
  const baseStyle = cardStyles.base
  const variantStyle = cardStyles.variants[variant]
  const paddingStyle = cardStyles.paddings[padding]
  
  // 组合样式
  const combinedStyle = {
    ...baseStyle,
    ...variantStyle,
    ...paddingStyle,
    ...(selected && {
      border: `2px solid ${colors.primary[500]}`,
      boxShadow: `0 0 0 3px ${opacityColors.primary[20]}`,
    }),
    ...style,
  }

  return (
    <motion.div
      whileHover={interactive ? { scale: 1.01 } : {}}
      whileTap={interactive ? { scale: 0.99 } : {}}
      className={`ai-card ai-card--${variant} ${className}`}
      style={combinedStyle}
      {...props}
    >
      {children}
    </motion.div>
  )
}

// 卡片头部组件
export interface CardHeaderProps {
  children?: React.ReactNode
  title?: string
  subtitle?: string
  action?: React.ReactNode
}

export const CardHeader: React.FC<CardHeaderProps> = ({
  children,
  title,
  subtitle,
  action,
}) => {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      marginBottom: spacing[4],
    }}>
      <div>
        {title && (
          <h3 style={{
            fontSize: '1.125rem',
            fontWeight: 600,
            color: colors.slate[50],
            margin: 0,
          }}>
            {title}
          </h3>
        )}
        {subtitle && (
          <p style={{
            fontSize: '0.875rem',
            color: colors.slate[400],
            margin: `${spacing[1]} 0 0 0`,
          }}>
            {subtitle}
          </p>
        )}
        {children}
      </div>
      {action && <div>{action}</div>}
    </div>
  )
}

// 卡片内容组件
export interface CardContentProps {
  children?: React.ReactNode
}

export const CardContent: React.FC<CardContentProps> = ({ children }) => {
  return <div>{children}</div>
}

// 卡片底部组件
export interface CardFooterProps {
  children?: React.ReactNode
}

export const CardFooter: React.FC<CardFooterProps> = ({ children }) => {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'flex-end',
      marginTop: spacing[4],
      paddingTop: spacing[4],
      borderTop: `1px solid ${colors.slate[600]}`,
      gap: spacing[3],
    }}>
      {children}
    </div>
  )
}

export default Card