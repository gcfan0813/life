import React, { useState, useEffect } from 'react'
import { useLifeStore } from '../stores/lifeStore'
import { GameEvent, CharacterState } from '../../shared/types'
import EventCard from './EventCard'
import StatusPanel from './StatusPanel'
import TimeControls from './TimeControls'
import FuturePreview from './FuturePreview'
import CausalityChain from './CausalityChain'
import MacroEventPanel from './MacroEventPanel'
import { Play, Pause, SkipForward, RotateCcw, Eye, GitBranch, Globe } from 'lucide-react'

const LifeTimeline: React.FC = () => {
  const { 
    currentState, 
    events, 
    advanceTime, 
    makeDecision, 
    isLoading,
    currentProfile
  } = useLifeStore()
  
  const [currentEventIndex, setCurrentEventIndex] = useState(0)
  const [isPlaying, setIsPlaying] = useState(false)
  const [autoAdvance, setAutoAdvance] = useState(false)
  const [showPreview, setShowPreview] = useState(false)
  const [showCausality, setShowCausality] = useState(false)
  const [showMacroEvents, setShowMacroEvents] = useState(false)
  
  // 响应式状态
  const [isMobile, setIsMobile] = useState(false)
  const [touchStartX, setTouchStartX] = useState(0)
  const [touchEndX, setTouchEndX] = useState(0)

  // 检测移动端
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768)
    }
    
    checkMobile()
    window.addEventListener('resize', checkMobile)
    return () => window.removeEventListener('resize', checkMobile)
  }, [])

  // 触摸滑动处理
  const handleTouchStart = (e: React.TouchEvent) => {
    setTouchStartX(e.targetTouches[0].clientX)
  }

  const handleTouchMove = (e: React.TouchEvent) => {
    setTouchEndX(e.targetTouches[0].clientX)
  }

  const handleTouchEnd = () => {
    if (!touchStartX || !touchEndX) return
    
    const distance = touchStartX - touchEndX
    const isLeftSwipe = distance > 50
    const isRightSwipe = distance < -50

    if (isLeftSwipe && pendingEvents.length > 0) {
      // 左滑：下一个事件
      handleSkip()
    } else if (isRightSwipe && currentEventIndex > 0) {
      // 右滑：上一个事件
      handleRewind()
    }
    
    setTouchStartX(0)
    setTouchEndX(0)
  }

  // 获取当前年份
  const currentYear = currentState?.currentDate 
    ? new Date(currentState.currentDate).getFullYear() 
    : 2000

  // 获取待处理的事件
  const pendingEvents = events.filter(event => !event.isCompleted)
  const currentEvent = pendingEvents[currentEventIndex]

  // 自动播放逻辑
  useEffect(() => {
    if (autoAdvance && !isLoading && pendingEvents.length > 0) {
      const timer = setTimeout(() => {
        if (currentEventIndex < pendingEvents.length - 1) {
          setCurrentEventIndex(prev => prev + 1)
        } else {
          // 处理完所有事件，推进时间
          handleAdvanceTime()
        }
      }, 3000) // 3秒间隔
      
      return () => clearTimeout(timer)
    }
  }, [autoAdvance, currentEventIndex, pendingEvents.length, isLoading])

  const handleDecision = async (eventId: string, choiceIndex: number) => {
    await makeDecision(eventId, choiceIndex)
    
    // 移动到下一个事件或推进时间
    if (currentEventIndex < pendingEvents.length - 1) {
      setCurrentEventIndex(prev => prev + 1)
    } else {
      await handleAdvanceTime()
    }
  }

  const handleAdvanceTime = async (days: number = 30) => {
    await advanceTime(days)
    setCurrentEventIndex(0)
    setIsPlaying(false)
    setAutoAdvance(false)
  }

  const handlePlayPause = () => {
    if (isPlaying) {
      setIsPlaying(false)
      setAutoAdvance(false)
    } else {
      setIsPlaying(true)
      setAutoAdvance(true)
    }
  }

  const handleSkip = () => {
    if (pendingEvents.length > 0) {
      setCurrentEventIndex(prev => Math.min(prev + 1, pendingEvents.length - 1))
    }
  }

  const handleRewind = () => {
    setCurrentEventIndex(prev => Math.max(prev - 1, 0))
  }

  if (!currentState) {
    return (
      <div className="flex items-center justify-center min-h-screen-mobile">
        <div className="text-center px-4">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600 text-sm sm:text-base">加载角色状态中...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto px-2 sm:px-0">
      {/* 状态面板 */}
      <div className="mb-4">
        <StatusPanel state={currentState} />
      </div>
      
      {/* 时间控制栏 - 响应式 */}
      <div className="bg-white rounded-lg shadow-sm p-3 sm:p-4 mb-4 sm:mb-6">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <div className="flex items-center space-x-2 sm:space-x-4">
            <button
              onClick={handlePlayPause}
              className={`p-2 rounded-full ${
                isPlaying 
                  ? 'bg-red-100 text-red-600' 
                  : 'bg-green-100 text-green-600'
              } hover:opacity-80 transition-opacity`}
              disabled={isLoading}
            >
              {isPlaying ? <Pause size={16} className="sm:size-20" /> : <Play size={16} className="sm:size-20" />}
            </button>
            
            <button
              onClick={handleSkip}
              className="p-2 rounded-full bg-blue-100 text-blue-600 hover:opacity-80 transition-opacity disabled:opacity-50"
              disabled={currentEventIndex >= pendingEvents.length - 1 || isLoading}
            >
              <SkipForward size={20} />
            </button>
            
            <button
              onClick={handleRewind}
              className="p-2 rounded-full bg-yellow-100 text-yellow-600 hover:opacity-80 transition-opacity disabled:opacity-50"
              disabled={currentEventIndex === 0 || isLoading}
            >
              <RotateCcw size={20} />
            </button>
            
            <span className="text-sm text-gray-600">
              当前时间: {currentState.currentDate} | 年龄: {currentState.age}岁
            </span>
          </div>
          
          <TimeControls onAdvance={handleAdvanceTime} isLoading={isLoading} />
          
          <button
            onClick={() => setShowPreview(!showPreview)}
            className={`p-2 rounded-full ${
              showPreview 
                ? 'bg-indigo-100 text-indigo-600' 
                : 'bg-gray-100 text-gray-600'
            } hover:opacity-80 transition-opacity`}
            title="未来预览"
          >
            <Eye size={20} />
          </button>
          
          <button
            onClick={() => setShowCausality(!showCausality)}
            className={`p-2 rounded-full ${
              showCausality 
                ? 'bg-indigo-100 text-indigo-600' 
                : 'bg-gray-100 text-gray-600'
            } hover:opacity-80 transition-opacity`}
            title="因果链追溯"
          >
            <GitBranch size={20} />
          </button>
          
          <button
            onClick={() => setShowMacroEvents(!showMacroEvents)}
            className={`p-2 rounded-full ${
              showMacroEvents 
                ? 'bg-slate-200 text-slate-700' 
                : 'bg-gray-100 text-gray-600'
            } hover:opacity-80 transition-opacity`}
            title="宏观事件"
          >
            <Globe size={20} />
          </button>
        </div>
      </div>

      {/* 未来预览面板 */}
      {showPreview && currentProfile && (
        <div className="mb-6">
          <FuturePreview profileId={currentProfile.id} />
        </div>
      )}

      {/* 因果链面板 */}
      {showCausality && currentProfile && (
        <div className="mb-6">
          <CausalityChain profileId={currentProfile.id} />
        </div>
      )}

      {/* 宏观事件面板 */}
      {showMacroEvents && currentProfile && (
        <div className="mb-6">
          <MacroEventPanel profileId={currentProfile.id} currentYear={currentYear} />
        </div>
      )}

      {/* 事件时间轴 */}
      <div className="space-y-6">
        {pendingEvents.length === 0 ? (
          <div className="text-center py-12">
            <div className="text-gray-400 mb-4">
              <svg className="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
            <p className="text-gray-500">当前没有待处理的事件</p>
            <p className="text-sm text-gray-400 mt-2">点击"推进时间"来生成新的事件</p>
          </div>
        ) : (
          <>
            {/* 当前事件高亮显示 */}
            {currentEvent && (
              <div className="relative">
                <div className="absolute -left-2 top-1/2 transform -translate-y-1/2 w-4 h-4 bg-indigo-600 rounded-full border-4 border-white shadow-lg"></div>
                <EventCard
                  event={currentEvent}
                  onDecision={handleDecision}
                  isCurrent={true}
                />
              </div>
            )}
            
            {/* 未来事件预览 */}
            {pendingEvents.slice(currentEventIndex + 1).map((event, index) => (
              <div key={event.id} className="relative opacity-60">
                <div className="absolute -left-2 top-1/2 transform -translate-y-1/2 w-3 h-3 bg-gray-400 rounded-full border-2 border-white"></div>
                <EventCard
                  event={event}
                  onDecision={handleDecision}
                  isCurrent={false}
                />
              </div>
            ))}
          </>
        )}
      </div>

      {/* 加载状态 */}
      {isLoading && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 text-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
            <p className="text-gray-600">AI正在推演未来可能性...</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default LifeTimeline