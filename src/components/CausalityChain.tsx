import React, { useState, useEffect } from 'react'
import { apiService } from '../services/api'

interface EventNode {
  id: string
  title: string
  date: string
  type: string
  isCompleted: boolean
  emotionalWeight: number
}

interface EventLink {
  source: string
  target: string
  type: string
}

interface CausalityData {
  nodes: EventNode[]
  links: EventLink[]
  stats: {
    totalEvents: number
    typeDistribution: Record<string, number>
    completedEvents: number
    pendingEvents: number
  }
}

interface CausalityChainProps {
  profileId: string
}

const CausalityChain: React.FC<CausalityChainProps> = ({ profileId }) => {
  const [data, setData] = useState<CausalityData | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedEvent, setSelectedEvent] = useState<string | null>(null)
  const [detailData, setDetailData] = useState<any>(null)

  const fetchCausality = async () => {
    if (!profileId) return
    
    setLoading(true)
    setError(null)
    
    try {
      const response = await apiService.getFullCausalityChain(profileId)
      if (response.success && response.data) {
        setData(response.data)
      } else {
        setError(response.error || '获取因果链失败')
      }
    } catch (err) {
      setError('网络请求失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchCausality()
  }, [profileId])

  const fetchEventDetail = async (eventId: string) => {
    setSelectedEvent(eventId)
    try {
      const response = await apiService.getEventCausality(profileId, eventId)
      if (response.success && response.data) {
        setDetailData(response.data)
      }
    } catch (err) {
      console.error('获取事件详情失败', err)
    }
  }

  const getTypeColor = (type: string) => {
    const colors: Record<string, string> = {
      career: 'bg-blue-100 border-blue-400',
      health: 'bg-red-100 border-red-400',
      relationship: 'bg-pink-100 border-pink-400',
      education: 'bg-yellow-100 border-yellow-400',
      finance: 'bg-green-100 border-green-400',
      family: 'bg-purple-100 border-purple-400',
      social: 'bg-indigo-100 border-indigo-400'
    }
    return colors[type] || 'bg-gray-100 border-gray-400'
  }

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      career: '职业',
      health: '健康',
      relationship: '情感',
      education: '教育',
      finance: '财务',
      family: '家庭',
      social: '社交'
    }
    return labels[type] || type
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
        <h2 className="text-xl font-bold text-gray-800">🔗 因果链追溯</h2>
        <button 
          onClick={fetchCausality}
          disabled={loading}
          className="px-3 py-1 bg-indigo-600 text-white rounded text-sm hover:bg-indigo-700 disabled:opacity-50"
        >
          {loading ? '加载中...' : '刷新'}
        </button>
      </div>

      {error && (
        <div className="bg-red-50 text-red-600 p-3 rounded mb-4">
          {error}
        </div>
      )}

      {data && (
        <div className="space-y-4">
          {/* 统计信息 */}
          <div className="bg-gray-50 rounded-lg p-4">
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
              <div className="text-center">
                <div className="text-2xl font-bold text-indigo-600">{data.stats.totalEvents}</div>
                <div className="text-gray-500">总事件数</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{data.stats.completedEvents}</div>
                <div className="text-gray-500">已完成</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-yellow-600">{data.stats.pendingEvents}</div>
                <div className="text-gray-500">待处理</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{data.nodes.length > 0 ? Math.round(data.stats.completedEvents / data.stats.totalEvents * 100) : 0}%</div>
                <div className="text-gray-500">完成率</div>
              </div>
            </div>
          </div>

          {/* 事件类型分布 */}
          <div className="flex flex-wrap gap-2">
            {Object.entries(data.stats.typeDistribution).map(([type, count]) => (
              <span 
                key={type}
                className={`px-3 py-1 rounded-full text-xs font-medium border ${getTypeColor(type)}`}
              >
                {getTypeLabel(type)}: {count}
              </span>
            ))}
          </div>

          {/* 事件列表 */}
          <div className="border rounded-lg overflow-hidden">
            <div className="bg-gray-50 px-4 py-2 font-medium text-sm text-gray-600">
              事件因果网络（点击查看详情）
            </div>
            <div className="max-h-96 overflow-y-auto">
              {data.nodes.length === 0 ? (
                <div className="p-8 text-center text-gray-500">
                  暂无事件数据
                </div>
              ) : (
                <div className="divide-y">
                  {data.nodes.map((node) => (
                    <div 
                      key={node.id}
                      onClick={() => fetchEventDetail(node.id)}
                      className={`p-3 cursor-pointer hover:bg-gray-50 transition-colors ${
                        selectedEvent === node.id ? 'bg-indigo-50' : ''
                      }`}
                    >
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <span className={`w-2 h-2 rounded-full ${
                            node.isCompleted ? 'bg-green-500' : 'bg-yellow-500'
                          }`}></span>
                          <span className="font-medium">{node.title}</span>
                          <span className={`px-2 py-0.5 rounded text-xs ${getTypeColor(node.type)}`}>
                            {getTypeLabel(node.type)}
                          </span>
                        </div>
                        <div className="text-sm text-gray-500">{node.date}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          {/* 事件详情 */}
          {detailData && selectedEvent && (
            <div className="border rounded-lg p-4 bg-indigo-50">
              <div className="flex justify-between items-start mb-3">
                <h3 className="font-bold text-lg">{detailData.event.title}</h3>
                <button 
                  onClick={() => setSelectedEvent(null)}
                  className="text-gray-500 hover:text-gray-700"
                >
                  ✕
                </button>
              </div>
              
              <p className="text-sm text-gray-600 mb-4">{detailData.event.description}</p>
              
              {detailData.event.narrative && (
                <div className="bg-white rounded p-3 mb-4 text-sm">
                  <div className="font-medium mb-1">叙事:</div>
                  {detailData.event.narrative}
                </div>
              )}

              {/* 决策信息 */}
              {detailData.decision && (
                <div className="bg-green-50 rounded p-3 mb-4">
                  <div className="text-sm">
                    <span className="font-medium">您的选择:</span> {detailData.decision.choice}
                  </div>
                </div>
              )}

              {/* 因果链 */}
              <div className="grid grid-cols-2 gap-4">
                {/* 原因 */}
                <div>
                  <h4 className="font-medium text-sm text-gray-700 mb-2">📍 原因事件</h4>
                  {detailData.causes.length === 0 ? (
                    <p className="text-sm text-gray-400">暂无原因记录</p>
                  ) : (
                    <div className="space-y-2">
                      {detailData.causes.map((cause: any) => (
                        <div key={cause.id} className="bg-white rounded p-2 text-sm">
                          <div className="font-medium">{cause.title}</div>
                          <div className="text-xs text-gray-500">{cause.date}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* 结果 */}
                <div>
                  <h4 className="font-medium text-sm text-gray-700 mb-2">📎 结果事件</h4>
                  {detailData.effects.length === 0 ? (
                    <p className="text-sm text-gray-400">暂无结果记录</p>
                  ) : (
                    <div className="space-y-2">
                      {detailData.effects.map((effect: any) => (
                        <div key={effect.id} className="bg-white rounded p-2 text-sm">
                          <div className="font-medium">{effect.title}</div>
                          <div className="text-xs text-gray-500">{effect.date}</div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>

              {/* 关联记忆 */}
              {detailData.relatedMemories && detailData.relatedMemories.length > 0 && (
                <div className="mt-4">
                  <h4 className="font-medium text-sm text-gray-700 mb-2">🧠 关联记忆</h4>
                  <div className="space-y-2">
                    {detailData.relatedMemories.map((memory: any) => (
                      <div key={memory.id} className="bg-white rounded p-2 text-sm">
                        <div>{memory.summary}</div>
                        <div className="text-xs text-gray-500 mt-1">
                          情感权重: {memory.emotionalWeight} | 记忆留存: {Math.round(memory.retention * 100)}%
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default CausalityChain
