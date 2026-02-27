// AI人生模拟器 - Slider组件
// 基于设计系统的现代化滑块组件

import React from 'react'
import { motion } from 'framer-motion'
import { colors, opacityColors } from '../../design-system/colors'
import { spacing, borderRadius } from '../../design-system/spacing'
import { textStyles } from '../../design-system/typography'

// 滑块属性接口
export interface SliderProps {
  label?: string
  value: number
  onChange: (value: number) => void
  min?: number
  max?: number
  step?: number
  showValue?: boolean
  showLabels?: boolean
  leftLabel?: string
  rightLabel?: string
  disabled?: boolean
  fullWidth?: boolean
  className?: string
}

// 滑块样式配置
const sliderStyles = {
  // 容器样式
  container: {
    width: '100%',
  },
  
  // 轨道样式
  track: {
    width: '100%',
    height: '8px',
    backgroundColor: colors.slate[600],
    borderRadius: borderRadius.full,
    position: 'relative' as const,
    cursor: 'pointer',
  },
  
  // 已填充部分样式
  fill: {
    height: '100%',
    background: `linear-gradient(to right, ${colors.primary[500]}, ${colors.primary[600]})`,
    borderRadius: borderRadius.full,
    transition: 'width 0.2s ease-in-out',
  },
  
  // 滑块样式
  thumb: {
    width: '20px',
    height: '20px',
    backgroundColor: colors.primary[500],
    border: `3px solid ${colors.slate[50]}`,
    borderRadius: '50%',
    position: 'absolute' as const,
    top: '50%',
    transform: 'translateY(-50%)',
    cursor: 'grab',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.2)',
    transition: 'transform 0.2s ease-in-out',
  },
}

// Slider组件
export const Slider: React.FC<SliderProps> = ({
  label,
  value,
  onChange,
  min = 0,
  max = 100,
  step = 1,
  showValue = true,
  showLabels = false,
  leftLabel,
  rightLabel,
  disabled = false,
  fullWidth = true,
  className = '',
}) => {
  // 计算百分比
  const percentage = ((value - min) / (max - min)) * 100

  // 处理滑块拖动
  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!disabled) {
      const newValue = parseFloat(e.target.value)
      onChange(newValue)
    }
  }

  return (
    <div style={{ ...sliderStyles.container, width: fullWidth ? '100%' : 'auto' }} className={className}>
      {/* 标签和数值显示 */}
      {(label || showValue) && (
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: spacing[3],
        }}>
          {label && (
            <label style={{
              fontSize: textStyles.label.base.fontSize,
              fontWeight: textStyles.label.base.fontWeight,
              color: colors.slate[200],
            }}>
              {label}
            </label>
          )}
          {showValue && (
            <span style={{
              fontSize: textStyles.data.base.fontSize,
              fontWeight: textStyles.data.base.fontWeight,
              color: colors.primary[400],
              fontFamily: textStyles.data.base.fontFamily,
            }}>
              {value}
            </span>
          )}
        </div>
      )}
      
      {/* 滑块轨道 */}
      <div style={{ position: 'relative' }}>
        <div style={sliderStyles.track}>
          {/* 已填充部分 */}
          <div style={{
            ...sliderStyles.fill,
            width: `${percentage}%`,
          }} />
        </div>
        
        {/* 滑块 */}
        <motion.div
          style={{
            ...sliderStyles.thumb,
            left: `calc(${percentage}% - 10px)`,
          }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9, cursor: 'grabbing' }}
        />
        
        {/* 隐藏的原生滑块 */}
        <input
          type="range"
          min={min}
          max={max}
          step={step}
          value={value}
          onChange={handleSliderChange}
          disabled={disabled}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            opacity: 0,
            cursor: disabled ? 'not-allowed' : 'pointer',
            margin: 0,
          }}
        />
      </div>
      
      {/* 两端标签 */}
      {showLabels && (leftLabel || rightLabel) && (
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          marginTop: spacing[2],
        }}>
          <span style={{
            fontSize: textStyles.body.small.fontSize,
            color: colors.slate[400],
          }}>
            {leftLabel}
          </span>
          <span style={{
            fontSize: textStyles.body.small.fontSize,
            color: colors.slate[400],
          }}>
            {rightLabel}
          </span>
        </div>
      )}
    </div>
  )
}

export default Slider