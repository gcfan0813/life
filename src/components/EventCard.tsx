import React from 'react'
import { GameEvent, EventChoice } from '@shared/types'
import { Clock, AlertCircle, TrendingUp } from 'lucide-react'

interface EventCardProps {
  event: GameEvent
  onDecision: (eventId: string, choiceIndex: number) => void
  isCurrent: boolean
}

const EventCard: React.FC<EventCardProps> = ({ event, onDecision, isCurrent }) => {
  const getEventTypeColor = (type: string) => {
    switch (type) {
      case 'milestone': return 'bg-purple-100 text-purple-800 border-purple-200'
      case 'crisis': return 'bg-red-100 text-red-800 border-red-200'
      case 'opportunity': return 'bg-green-100 text-green-800 border-green-200'
      case 'relationship': return 'bg-pink-100 text-pink-800 border-pink-200'
      default: return 'bg-blue-100 text-blue-800 border-blue-200'
    }
  }

  const getPlausibilityColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className={`bg-white rounded-lg shadow-sm border-2 ${isCurrent ? 'border-indigo-300 shadow-md' : 'border-gray-100'} transition-all duration-200`}>
      {/* 事件头部 */}
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-start justify-between mb-3">
          <div className="flex items-center space-x-3">
            <span className={`px-3 py-1 rounded-full text-sm font-medium ${getEventTypeColor(event.eventType)}`}>
              {event.eventType === 'milestone' ? '里程碑' : 
               event.eventType === 'crisis' ? '危机' : 
               event.eventType === 'opportunity' ? '机遇' : 
               event.eventType === 'relationship' ? '关系' : '日常'}
            </span>
            
            <div className="flex items-center text-sm text-gray-500">
              <Clock size={14} className="mr-1" />
              {event.eventDate}
            </div>
          </div>
          
          <div className="flex items-center space-x-2">
            {event.plausibility < 60 && (
              <AlertCircle size={16} className="text-yellow-500" />
            )}
            <span className={`text-sm font-medium ${getPlausibilityColor(event.plausibility)}`}>
              可信度: {event.plausibility}%
            </span>
          </div>
        </div>
        
        <h3 className="text-xl font-semibold text-gray-900 mb-2">{event.title}</h3>
        <p className="text-gray-600 leading-relaxed">{event.description}</p>
        
        {/* 情感权重指示器 */}
        {event.emotionalWeight > 0.7 && (
          <div className="flex items-center mt-3 text-sm text-red-600">
            <TrendingUp size={14} className="mr-1" />
            重要情感事件
          </div>
        )}
      </div>

      {/* 详细叙事 */}
      {event.narrative && event.narrative !== event.description && (
        <div className="p-6 border-b border-gray-100 bg-gray-50">
          <p className="text-gray-700 italic leading-relaxed">"{event.narrative}"</p>
        </div>
      )}

      {/* 影响预览 */}
      {event.impacts.length > 0 && (
        <div className="p-4 bg-gray-50 border-b border-gray-100">
          <h4 className="text-sm font-medium text-gray-700 mb-2">预期影响:</h4>
          <div className="flex flex-wrap gap-2">
            {event.impacts.map((impact, index) => (
              <span key={index} className="px-2 py-1 bg-white rounded text-xs text-gray-600 border">
                {impact.dimension}.{impact.subDimension}: {impact.change > 0 ? '+' : ''}{impact.change}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* 选择项 */}
      {!event.isCompleted && (
        <div className="p-6">
          <h4 className="text-sm font-medium text-gray-700 mb-4">请做出选择:</h4>
          <div className="space-y-3">
            {event.choices.map((choice: EventChoice) => (
              <button
                key={choice.id}
                onClick={() => onDecision(event.id, choice.id)}
                className={`w-full text-left p-4 rounded-lg border transition-all duration-200 hover:shadow-md ${
                  choice.riskLevel > 60 
                    ? 'border-red-200 hover:border-red-300 bg-red-50 hover:bg-red-100' 
                    : choice.riskLevel > 30
                    ? 'border-yellow-200 hover:border-yellow-300 bg-yellow-50 hover:bg-yellow-100'
                    : 'border-green-200 hover:border-green-300 bg-green-50 hover:bg-green-100'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-medium text-gray-900">{choice.text}</span>
                  <span className={`text-xs px-2 py-1 rounded-full ${
                    choice.riskLevel > 60 
                      ? 'bg-red-100 text-red-800' 
                      : choice.riskLevel > 30
                      ? 'bg-yellow-100 text-yellow-800'
                      : 'bg-green-100 text-green-800'
                  }`}>
                    风险: {choice.riskLevel}%
                  </span>
                </div>
                
                {/* 即时影响预览 */}
                {choice.immediateImpacts.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-1">
                    {choice.immediateImpacts.map((impact, idx) => (
                      <span key={idx} className="text-xs text-gray-600 bg-white px-1 rounded">
                        {impact.dimension}.{impact.subDimension}: {impact.change > 0 ? '+' : ''}{impact.change}
                      </span>
                    ))}
                  </div>
                )}
                
                {/* 长期效果 */}
                {choice.longTermEffects.length > 0 && (
                  <div className="mt-2">
                    <span className="text-xs text-gray-500">长期效果: {choice.longTermEffects.join(', ')}</span>
                  </div>
                )}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* 已完成事件标记 */}
      {event.isCompleted && event.selectedChoice !== undefined && (
        <div className="p-4 bg-green-50 border-t border-green-200">
          <div className="flex items-center justify-between">
            <span className="text-green-800 font-medium">已选择: {event.choices[event.selectedChoice]?.text}</span>
            <span className="text-green-600 text-sm">✓ 已完成</span>
          </div>
        </div>
      )}
    </div>
  )
}

export default EventCard