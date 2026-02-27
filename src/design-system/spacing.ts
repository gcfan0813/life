// AI人生模拟器间距和布局系统
// 基于设计Token的间距配置

import { spacing, borderRadius, screens } from './tokens'

// 间距配置
export const spacingScale = spacing

// 圆角配置
export const borderRadiusScale = borderRadius

// 屏幕断点配置
export const breakpoints = screens

// 布局网格系统
export const layout = {
  // 容器最大宽度
  container: {
    xs: '475px',
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
  
  // 栅格系统
  grid: {
    columns: 12,
    gap: spacing[6],
    gapX: spacing[6],
    gapY: spacing[6],
  },
  
  // 页面内边距
  padding: {
    page: {
      mobile: spacing[4],
      tablet: spacing[6],
      desktop: spacing[8],
    },
    section: {
      mobile: spacing[6],
      tablet: spacing[8],
      desktop: spacing[12],
    },
  },
  
  // 页面外边距
  margin: {
    section: {
      mobile: spacing[8],
      tablet: spacing[12],
      desktop: spacing[16],
    },
  },
} as const

// 组件间距预设
export const componentSpacing = {
  // 卡片内边距
  card: {
    sm: spacing[4],
    base: spacing[6],
    lg: spacing[8],
  },
  
  // 按钮内边距
  button: {
    sm: {
      x: spacing[3],
      y: spacing[2],
    },
    base: {
      x: spacing[4],
      y: spacing[2],
    },
    lg: {
      x: spacing[6],
      y: spacing[3],
    },
  },
  
  // 输入框内边距
  input: {
    sm: {
      x: spacing[3],
      y: spacing[2],
    },
    base: {
      x: spacing[4],
      y: spacing[3],
    },
    lg: {
      x: spacing[4],
      y: spacing[4],
    },
  },
  
  // 列表项间距
  listItem: {
    base: spacing[3],
    lg: spacing[4],
  },
  
  // 标签间距
  badge: {
    x: spacing[2],
    y: spacing[1],
  },
} as const

// 间距工具函数
export const getSpacing = (size: keyof typeof spacing) => spacing[size]

// 响应式间距工具
export const getResponsiveSpacing = (
  mobile: keyof typeof spacing,
  tablet?: keyof typeof spacing,
  desktop?: keyof typeof spacing
) => ({
  mobile: spacing[mobile],
  tablet: tablet ? spacing[tablet] : spacing[mobile],
  desktop: desktop ? spacing[desktop] : tablet ? spacing[tablet] : spacing[mobile],
})

// Tailwind CSS 间距配置
export const tailwindSpacing = {
  spacing: spacingScale,
  borderRadius: borderRadiusScale,
  screens: breakpoints,
}

export type Layout = typeof layout
export type ComponentSpacing = typeof componentSpacing

export default {
  spacing: spacingScale,
  borderRadius: borderRadiusScale,
  breakpoints,
  layout,
  componentSpacing,
}