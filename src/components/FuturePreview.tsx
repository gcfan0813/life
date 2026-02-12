import React, { useState, useEffect } from 'react'
import { apiService } from '../services/api'

interface Prediction {
  type: string
  title: string
  description: string
  probability: number
  suggestion: string
}

interface PreviewData {
  previewDays: number
  currentAge: number
  currentStage: string
  currentDimensions: Record<string, number>
  predictions: Prediction[]
  generatedAt: string
}

interface FuturePreviewProps {
  profileId: string
}

const FuturePreview: React.FC<FuturePreviewProps> = ({ profileId }) => {
  const [previewData, setPreviewData] = useState<PreviewData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [days, setDays] = useState(90)

  const fetchPreview = async () => {
    if (!profileId) return
    
    setLoading(true)
    setError(null)
    
    try {
      const response = await apiService.previewFuture(profileId, days)
      if (response.success && response.data) {
        setPreviewData(response.data)
      } else {
        setError(response.error || '获取预览失败')
      }
    } catch (err) {
      setError('网络请求失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchPreview()
  }, [profileId, days])

  const getProbabilityColor = (probability: number) => {
    if (probability >= 0.8) return 'bg-red-100 text-red-800'
    if (probability >= 0.6) return 'bg-yellow-100 text-yellow-800'
    return 'bg-green-100 text-green-800'
  }

  const getTypeIcon = (type: string) => {
    const icons: Record<string, string> = {
      health_warning: '🏥',
      energy_warning: '⚡',
      financial_warning: '💰',
      career: '💼',
      relationship: '💕',
      family: '👨‍👩‍👧',
      wealth: '📈',
      social_opportunity: '🤝',
      retirement: '🌴',
      health: '❤️'
    }
    return icons[type] || '📌'
  }

  if (!profileId) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center text-gray-500">
        请先创建角色
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-lg p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-bold text-gray-800">🔮 未来预览</h2>
        <div className="flex items-center gap-2">
          <label className="text-sm text-gray-600">预测天数:</label>
          <select 
            value={days} 
            onChange={(e) => setDays(Number(e.target.value))}
            className="border rounded px-2 py-1 text-sm"
          >
            <option value={30}>30天</option>
            <option value={90}>90天</option>
            <option value={180}>180天</option>
            <option value={365}>365天</option>
          </select>
          <button 
            onClick={fetchPreview}
            disabled={loading}
            className="px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700 disabled:opacity-50"
          >
            {loading ? '加载中...' : '刷新'}
          </button>
        </div>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded mb-4">
          {error}
        </div>
      )}

      {previewData && (
        <div className="space-y-4">
          {/* 当前状态概览 */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="text-gray-500">当前年龄:</span>
                <p className="font-semibold">{previewData.currentAge}岁</p>
              </div>
              <div>
                <span className="text-gray-500">人生阶段:</span>
                <p className="font-semibold">{previewData.currentStage}</p>
              </div>
              <div>
                <span className="text-gray-500">预测天数:</span>
                <p className="font-semibold">{previewData.previewDays}天</p>
              </div>
              <div>
                <span className="text-gray-500">预测数量:</span>
                <p className="font-semibold">{previewData.predictions.length}条</p>
              </div>
            </div>
          </div>

          {/* 维度状态 */}
          <div className="grid grid-cols-5 gap-2">
            {Object.entries(previewData.currentDimensions).map(([key, value]) => (
              <div key={key} className="text-center">
                <div className="text-xs text-gray-500 capitalize">{key}</div>
                <div className={`h-2 rounded-full ${
                  value >= 70 ? 'bg-green-500' : value >= 40 ? 'bg-yellow-500' : 'bg-red-500'
                }`} style={{ width: `${value}%` }}></div>
                <div className="text-xs font-semibold">{Math.round(value)}</div>
              </div>
            ))}
          </div>

          {/* 预测列表 */}
          <div className="space-y-2">
            <h3 className="font-semibold text-gray-700">预测事件</h3>
            {previewData.predictions.length === 0 ? (
              <p className="text-gray-500 text-sm">暂无预测</p>
            ) : (
              previewData.predictions.map((prediction, index) => (
                <div 
                  key={index}
                  className="border rounded-lg p-3 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex items-center gap-2">
                      <span className="text-xl">{getTypeIcon(prediction.type)}</span>
                      <div>
                        <h4 className="font-medium">{prediction.title}</h4>
                        <p className="text-sm text-gray-600">{prediction.description}</p>
                      </div>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs ${getProbabilityColor(prediction.probability)}`}>
                      {Math.round(prediction.probability * 100)}%
                    </span>
                  </div>
                  {prediction.suggestion && (
                    <div className="mt-2 text-sm text-indigo-600 bg-indigo-50 p-2 rounded">
                      💡 建议: {prediction.suggestion}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>

          <div className="text-xs text-gray-400 text-right">
            预测生成时间: {new Date(previewData.generatedAt).toLocaleString()}
          </div>
        </div>
      )}
    </div>
  )
}

export default FuturePreview
