import React from 'react'
import { CharacterState } from '@shared/types'
import { Heart, Brain, Users, Lightbulb, HeartHandshake, TrendingUp } from 'lucide-react'

interface StatusPanelProps {
  state: CharacterState
}

const StatusPanel: React.FC<StatusPanelProps> = ({ state }) => {
  const { dimensions } = state

  const getStatusColor = (value: number) => {
    if (value >= 80) return 'text-green-600'
    if (value >= 60) return 'text-yellow-600'
    if (value >= 40) return 'text-orange-600'
    return 'text-red-600'
  }

  const getStatusIcon = (value: number) => {
    if (value >= 80) return '😊'
    if (value >= 60) return '🙂'
    if (value >= 40) return '😐'
    return '😞'
  }

  const dimensionCards = [
    {
      key: 'physical' as const,
      name: '生理系统',
      icon: Heart,
      color: 'text-red-500',
      bgColor: 'bg-red-50',
      subDimensions: [
        { key: 'health', name: '健康', value: dimensions.physical.health },
        { key: 'energy', name: '精力', value: dimensions.physical.energy },
        { key: 'appearance', name: '外貌', value: dimensions.physical.appearance },
        { key: 'fitness', name: '体能', value: dimensions.physical.fitness }
      ]
    },
    {
      key: 'psychological' as const,
      name: '心理系统',
      icon: Brain,
      color: 'text-purple-500',
      bgColor: 'bg-purple-50',
      subDimensions: [
        { key: 'happiness', name: '幸福感', value: dimensions.psychological.happiness },
        { key: 'stress', name: '压力', value: dimensions.psychological.stress },
        { key: 'resilience', name: '韧性', value: dimensions.psychological.resilience }
      ]
    },
    {
      key: 'social' as const,
      name: '社会系统',
      icon: Users,
      color: 'text-blue-500',
      bgColor: 'bg-blue-50',
      subDimensions: [
        { key: 'socialCapital', name: '社会资本', value: dimensions.social.socialCapital },
        { key: 'career.level', name: '职业等级', value: dimensions.social.career.level },
        { key: 'career.satisfaction', name: '职业满意度', value: dimensions.social.career.satisfaction }
      ]
    },
    {
      key: 'cognitive' as const,
      name: '认知系统',
      icon: Lightbulb,
      color: 'text-yellow-500',
      bgColor: 'bg-yellow-50',
      subDimensions: [
        { key: 'knowledge.academic', name: '学术知识', value: dimensions.cognitive.knowledge.academic },
        { key: 'skills.communication', name: '沟通能力', value: dimensions.cognitive.skills.communication },
        { key: 'memory.longTerm', name: '长期记忆', value: dimensions.cognitive.memory.longTerm }
      ]
    },
    {
      key: 'relational' as const,
      name: '关系系统',
      icon: HeartHandshake,
      color: 'text-pink-500',
      bgColor: 'bg-pink-50',
      subDimensions: [
        { key: 'intimacy.family', name: '家庭亲密度', value: dimensions.relational.intimacy.family },
        { key: 'intimacy.friends', name: '朋友亲密度', value: dimensions.relational.intimacy.friends },
        { key: 'network.quality', name: '网络质量', value: dimensions.relational.network.quality }
      ]
    }
  ]

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
      {/* 头部信息 */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">
            {state.occupation || '待业'} | {state.education || '未受教育'}
          </h2>
          <p className="text-gray-600">
            {state.location || '未知地点'} • {state.lifeStage === 'childhood' ? '童年' : 
              state.lifeStage === 'teen' ? '青少年' :
              state.lifeStage === 'youngAdult' ? '青年' :
              state.lifeStage === 'adult' ? '成年' :
              state.lifeStage === 'middleAge' ? '中年' : '老年'}
          </p>
        </div>
        <div className="text-right">
          <div className="text-3xl font-bold text-indigo-600">
            {state.dimensions.psychological.happiness}
          </div>
          <div className="text-sm text-gray-500">
            {getStatusIcon(state.dimensions.psychological.happiness)} 总体幸福感
          </div>
        </div>
      </div>

      {/* 五维系统状态 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4">
        {dimensionCards.map((dimension) => {
          const Icon = dimension.icon
          const avgValue = dimension.subDimensions.reduce((sum, sub) => sum + sub.value, 0) / dimension.subDimensions.length
          
          return (
            <div key={dimension.key} className={`${dimension.bgColor} rounded-lg p-4`}>
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center space-x-2">
                  <Icon className={dimension.color} size={18} />
                  <span className="font-medium text-gray-900">{dimension.name}</span>
                </div>
                <span className={`text-lg font-bold ${getStatusColor(avgValue)}`}>
                  {Math.round(avgValue)}
                </span>
              </div>
              
              <div className="space-y-2">
                {dimension.subDimensions.map((subDim) => (
                  <div key={subDim.key} className="flex items-center justify-between">
                    <span className="text-xs text-gray-600">{subDim.name}</span>
                    <div className="flex items-center space-x-2">
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${getStatusColor(subDim.value).replace('text-', 'bg-')}`}
                          style={{ width: `${subDim.value}%` }}
                        ></div>
                      </div>
                      <span className={`text-xs font-medium ${getStatusColor(subDim.value)}`}>
                        {subDim.value}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>

      {/* 统计信息 */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <div className="flex items-center space-x-6 text-sm text-gray-600">
          <div className="flex items-center space-x-2">
            <TrendingUp size={16} />
            <span>已处理事件: {state.totalEvents}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>决策次数: {state.totalDecisions}</span>
          </div>
          <div className="flex items-center space-x-2">
            <span>生存天数: {state.daysSurvived}</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatusPanel