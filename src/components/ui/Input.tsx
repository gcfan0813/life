// AI人生模拟器 - Input组件
// 基于设计系统的现代化输入框组件

import React from 'react'
import { motion, HTMLMotionProps } from 'framer-motion'
import { colors, opacityColors } from '../../design-system/colors'
import { spacing, borderRadius } from '../../design-system/spacing'
import { textStyles } from '../../design-system/typography'

// 输入框变体类型
export type InputVariant = 'default' | 'filled' | 'outlined'
export type InputSize = 'sm' | 'base' | 'lg'

// 输入框属性接口
export interface InputProps extends Omit<HTMLMotionProps<'input'>, 'size'> {
  variant?: InputVariant
  inputSize?: InputSize
  label?: string
  error?: string
  helper?: string
  icon?: React.ReactNode
  iconPosition?: 'left' | 'right'
  fullWidth?: boolean
}

// 输入框样式配置
const inputStyles = {
  // 基础样式
  base: {
    backgroundColor: colors.slate[700],
    border: `1px solid ${colors.slate[600]}`,
    borderRadius: borderRadius.lg,
    color: colors.slate[50],
    fontSize: textStyles.body.base.fontSize,
    fontFamily: textStyles.body.base.fontFamily,
    transition: 'all 0.2s ease-in-out',
    outline: 'none',
    width: '100%',
    '&:focus': {
      borderColor: colors.primary[500],
      boxShadow: `0 0 0 3px ${opacityColors.primary[20]}`,
    },
    '&::placeholder': {
      color: colors.slate[400],
    },
  },
  
  // 变体样式
  variants: {
    default: {
      backgroundColor: colors.slate[700],
      border: `1px solid ${colors.slate[600]}`,
    },
    filled: {
      backgroundColor: colors.slate[600],
      border: '1px solid transparent',
    },
    outlined: {
      backgroundColor: 'transparent',
      border: `2px solid ${colors.slate[500]}`,
    },
  },
  
  // 尺寸样式
  sizes: {
    sm: {
      padding: `${spacing[2]} ${spacing[3]}`,
      fontSize: textStyles.body.small.fontSize,
    },
    base: {
      padding: `${spacing[3]} ${spacing[4]}`,
      fontSize: textStyles.body.base.fontSize,
    },
    lg: {
      padding: `${spacing[4]} ${spacing[4]}`,
      fontSize: textStyles.body.large.fontSize,
    },
  },
}

// Input组件
export const Input: React.FC<InputProps> = ({
  variant = 'default',
  inputSize = 'base',
  label,
  error,
  helper,
  icon,
  iconPosition = 'left',
  fullWidth = true,
  className = '',
  style,
  ...props
}) => {
  // 样式计算
  const baseStyle = inputStyles.base
  const variantStyle = inputStyles.variants[variant]
  const sizeStyle = inputStyles.sizes[inputSize]
  
  // 组合样式
  const combinedStyle = {
    ...baseStyle,
    ...variantStyle,
    ...sizeStyle,
    ...(error && {
      borderColor: colors.error[500],
      boxShadow: `0 0 0 3px ${colors.error[500]}20`,
    }),
    paddingLeft: icon && iconPosition === 'left' ? spacing[10] : sizeStyle.paddingLeft || sizeStyle.padding,
    paddingRight: icon && iconPosition === 'right' ? spacing[10] : sizeStyle.paddingRight || sizeStyle.padding,
    width: fullWidth ? '100%' : 'auto',
    ...style,
  }

  return (
    <div style={{ width: fullWidth ? '100%' : 'auto' }}>
      {/* 标签 */}
      {label && (
        <label style={{
          display: 'block',
          fontSize: textStyles.label.base.fontSize,
          fontWeight: textStyles.label.base.fontWeight,
          color: colors.slate[200],
          marginBottom: spacing[2],
        }}>
          {label}
        </label>
      )}
      
      {/* 输入框容器 */}
      <div style={{ position: 'relative', width: '100%' }}>
        {/* 图标 */}
        {icon && (
          <div style={{
            position: 'absolute',
            [iconPosition]: spacing[3],
            top: '50%',
            transform: 'translateY(-50%)',
            color: colors.slate[400],
            pointerEvents: 'none',
          }}>
            {icon}
          </div>
        )}
        
        {/* 输入框 */}
        <motion.input
          whileFocus={{ scale: 1.01 }}
          className={`ai-input ai-input--${variant} ai-input--${inputSize} ${className}`}
          style={combinedStyle}
          {...props}
        />
      </div>
      
      {/* 错误信息 */}
      {error && (
        <p style={{
          fontSize: textStyles.body.small.fontSize,
          color: colors.error[500],
          marginTop: spacing[1],
        }}>
          {error}
        </p>
      )}
      
      {/* 帮助文本 */}
      {helper && !error && (
        <p style={{
          fontSize: textStyles.body.small.fontSize,
          color: colors.slate[400],
          marginTop: spacing[1],
        }}>
          {helper}
        </p>
      )}
    </div>
  )
}

export default Input