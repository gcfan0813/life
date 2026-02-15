import React, { useState, useEffect } from 'react'
import { useLifeStore } from '../stores/lifeStore'
import { GameEvent, CharacterState } from '../../shared/types'
import EventCard from './EventCard'
import StatusPanel from './StatusPanel'
import TimeControls from './TimeControls'
import FuturePreview from './FuturePreview'
import CausalityChain from './CausalityChain'
import MacroEventPanel from './MacroEventPanel'
import { Play, Pause, SkipForward, RotateCcw, Eye, GitBranch, Globe, Clock } from 'lucide-react'

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
  const date = currentState?.currentDate ? new Date(currentState.currentDate) : null;
  const currentYear = (date && !isNaN(date.getTime())) 
    ? date.getFullYear() 
    : 2000;

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
    <div className="space-y-8">
      {/* 状态面板 - 优化间距 */}
      <div className="mb-2">
        <StatusPanel state={currentState} />
      </div>
      
      {/* 时间控制栏 - 优化布局和间距 */}
      <div className="card-primary rounded-2xl shadow-xl p-5 sm:p-6">

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 sm:gap-6">
          <div className="flex items-center flex-wrap gap-3">
            <button
              onClick={handlePlayPause}
              className={`flex items-center gap-2 px-3 py-2 rounded-full text-sm font-semibold shadow ${
                isPlaying 
                  ? 'bg-rose-500/20 text-rose-100 border border-rose-200/40' 
                  : 'bg-emerald-500/20 text-emerald-100 border border-emerald-200/40'
              } disabled:opacity-50`}
              disabled={isLoading}
            >

              {isPlaying ? <Pause size={16} /> : <Play size={16} />}
              {isPlaying ? '暂停' : '自动播放'}
            </button>
            
            <div className="flex items-center gap-2">
              <button
                onClick={handleSkip}
                className="p-2 rounded-full bg-sky-500/15 text-sky-100 hover:bg-sky-500/25 transition-opacity disabled:opacity-50"
                disabled={currentEventIndex >= pendingEvents.length - 1 || isLoading}
              >
                <SkipForward size={18} />
              </button>
              <button
                onClick={handleRewind}
                className="p-2 rounded-full bg-amber-500/20 text-amber-100 hover:bg-amber-500/30 transition-opacity disabled:opacity-50"
                disabled={currentEventIndex === 0 || isLoading}
              >
                <RotateCcw size={18} />
              </button>

            </div>
            
            <span className="text-sm text-slate-100 px-3 py-1.5 rounded-full bg-white/10 border border-white/10 font-medium">
              当前时间 {currentState.currentDate} · 年龄 {currentState.age} 岁
            </span>

          </div>
          
          <div className="flex items-center gap-3 flex-wrap">
            <TimeControls onAdvance={handleAdvanceTime} isLoading={isLoading} />
            <button
              onClick={() => setShowPreview(!showPreview)}
              className={`p-2 rounded-full border transition ${
                showPreview 
                  ? 'border-indigo-200/50 bg-indigo-500/20 text-indigo-100' 
                  : 'border-white/10 bg-white/5 text-slate-100'
              }`}
              title="未来预览"
            >

              <Eye size={18} />
            </button>
            <button
              onClick={() => setShowCausality(!showCausality)}
              className={`p-2 rounded-full border transition ${
                showCausality 
                  ? 'border-indigo-200/50 bg-indigo-500/20 text-indigo-100' 
                  : 'border-white/10 bg-white/5 text-slate-100'
              }`}
              title="因果链追溯"
            >

              <GitBranch size={18} />
            </button>
            <button
              onClick={() => setShowMacroEvents(!showMacroEvents)}
              className={`p-2 rounded-full border transition ${
                showMacroEvents 
                  ? 'border-slate-200/50 bg-slate-500/20 text-slate-100' 
                  : 'border-white/10 bg-white/5 text-slate-100'
              }`}
              title="宏观事件"
            >

              <Globe size={18} />
            </button>
          </div>
        </div>
      </div>


      {/* 扩展面板区域 - 统一间距 */}
      <div className="space-y-6">
        {showPreview && currentProfile && (
          <div className="transform transition-all duration-300">
            <FuturePreview profileId={currentProfile.id} />
          </div>
        )}

        {showCausality && currentProfile && (
          <div className="transform transition-all duration-300">
            <CausalityChain profileId={currentProfile.id} />
          </div>
        )}

        {showMacroEvents && currentProfile && (
          <div className="transform transition-all duration-300">
            <MacroEventPanel profileId={currentProfile.id} currentYear={currentYear} />
          </div>
        )}
      </div>

      {/* 事件时间轴 - 优化间距和层次 */}
      <div className="relative space-y-12 sm:space-y-16 pb-24 sm:pb-32 pt-6 sm:pt-8">
        {/* Central timeline line */}
        <div className="absolute left-0 md:left-1/2 top-0 bottom-0 w-px bg-gradient-to-b from-indigo-500/50 via-sky-500/20 to-transparent md:-translate-x-1/2" />

        {pendingEvents.length === 0 ? (
          <div className="relative z-10 text-center py-32 rounded-[40px] card-secondary shadow-2xl">
            <div className="text-indigo-500/20 mb-6 flex justify-center">
              <Clock size={80} strokeWidth={1} className="animate-pulse-slow" />
            </div>
            <h4 className="text-2xl font-black text-white tracking-tight mb-2 high-contrast-text">静待时机</h4>
            <p className="text-slate-400 font-medium">当前因果网络平稳，点击“推进时间”触发新的波澜。</p>
          </div>
        ) : (
          <div className="space-y-24">
            {/* 当前事件高亮显示 - 增强视觉层次 */}
            {currentEvent && (
              <div className="relative z-20 animate-slide-up">
                <div className="absolute left-4 sm:left-0 md:left-1/2 top-1/2 -translate-y-1/2 -translate-x-2 md:-translate-x-1/2 w-3 h-3 sm:w-4 sm:h-4 bg-white rounded-full border-2 sm:border-4 border-indigo-600 shadow-[0_0_15px_rgba(255,255,255,0.8)]"></div>
                <div className="w-full sm:w-[90%] lg:w-[85%] mx-auto">
                  <EventCard
                    event={currentEvent}
                    onDecision={handleDecision}
                    isCurrent={true}
                  />
                </div>
              </div>
            )}
            
            {/* 未来事件预览 */}
            <div className="space-y-12">
              {pendingEvents.slice(currentEventIndex + 1).map((event, index) => (
                <div key={event.id} className="relative z-10 opacity-40 hover:opacity-80 transition-opacity duration-500">
                  <div className="absolute left-4 sm:left-0 md:left-1/2 top-1/2 -translate-y-1/2 -translate-x-1.5 md:-translate-x-1/2 w-2.5 h-2.5 sm:w-3 sm:h-3 bg-slate-700 rounded-full border border-slate-900"></div>
                  <div className="w-full sm:w-[80%] lg:w-[75%] mx-auto scale-95 origin-center">
                    <EventCard
                      event={event}
                      onDecision={handleDecision}
                      isCurrent={false}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 加载状态 - 全屏极简设计 */}
      {isLoading && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-xl flex items-center justify-center z-[100] animate-fade-in">
          <div className="text-center space-y-6">
            <div className="relative inline-flex">
              <div className="w-24 h-24 rounded-full border-2 border-indigo-500/20 border-t-indigo-500 animate-spin" />
              <div className="absolute inset-4 rounded-full bg-indigo-500/10 blur-xl animate-pulse" />
              <Brain size={32} className="absolute inset-0 m-auto text-white animate-pulse" />
            </div>
            <div className="space-y-2">
              <p className="text-xl font-black text-white tracking-widest uppercase">Quantum推演中</p>
              <p className="text-xs text-slate-500 font-bold tracking-[0.3em]">SYNCHRONIZING CAUSALITY NETWORK...</p>
            </div>
          </div>
        </div>
      )}
    </div>
  )

}

export default LifeTimeline