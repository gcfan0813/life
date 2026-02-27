// AI人生模拟器色彩系统
// 基于设计Token的色彩配置

import { colors } from './tokens'

// 语义化色彩定义
export const semanticColors = {
  // 背景色
  background: {
    primary: colors.slate[900],
    secondary: colors.slate[800],
    tertiary: colors.slate[700],
    elevated: colors.slate[600],
  },
  
  // 表面色（卡片、面板等）
  surface: {
    primary: colors.slate[800],
    secondary: colors.slate[700],
    tertiary: colors.slate[600],
    elevated: colors.slate[500],
  },
  
  // 文字色
  text: {
    primary: colors.slate[50],
    secondary: colors.slate[200],
    tertiary: colors.slate[300],
    muted: colors.slate[400],
    disabled: colors.slate[500],
  },
  
  // 边框色
  border: {
    primary: colors.slate[700],
    secondary: colors.slate[600],
    tertiary: colors.slate[500],
    focus: colors.primary[500],
  },
  
  // 状态色
  status: {
    success: colors.success[500],
    warning: colors.warning[500],
    error: colors.error[500],
    info: colors.primary[500],
  },
  
  // 交互色
  interactive: {
    primary: colors.primary[500],
    secondary: colors.secondary[500],
    hover: colors.primary[400],
    active: colors.primary[600],
    disabled: colors.slate[600],
  },
} as const

// 渐变色定义
export const gradients = {
  // 主色调渐变
  primary: {
    from: colors.primary[500],
    to: colors.primary[700],
    via: colors.primary[600],
  },
  
  // 辅助色渐变
  secondary: {
    from: colors.secondary[400],
    to: colors.secondary[600],
    via: colors.secondary[500],
  },
  
  // 成功色渐变
  success: {
    from: colors.success[400],
    to: colors.success[600],
    via: colors.success[500],
  },
  
  // 错误色渐变
  error: {
    from: colors.error[400],
    to: colors.error[600],
    via: colors.error[500],
  },
  
  // 背景渐变
  background: {
    primary: {
      from: colors.slate[900],
      to: colors.slate[800],
    },
    secondary: {
      from: colors.slate[800],
      to: colors.slate[700],
    },
  },
  
  // AI主题渐变
  ai: {
    from: colors.primary[600],
    to: colors.secondary[500],
    via: colors.primary[500],
  },
} as const

// 透明度色彩
export const opacityColors = {
  // 黑色透明度
  black: {
    5: 'rgba(0, 0, 0, 0.05)',
    10: 'rgba(0, 0, 0, 0.1)',
    20: 'rgba(0, 0, 0, 0.2)',
    30: 'rgba(0, 0, 0, 0.3)',
    40: 'rgba(0, 0, 0, 0.4)',
    50: 'rgba(0, 0, 0, 0.5)',
    60: 'rgba(0, 0, 0, 0.6)',
    70: 'rgba(0, 0, 0, 0.7)',
    80: 'rgba(0, 0, 0, 0.8)',
    90: 'rgba(0, 0, 0, 0.9)',
  },
  
  // 白色透明度
  white: {
    5: 'rgba(255, 255, 255, 0.05)',
    10: 'rgba(255, 255, 255, 0.1)',
    20: 'rgba(255, 255, 255, 0.2)',
    30: 'rgba(255, 255, 255, 0.3)',
    40: 'rgba(255, 255, 255, 0.4)',
    50: 'rgba(255, 255, 255, 0.5)',
    60: 'rgba(255, 255, 255, 0.6)',
    70: 'rgba(255, 255, 255, 0.7)',
    80: 'rgba(255, 255, 255, 0.8)',
    90: 'rgba(255, 255, 255, 0.9)',
  },
  
  // 主色透明度
  primary: {
    5: `rgba(59, 130, 246, 0.05)`,
    10: `rgba(59, 130, 246, 0.1)`,
    20: `rgba(59, 130, 246, 0.2)`,
    30: `rgba(59, 130, 246, 0.3)`,
    40: `rgba(59, 130, 246, 0.4)`,
    50: `rgba(59, 130, 246, 0.5)`,
  },
} as const

// 主题配置
export const theme = {
  colors: semanticColors,
  gradients,
  opacityColors,
} as const

// Tailwind CSS 色彩配置
export const tailwindColors = {
  // 扩展主色调
  primary: colors.primary,
  secondary: colors.secondary,
  success: colors.success,
  warning: colors.warning,
  error: colors.error,
  
  // 语义化色彩
  background: semanticColors.background,
  surface: semanticColors.surface,
  text: semanticColors.text,
  border: semanticColors.border,
  
  // 保留slate中性色
  slate: colors.slate,
}

export type SemanticColors = typeof semanticColors
export type Gradients = typeof gradients
export type OpacityColors = typeof opacityColors

export default theme