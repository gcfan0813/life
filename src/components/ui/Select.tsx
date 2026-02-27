// AI人生模拟器 - Select组件
// 基于设计系统的现代化选择器组件

import React from 'react'
import { motion } from 'framer-motion'
import { colors, opacityColors } from '../../design-system/colors'
import { spacing, borderRadius } from '../../design-system/spacing'
import { textStyles } from '../../design-system/typography'

// 选择器变体类型
export type SelectVariant = 'default' | 'filled' | 'outlined'
export type SelectSize = 'sm' | 'base' | 'lg'

// 选项接口
export interface SelectOption {
  value: string
  label: string
  disabled?: boolean
}

// 选择器属性接口
export interface SelectProps {
  variant?: SelectVariant
  selectSize?: SelectSize
  label?: string
  error?: string
  helper?: string
  options: SelectOption[]
  value?: string
  onChange?: (value: string) => void
  placeholder?: string
  disabled?: boolean
  fullWidth?: boolean
  className?: string
}

// 选择器样式配置
const selectStyles = {
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
    cursor: 'pointer',
    appearance: 'none',
    width: '100%',
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
      padding: `${spacing[2]} ${spacing[8]} ${spacing[2]} ${spacing[3]}`,
      fontSize: textStyles.body.small.fontSize,
    },
    base: {
      padding: `${spacing[3]} ${spacing[10]} ${spacing[3]} ${spacing[4]}`,
      fontSize: textStyles.body.base.fontSize,
    },
    lg: {
      padding: `${spacing[4]} ${spacing[12]} ${spacing[4]} ${spacing[4]}`,
      fontSize: textStyles.body.large.fontSize,
    },
  },
}

// Select组件
export const Select: React.FC<SelectProps> = ({
  variant = 'default',
  selectSize = 'base',
  label,
  error,
  helper,
  options,
  value,
  onChange,
  placeholder = '请选择...',
  disabled = false,
  fullWidth = true,
  className = '',
}) => {
  // 样式计算
  const baseStyle = selectStyles.base
  const variantStyle = selectStyles.variants[variant]
  const sizeStyle = selectStyles.sizes[selectSize]
  
  // 组合样式
  const combinedStyle = {
    ...baseStyle,
    ...variantStyle,
    ...sizeStyle,
    ...(error && {
      borderColor: colors.error[500],
      boxShadow: `0 0 0 3px ${colors.error[500]}20`,
    }),
    opacity: disabled ? 0.6 : 1,
    cursor: disabled ? 'not-allowed' : 'pointer',
  }

  const handleChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    if (!disabled && onChange) {
      onChange(e.target.value)
    }
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
      
      {/* 选择器容器 */}
      <div style={{ position: 'relative', width: '100%' }}>
        {/* 下拉箭头 */}
        <div style={{
          position: 'absolute',
          right: spacing[3],
          top: '50%',
          transform: 'translateY(-50%)',
          color: colors.slate[400],
          pointerEvents: 'none',
        }}>
          ▼
        </div>
        
        {/* 选择器 */}
        <motion.select
          whileFocus={{ scale: 1.01 }}
          value={value}
          onChange={handleChange}
          disabled={disabled}
          className={`ai-select ai-select--${variant} ai-select--${selectSize} ${className}`}
          style={combinedStyle}
        >
          {/* 占位符选项 */}
          <option value="" disabled>
            {placeholder}
          </option>
          
          {/* 选项列表 */}
          {options.map((option) => (
            <option
              key={option.value}
              value={option.value}
              disabled={option.disabled}
            >
              {option.label}
            </option>
          ))}
        </motion.select>
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

export default Select