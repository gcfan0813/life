import React, { useState, useEffect } from 'react'
import { AlertTriangle, Heart, SkipForward, Shield, Info } from 'lucide-react'
import { apiService } from '../services/api'

interface SensitiveEventDialogProps {
  eventId: string
  eventName: string
  onChoice: (mode: 'skip' | 'soften' | 'full') => void
  onClose: () => void
}

const SensitiveEventDialog: React.FC<SensitiveEventDialogProps> = ({
  eventId,
  eventName,
  onChoice,
  onClose
}) => {
  const [options, setOptions] = useState<{
    title: string
    description: string
    options: Array<{ id: string; label: string; description: string }>
    support_resources: string[]
    warning: string
    sensitivity_level: string
  } | null>(null)
  const [selectedOption, setSelectedOption] = useState<string>('soften')
  const [isLoading, setIsLoading] = useState(true)
  const [showResources, setShowResources] = useState(false)

  useEffect(() => {
    loadOptions()
  }, [eventId])

  const loadOptions = async () => {
    setIsLoading(true)
    try {
      const response = await apiService.getSensitiveEventOptions(eventId)
      if (response.success && response.data) {
        setOptions(response.data as any)
      }
    } catch (error) {
      console.error('加载高敏事件选项失败:', error)
    }
    setIsLoading(false)
  }

  const handleConfirm = () => {
    onChoice(selectedOption as 'skip' | 'soften' | 'full')
  }

  const getLevelColor = (level: string) => {
    switch (level) {
      case 'critical': return 'text-red-600 bg-red-50'
      case 'high': return 'text-orange-600 bg-orange-50'
      case 'medium': return 'text-yellow-600 bg-yellow-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  const getLevelLabel = (level: string) => {
    switch (level) {
      case 'critical': return '极高敏感'
      case 'high': return '高敏感'
      case 'medium': return '中敏感'
      default: return '低敏感'
    }
  }

  if (isLoading) {
    return (
      <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
        <div className="bg-white rounded-lg p-6">
          <div className="animate-spin rounded-full h-8 w-8 border-2 border-indigo-600 border-t-transparent mx-auto"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-xl shadow-xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
        {/* 头部 */}
        <div className="bg-gradient-to-r from-slate-800 to-slate-700 text-white p-4 rounded-t-xl">
          <div className="flex items-center space-x-3">
            <div className="p-2 bg-white/20 rounded-lg">
              <AlertTriangle className="w-6 h-6" />
            </div>
            <div>
              <h2 className="text-lg font-semibold">高敏感事件提示</h2>
              <p className="text-sm text-slate-300">{options?.title || eventName}</p>
            </div>
          </div>
        </div>

        {/* 内容 */}
        <div className="p-4 space-y-4">
          {/* 警告信息 */}
          <div className={`p-3 rounded-lg ${getLevelColor(options?.sensitivity_level || 'medium')}`}>
            <div className="flex items-start space-x-2">
              <Info className="w-5 h-5 flex-shrink-0 mt-0.5" />
              <div>
                <p className="font-medium">{options?.warning}</p>
                <p className="text-sm mt-1">
                  敏感度级别: <span className="font-medium">{getLevelLabel(options?.sensitivity_level || 'medium')}</span>
                </p>
              </div>
            </div>
          </div>

          {/* 描述 */}
          {options?.description && (
            <p className="text-gray-600 text-sm">{options.description}</p>
          )}

          {/* 处理选项 */}
          <div className="space-y-3">
            <h3 className="font-medium text-gray-800">请选择处理方式：</h3>
            
            {options?.options.map((option) => (
              <label
                key={option.id}
                className={`flex items-start space-x-3 p-3 rounded-lg border-2 cursor-pointer transition-colors ${
                  selectedOption === option.id
                    ? 'border-indigo-500 bg-indigo-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <input
                  type="radio"
                  name="handling"
                  value={option.id}
                  checked={selectedOption === option.id}
                  onChange={(e) => setSelectedOption(e.target.value)}
                  className="mt-1"
                />
                <div>
                  <p className="font-medium text-gray-800">{option.label}</p>
                  <p className="text-sm text-gray-600">{option.description}</p>
                </div>
              </label>
            ))}
          </div>

          {/* 支持资源 */}
          <div className="border-t pt-4">
            <button
              onClick={() => setShowResources(!showResources)}
              className="flex items-center space-x-2 text-sm text-indigo-600 hover:text-indigo-700"
            >
              <Heart className="w-4 h-4" />
              <span>支持资源与帮助</span>
            </button>
            
            {showResources && options?.support_resources && (
              <div className="mt-3 p-3 bg-blue-50 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-2">如果您需要帮助：</h4>
                <ul className="space-y-1">
                  {options.support_resources.map((resource, index) => (
                    <li key={index} className="text-sm text-blue-700 flex items-start space-x-2">
                      <span className="text-blue-400">•</span>
                      <span>{resource}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>

        {/* 按钮 */}
        <div className="flex space-x-3 p-4 border-t bg-gray-50 rounded-b-xl">
          <button
            onClick={onClose}
            className="flex-1 px-4 py-2 text-gray-600 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors"
          >
            取消
          </button>
          <button
            onClick={handleConfirm}
            className="flex-1 px-4 py-2 text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors flex items-center justify-center space-x-2"
          >
            {selectedOption === 'skip' && <SkipForward className="w-4 h-4" />}
            {selectedOption === 'soften' && <Shield className="w-4 h-4" />}
            {selectedOption === 'full' && <Heart className="w-4 h-4" />}
            <span>确认选择</span>
          </button>
        </div>
      </div>
    </div>
  )
}

export default SensitiveEventDialog
