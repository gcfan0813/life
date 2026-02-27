// AI人生模拟器 - UI组件库导出
// 统一导出所有基础UI组件

// 导出组件
export { Button } from './Button'
export { Card, CardHeader, CardContent, CardFooter } from './Card'
export { Input } from './Input'
export { Select } from './Select'
export { Slider } from './Slider'

// 导出类型
export type { ButtonProps, ButtonVariant, ButtonSize } from './Button'
export type { CardProps, CardVariant, CardPadding, CardHeaderProps, CardContentProps, CardFooterProps } from './Card'
export type { InputProps, InputVariant, InputSize } from './Input'
export type { SelectProps, SelectVariant, SelectSize, SelectOption } from './Select'
export type { SliderProps } from './Slider'

// 默认导出
export default {
  Button,
  Card,
  Input,
  Select,
  Slider,
}