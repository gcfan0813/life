// AI人生模拟器 - Button组件
// 基于设计系统的现代化按钮组件

import React from 'react'
import { motion, HTMLMotionProps } from 'framer-motion'
import { colors } from '../../design-system/colors'
import { spacing, borderRadius } from '../../design-system/spacing'
import { textStyles } from '../../design-system/typography'

// 按钮变体类型
export type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost' | 'danger'
export type ButtonSize = 'sm' | 'base' | 'lg'

// 按钮属性接口
export interface ButtonProps extends Omit<HTMLMotionProps<'button'>, 'children'> {
  variant?: ButtonVariant
  size?: ButtonSize
  children?: React.ReactNode
  loading?: boolean
  disabled?: boolean
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
  fullWidth?: boolean
}

// 按钮样式配置
const buttonStyles = {
  // 基础样式
  base: {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: textStyles.label.base.fontWeight,
    transition: 'all 0.2s ease-in-out',
    cursor: 'pointer',
    border: 'none',
    outline: 'none',
  fontFamily: textStyles.label.base.fontFamily,
  },
  
  // 变体样式
  variants: {
    primary: {
      backgroundColor: colors.primary[500],
      color: colors.slate[50],
      '&:hover': {
        backgroundColor: colors.primary[600],
      },
      '&:active': {
        backgroundColor: colors.primary[700],
      },
    },
    secondary: {
      backgroundColor: colors.secondary[500],
      color: colors.slate[900],
      '&:hover': {
        backgroundColor: colors.secondary[600],
      },
      '&:active': {
        backgroundColor: colors.secondary[700],
      },
    },
    outline: {
      backgroundColor: 'transparent',
      color: colors.primary[500],
      border: `2px solid ${colors.primary[500]}`,
      '&:hover': {
        backgroundColor: colors.primary[500],
        color: colors.slate[50],
      },
      '&:active': {
        backgroundColor: colors.primary[600],
      },
    },
    ghost: {
      backgroundColor: 'transparent',
      color: colors.slate[300],
      '&:hover': {
        backgroundColor: colors.slate[700],
        color: colors.slate[50],
      },
      '&:active': {
        backgroundColor: colors.slate[600],
      },
    },
    danger: {
      backgroundColor: colors.error[500],
      color: colors.slate[50],
      '&:hover': {
        backgroundColor: colors.error[600],
      },
      '&:active': {
        backgroundColor: colors.error[700],
      },
    },
  },
  
  // 尺寸样式
  sizes: {
    sm: {
      padding: `${spacing[2]} ${spacing[3]}`,
      fontSize: textStyles.label.small.fontSize,
      borderRadius: borderRadius.md,
      gap: spacing[1],
    },
    base: {
      padding: `${spacing[2]} ${spacing[4]}`,
      fontSize: textStyles.label.base.fontSize,
      borderRadius: borderRadius.lg,
      gap: spacing[2],
    },
    lg: {
      padding: `${spacing[3]} ${spacing[6]}`,
      fontSize: textStyles.label.large.fontSize,
      borderRadius: borderRadius.lg,
      gap: spacing[2],
    },
  },
}

// Button组件
export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'base',
  children,
  loading = false,
  disabled = false,
  icon,
  iconPosition = 'left',
  fullWidth = false,
  className = '',
  ...props
}) => {
  // 样式计算
  const baseStyle = buttonStyles.base
  const variantStyle = buttonStyles.variants[variant]
  const sizeStyle = buttonStyles.sizes[size]
  
  // 组合样式
  const combinedStyle = {
    ...baseStyle,
    ...sizeStyle,
    width: fullWidth ? '100%' : 'auto',
    opacity: disabled || loading ? 0.6 : 1,
    cursor: disabled || loading ? 'not-allowed' : 'pointer',
  }

  return (
    <motion.button
      whileHover={!disabled && !loading ? { scale: 1.02 } : {}}
      whileTap={!disabled && !loading ? { scale: 0.98 } : {}}
      disabled={disabled || loading}
      className={`ai-button ai-button--${variant} ai-button--${size} ${className}`}
      style={combinedStyle}
      {...props}
    >
      {/* Loading图标 */}
      {loading && (
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
          style={{ width: size === 'sm' ? 14 : 16, height: size === 'sm' ? 14 : 16 }}
        >
          ⚙️
        </motion.div>
      )}
      
      {/* 左侧图标 */}
      {!loading && icon && iconPosition === 'left' && icon}
      
      {/* 按钮内容 */}
      {children}
      
      {/* 右侧图标 */}
      {!loading && icon && iconPosition === 'right' && icon}
    </motion.button>
  )
}

export default Button