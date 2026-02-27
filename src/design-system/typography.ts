// AI人生模拟器字体系统
// 基于设计Token的字体配置

import { typography } from './tokens'

// 字体大小配置
export const fontSizes = typography.fontSize

// 字体粗细配置
export const fontWeights = typography.fontWeight

// 行高配置
export const lineHeights = typography.lineHeight

// 字体家族配置
export const fontFamilies = typography.fontFamily

// 预定义字体样式
export const textStyles = {
  // 标题样式
  heading: {
    h1: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes['5xl'],
      fontWeight: fontWeights.bold,
      lineHeight: lineHeights.tight,
    },
    h2: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes['4xl'],
      fontWeight: fontWeights.bold,
      lineHeight: lineHeights.tight,
    },
    h3: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes['3xl'],
      fontWeight: fontWeights.semibold,
      lineHeight: lineHeights.tight,
    },
    h4: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes['2xl'],
      fontWeight: fontWeights.semibold,
      lineHeight: lineHeights.normal,
    },
    h5: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes.xl,
      fontWeight: fontWeights.medium,
      lineHeight: lineHeights.normal,
    },
    h6: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes.lg,
      fontWeight: fontWeights.medium,
      lineHeight: lineHeights.normal,
    },
  },
  
  // 正文样式
  body: {
    large: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes.lg,
      fontWeight: fontWeights.normal,
      lineHeight: lineHeights.relaxed,
    },
    base: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes.base,
      fontWeight: fontWeights.normal,
      lineHeight: lineHeights.normal,
    },
    small: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes.sm,
      fontWeight: fontWeights.normal,
      lineHeight: lineHeights.normal,
    },
  },
  
  // 标签样式
  label: {
    large: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes.base,
      fontWeight: fontWeights.medium,
      lineHeight: lineHeights.normal,
    },
    base: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes.sm,
      fontWeight: fontWeights.medium,
      lineHeight: lineHeights.normal,
    },
    small: {
      fontFamily: fontFamilies.sans.join(', '),
      fontSize: fontSizes.xs,
      fontWeight: fontWeights.medium,
      lineHeight: lineHeights.normal,
    },
  },
  
  // 代码样式
  code: {
    inline: {
      fontFamily: fontFamilies.mono.join(', '),
      fontSize: fontSizes.sm,
      fontWeight: fontWeights.normal,
      lineHeight: lineHeights.normal,
    },
    block: {
      fontFamily: fontFamilies.mono.join(', '),
      fontSize: fontSizes.sm,
      fontWeight: fontWeights.normal,
      lineHeight: lineHeights.relaxed,
    },
  },
  
  // 数据展示样式
  data: {
    display: {
      fontFamily: fontFamilies.mono.join(', '),
      fontSize: fontSizes['4xl'],
      fontWeight: fontWeights.bold,
      lineHeight: lineHeights.tight,
    },
    large: {
      fontFamily: fontFamilies.mono.join(', '),
      fontSize: fontSizes['2xl'],
      fontWeight: fontWeights.semibold,
      lineHeight: lineHeights.tight,
    },
    base: {
      fontFamily: fontFamilies.mono.join(', '),
      fontSize: fontSizes.base,
      fontWeight: fontWeights.medium,
      lineHeight: lineHeights.normal,
    },
  },
} as const

// 字体样式工具函数
export const getFontStyle = (
  category: keyof typeof textStyles,
  variant: string
) => {
  const categoryStyles = textStyles[category]
  return categoryStyles[variant as keyof typeof categoryStyles] || categoryStyles.base
}

// Tailwind CSS 字体配置
export const tailwindTypography = {
  fontFamily: {
    sans: fontFamilies.sans,
    mono: fontFamilies.mono,
  },
  fontSize: fontSizes,
  fontWeight: fontWeights,
  lineHeight: lineHeights,
}

export type TextStyles = typeof textStyles
export default textStyles