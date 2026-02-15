import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLifeStore } from '../stores/lifeStore';
import { GameEvent, CharacterState } from '../../shared/types';
import { 
  Play, Pause, SkipForward, RotateCcw, Eye, GitBranch, 
  Globe, Clock, Sparkles, Zap, Heart, Brain, Users, Target 
} from 'lucide-react';

const QuantumLifeTimeline: React.FC = () => {
  const { 
    currentState, 
    events, 
    advanceTime, 
    makeDecision, 
    isLoading,
    currentProfile
  } = useLifeStore();
  
  const [currentEventIndex, setCurrentEventIndex] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [autoAdvance, setAutoAdvance] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const [showCausality, setShowCausality] = useState(false);
  const [showMacroEvents, setShowMacroEvents] = useState(false);
  const [quantumState, setQuantumState] = useState<'stable' | 'fluctuating' | 'collapsing'>('stable');
  
  // 量子波动效果
  const [waveOffset, setWaveOffset] = useState(0);
  
  useEffect(() => {
    const interval = setInterval(() => {
      setWaveOffset(prev => (prev + 0.02) % (Math.PI * 2));
    }, 50);
    return () => clearInterval(interval);
  }, []);

  // 获取当前年份
  const date = currentState?.currentDate ? new Date(currentState.currentDate) : null;
  const currentYear = (date && !isNaN(date.getTime())) 
    ? date.getFullYear() 
    : 2000;

  // 获取待处理的事件
  const pendingEvents = events.filter(event => !event.isCompleted);
  const currentEvent = pendingEvents[currentEventIndex];

  // 量子状态管理
  useEffect(() => {
    if (isLoading) {
      setQuantumState('collapsing');
    } else if (pendingEvents.length === 0) {
      setQuantumState('stable');
    } else {
      setQuantumState('fluctuating');
    }
  }, [isLoading, pendingEvents.length]);

  const handleDecision = async (eventId: string, choiceIndex: number) => {
    await makeDecision(eventId, choiceIndex);
    
    if (currentEventIndex < pendingEvents.length - 1) {
      setCurrentEventIndex(prev => prev + 1);
    } else {
      await handleAdvanceTime();
    }
  };

  const handleAdvanceTime = async (days: number = 30) => {
    await advanceTime(days);
    setCurrentEventIndex(0);
    setIsPlaying(false);
    setAutoAdvance(false);
  };

  const handlePlayPause = () => {
    setIsPlaying(!isPlaying);
    setAutoAdvance(!isPlaying);
  };

  const handleSkip = () => {
    if (pendingEvents.length > 0) {
      setCurrentEventIndex(prev => Math.min(prev + 1, pendingEvents.length - 1));
    }
  };

  const handleRewind = () => {
    setCurrentEventIndex(prev => Math.max(prev - 1, 0));
  };

  if (!currentState) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            className="w-16 h-16 border-4 border-indigo-500 border-t-transparent rounded-full mx-auto mb-4"
          />
          <p className="text-slate-400">初始化量子意识矩阵...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-indigo-950/20 to-slate-900">
      {/* 量子背景场 */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_30%_20%,rgba(99,102,241,0.1),transparent_50%)]" />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_70%_80%,rgba(14,165,233,0.08),transparent_50%)]" />
        
        {/* 量子波动线条 */}
        {[...Array(5)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute h-px bg-gradient-to-r from-transparent via-indigo-500/30 to-transparent"
            style={{
              top: `${20 + i * 15}%`,
              left: '-10%',
              right: '-10%',
              transform: `translateX(${Math.sin(waveOffset + i) * 20}px)`,
            }}
            animate={{
              opacity: [0.3, 0.7, 0.3],
            }}
            transition={{
              duration: 3 + i * 0.5,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          />
        ))}
      </div>

      <div className="relative z-10 max-w-7xl mx-auto px-4 py-8">
        {/* 顶部状态栏 */}
        <motion.div 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="mb-8"
        >
          <div className="flex flex-wrap items-center justify-between gap-6 p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10">
            <div className="flex items-center gap-6">
              <div className="flex items-center gap-3">
                <div className={`w-3 h-3 rounded-full ${
                  quantumState === 'stable' ? 'bg-emerald-500' :
                  quantumState === 'fluctuating' ? 'bg-amber-500 animate-pulse' :
                  'bg-rose-500 animate-pulse'
                }`} />
                <span className="text-sm font-medium text-slate-300 capitalize">
                  量子态: {quantumState === 'stable' ? '稳定' : quantumState === 'fluctuating' ? '波动' : '坍缩'}
                </span>
              </div>
              
              <div className="hidden sm:flex items-center gap-4 text-sm">
                <div className="flex items-center gap-2">
                  <Heart className="w-4 h-4 text-rose-400" />
                  <span className="text-slate-300">{currentState.health.toFixed(1)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Brain className="w-4 h-4 text-indigo-400" />
                  <span className="text-slate-300">{currentState.intelligence.toFixed(1)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="w-4 h-4 text-emerald-400" />
                  <span className="text-slate-300">{currentState.social.toFixed(1)}</span>
                </div>
                <div className="flex items-center gap-2">
                  <Target className="w-4 h-4 text-amber-400" />
                  <span className="text-slate-300">{currentState.achievement.toFixed(1)}</span>
                </div>
              </div>
            </div>

            <div className="text-right">
              <div className="text-lg font-bold text-white">{currentState.age} 岁</div>
              <div className="text-sm text-slate-400">{currentState.currentDate}</div>
            </div>
          </div>
        </motion.div>

        {/* 控制面板 */}
        <motion.div 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.1 }}
          className="mb-8 p-6 rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10"
        >
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={handlePlayPause}
                className={`flex items-center gap-2 px-4 py-2 rounded-full text-sm font-semibold transition-all ${
                  isPlaying 
                    ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30' 
                    : 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                }`}
              >
                {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                {isPlaying ? '暂停推演' : '自动推演'}
              </motion.button>
              
              <div className="flex items-center gap-2">
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={handleSkip}
                  disabled={currentEventIndex >= pendingEvents.length - 1 || isLoading}
                  className="p-2 rounded-full bg-sky-500/15 text-sky-300 hover:bg-sky-500/25 transition-all disabled:opacity-50"
                >
                  <SkipForward size={18} />
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.1 }}
                  whileTap={{ scale: 0.9 }}
                  onClick={handleRewind}
                  disabled={currentEventIndex === 0 || isLoading}
                  className="p-2 rounded-full bg-amber-500/20 text-amber-300 hover:bg-amber-500/30 transition-all disabled:opacity-50"
                >
                  <RotateCcw size={18} />
                </motion.button>
              </div>
            </div>
            
            <div className="flex items-center gap-2">
              <TimeControls onAdvance={handleAdvanceTime} isLoading={isLoading} />
              <ControlButton 
                icon={<Eye size={18} />} 
                active={showPreview} 
                onClick={() => setShowPreview(!showPreview)}
                tooltip="未来预览"
              />
              <ControlButton 
                icon={<GitBranch size={18} />} 
                active={showCausality} 
                onClick={() => setShowCausality(!showCausality)}
                tooltip="因果链"
              />
              <ControlButton 
                icon={<Globe size={18} />} 
                active={showMacroEvents} 
                onClick={() => setShowMacroEvents(!showMacroEvents)}
                tooltip="宏观事件"
              />
            </div>
          </div>
        </motion.div>

        {/* 扩展面板 */}
        <AnimatePresence>
          {(showPreview || showCausality || showMacroEvents) && (
            <motion.div 
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="mb-8 space-y-6 overflow-hidden"
            >
              {showPreview && currentProfile && (
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: -20, opacity: 0 }}
                >
                  <FuturePreview profileId={currentProfile.id} />
                </motion.div>
              )}
              
              {showCausality && currentProfile && (
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: -20, opacity: 0 }}
                >
                  <CausalityChain profileId={currentProfile.id} />
                </motion.div>
              )}
              
              {showMacroEvents && currentProfile && (
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  exit={{ y: -20, opacity: 0 }}
                >
                  <MacroEventPanel profileId={currentProfile.id} currentYear={currentYear} />
                </motion.div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* 量子时间轴 */}
        <motion.div 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: 0.2 }}
          className="relative"
        >
          {pendingEvents.length === 0 ? (
            <QuantumEmptyState onAdvance={handleAdvanceTime} isLoading={isLoading} />
          ) : (
            <QuantumTimeline 
              events={pendingEvents}
              currentIndex={currentEventIndex}
              onDecision={handleDecision}
              currentEvent={currentEvent}
            />
          )}
        </motion.div>

        {/* 量子加载状态 */}
        <AnimatePresence>
          {isLoading && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="fixed inset-0 bg-slate-950/90 backdrop-blur-xl flex items-center justify-center z-50"
            >
              <div className="text-center">
                <motion.div
                  animate={{ 
                    scale: [1, 1.2, 1],
                    rotate: [0, 180, 360]
                  }}
                  transition={{ 
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut"
                  }}
                  className="relative w-24 h-24 mx-auto mb-6"
                >
                  <div className="absolute inset-0 border-4 border-indigo-500/30 rounded-full" />
                  <div className="absolute inset-2 border-4 border-transparent border-t-indigo-400 rounded-full" />
                  <Sparkles className="absolute inset-0 m-auto text-indigo-400 animate-pulse" size={32} />
                </motion.div>
                <div className="space-y-2">
                  <p className="text-xl font-bold text-white tracking-wider">QUANTUM SIMULATION</p>
                  <p className="text-slate-400 text-sm">正在计算因果网络...</p>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// 控制按钮组件
const ControlButton: React.FC<{
  icon: React.ReactNode;
  active: boolean;
  onClick: () => void;
  tooltip: string;
}> = ({ icon, active, onClick, tooltip }) => (
  <motion.button
    whileHover={{ scale: 1.1 }}
    whileTap={{ scale: 0.9 }}
    onClick={onClick}
    className={`p-2 rounded-full border transition-all ${
      active 
        ? 'border-indigo-400/50 bg-indigo-500/20 text-indigo-300' 
        : 'border-white/10 bg-white/5 text-slate-400 hover:text-white'
    }`}
    title={tooltip}
  >
    {icon}
  </motion.button>
);

// 时间控制组件
const TimeControls: React.FC<{ 
  onAdvance: (days: number) => void; 
  isLoading: boolean 
}> = ({ onAdvance, isLoading }) => (
  <div className="flex items-center gap-2">
    {[7, 30, 90, 365].map((days) => (
      <motion.button
        key={days}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => onAdvance(days)}
        disabled={isLoading}
        className="px-3 py-1.5 text-xs rounded-full bg-white/5 border border-white/10 text-slate-300 hover:text-white hover:bg-white/10 transition-all disabled:opacity-50"
      >
        +{days}天
      </motion.button>
    ))}
  </div>
);

// 量子空状态组件
const QuantumEmptyState: React.FC<{ 
  onAdvance: (days: number) => void; 
  isLoading: boolean 
}> = ({ onAdvance, isLoading }) => (
  <motion.div
    initial={{ scale: 0.9, opacity: 0 }}
    animate={{ scale: 1, opacity: 1 }}
    className="text-center py-20 rounded-3xl border border-white/10 bg-white/[0.02] backdrop-blur-xl"
  >
    <div className="mb-6 flex justify-center">
      <motion.div
        animate={{ 
          scale: [1, 1.1, 1],
          rotate: [0, 5, -5, 0]
        }}
        transition={{ 
          duration: 3,
          repeat: Infinity,
          ease: "easeInOut"
        }}
      >
        <Clock size={80} className="text-indigo-500/30" strokeWidth={1} />
      </motion.div>
    </div>
    <h3 className="text-2xl font-bold text-white mb-2">量子真空态</h3>
    <p className="text-slate-400 mb-8 max-w-md mx-auto">
      当前因果网络处于稳定状态，点击下方按钮触发新的量子涨落
    </p>
    <div className="flex justify-center gap-3">
      {[30, 90, 365].map((days) => (
        <motion.button
          key={days}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => onAdvance(days)}
          disabled={isLoading}
          className="px-6 py-3 bg-gradient-to-r from-indigo-500/20 to-purple-500/20 border border-indigo-500/30 text-white rounded-full font-medium hover:from-indigo-500/30 hover:to-purple-500/30 transition-all disabled:opacity-50"
        >
          推进 {days} 天
        </motion.button>
      ))}
    </div>
  </motion.div>
);

// 量子时间轴组件
const QuantumTimeline: React.FC<{
  events: GameEvent[];
  currentIndex: number;
  onDecision: (eventId: string, choiceIndex: number) => void;
  currentEvent?: GameEvent;
}> = ({ events, currentIndex, onDecision, currentEvent }) => (
  <div className="relative space-y-16">
    {/* 中心时间线 */}
    <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-indigo-500/50 via-purple-500/30 to-transparent -translate-x-1/2" />
    
    {/* 当前事件 */}
    {currentEvent && (
      <motion.div
        initial={{ y: 20, opacity: 0, scale: 0.9 }}
        animate={{ y: 0, opacity: 1, scale: 1 }}
        className="relative z-10"
      >
        <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-6 h-6 bg-white rounded-full border-4 border-indigo-500 shadow-[0_0_30px_rgba(99,102,241,0.6)]" />
        <div className="w-full max-w-4xl mx-auto">
          <EventCard
            event={currentEvent}
            onDecision={onDecision}
            isCurrent={true}
          />
        </div>
      </motion.div>
    )}
    
    {/* 未来事件 */}
    <div className="space-y-12">
      {events.slice(currentIndex + 1).map((event, index) => (
        <motion.div
          key={event.id}
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ delay: index * 0.1 }}
          className="relative z-10 opacity-60 hover:opacity-100 transition-all duration-500"
        >
          <div className="absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 w-3 h-3 bg-slate-600 rounded-full border-2 border-slate-800" />
          <div className="w-full max-w-3xl mx-auto transform scale-90 origin-center">
            <EventCard
              event={event}
              onDecision={onDecision}
              isCurrent={false}
            />
          </div>
        </motion.div>
      ))}
    </div>
  </div>
);

export default QuantumLifeTimeline;