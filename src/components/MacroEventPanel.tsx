import React, { useState, useEffect } from 'react'
import { apiService } from '../services/api'
import { AlertTriangle, Globe, TrendingDown, Virus, FileText, Cpu, CloudLightning } from 'lucide-react'

interface MacroEvent {
  id: string
  name: string
  type: string
  yearRange: [number, number]
  description: string
  probability: number
}

interface TriggeredEvent {
  affected: boolean
  event_name: string
  impacts: Record<string, any>
  narrative: string
}

const MacroEventPanel: React.FC<{ profileId: string; currentYear: number }> = ({ 
  profileId, 
  currentYear 
}) => {
  const [activeEvents, setActiveEvents] = useState<MacroEvent[]>([])
  const [triggeredEvents, setTriggeredEvents] = useState<TriggeredEvent[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [showPanel, setShowPanel] = useState(false)

  useEffect(() => {
    loadMacroEvents()
    checkTriggeredEvents()
  }, [currentYear])

  const loadMacroEvents = async () => {
    try {
      const response = await apiService.getMacroEvents(currentYear)
      if (response.success && response.data) {
        setActiveEvents(response.data.events)
      }
    } catch (error) {
      console.error('加载宏观事件失败:', error)
    }
  }

  const checkTriggeredEvents = async () => {
    setIsLoading(true)
    try {
      const response = await apiService.checkMacroEvents(profileId, currentYear)
      if (response.success && response.data) {
        setTriggeredEvents(response.data.triggeredEvents)
      }
    } catch (error) {
      console.error('检查宏观事件失败:', error)
    }
    setIsLoading(false)
  }

  const getEventIcon = (type: string) => {
    switch (type) {
      case 'economic': return <TrendingDown className="w-5 h-5 text-red-500" />
      case 'pandemic': return <Virus className="w-5 h-5 text-orange-500" />
      case 'policy': return <FileText className="w-5 h-5 text-blue-500" />
      case 'technology': return <Cpu className="w-5 h-5 text-purple-500" />
      case 'natural_disaster': return <CloudLightning className="w-5 h-5 text-yellow-500" />
      default: return <Globe className="w-5 h-5 text-gray-500" />
    }
  }

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      'economic': '经济',
      'pandemic': '疫情',
      'policy': '政策',
      'technology': '科技',
      'natural_disaster': '灾害',
      'social': '社会'
    }
    return labels[type] || type
  }

  if (triggeredEvents.length === 0 && !showPanel) {
    return (
      <div className="mb-4">
        <button
          onClick={() => setShowPanel(true)}
          className="flex items-center space-x-2 px-3 py-2 bg-gray-100 rounded-lg text-sm text-gray-600 hover:bg-gray-200 transition-colors"
        >
          <Globe size={16} />
          <span>查看宏观事件</span>
        </button>
      </div>
    )
  }

  return (
    <div className="bg-gradient-to-r from-slate-800 to-slate-700 rounded-lg shadow-lg p-4 mb-6 text-white">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <Globe className="w-5 h-5" />
          <h3 className="font-semibold">宏观事件</h3>
          <span className="text-sm text-slate-300">{currentYear}年</span>
        </div>
        <button
          onClick={() => setShowPanel(!showPanel)}
          className="text-sm text-slate-300 hover:text-white"
        >
          {showPanel ? '收起' : '展开'}
        </button>
      </div>

      {/* 已触发的宏观事件 */}
      {triggeredEvents.length > 0 && (
        <div className="space-y-3 mb-4">
          {triggeredEvents.map((event, index) => (
            <div key={index} className="bg-slate-600/50 rounded-lg p-3">
              <div className="flex items-start space-x-2">
                <AlertTriangle className="w-4 h-4 text-yellow-400 mt-0.5 flex-shrink-0" />
                <div>
                  <h4 className="font-medium text-yellow-400">{event.event_name}</h4>
                  <p className="text-sm text-slate-300 mt-1">{event.narrative}</p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 可能发生的宏观事件 */}
      {showPanel && activeEvents.length > 0 && (
        <div className="border-t border-slate-600 pt-4">
          <h4 className="text-sm font-medium text-slate-300 mb-3">可能发生的宏观事件</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {activeEvents.map(event => (
              <div key={event.id} className="bg-slate-600/30 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-2">
                  {getEventIcon(event.type)}
                  <span className="font-medium">{event.name}</span>
                  <span className="text-xs px-2 py-0.5 bg-slate-500 rounded">
                    {getTypeLabel(event.type)}
                  </span>
                </div>
                <p className="text-sm text-slate-300">{event.description}</p>
                <div className="mt-2 flex items-center justify-between text-xs text-slate-400">
                  <span>{event.yearRange[0]}-{event.yearRange[1]}</span>
                  <span>概率: {(event.probability * 100).toFixed(0)}%</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {isLoading && (
        <div className="text-center py-4">
          <div className="animate-spin rounded-full h-6 w-6 border-2 border-white border-t-transparent mx-auto"></div>
        </div>
      )}
    </div>
  )
}

export default MacroEventPanel
