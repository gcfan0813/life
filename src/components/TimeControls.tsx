import React, { useState } from 'react'
import { FastForward } from 'lucide-react'

interface TimeControlsProps {
  onAdvance: (days: number) => void
  isLoading: boolean
}

const TimeControls: React.FC<TimeControlsProps> = ({ onAdvance, isLoading }) => {
  const [selectedDays, setSelectedDays] = useState(30)

  const timeOptions = [
    { days: 1, label: '1D', description: '日常推进' },
    { days: 7, label: '1W', description: '周计划' },
    { days: 30, label: '1M', description: '月度规划' },
    { days: 90, label: '3M', description: '季度规划' },
    { days: 365, label: '1Y', description: '年度规划' }
  ]

  return (
    <div className="flex items-center gap-4 bg-white/5 p-1.5 rounded-2xl border border-white/5">
      {/* 步进选择 */}
      <div className="flex items-center gap-1">
        {timeOptions.map((option) => (
          <button
            key={option.days}
            onClick={() => setSelectedDays(option.days)}
            className={`px-4 py-2.5 rounded-xl text-[10px] font-black transition-all duration-300 ${
              selectedDays === option.days
                ? 'bg-white text-slate-950 shadow-xl scale-105'
                : 'text-slate-500 hover:text-slate-300 hover:bg-white/5'
            }`}
            disabled={isLoading}
          >
            {option.label}
          </button>
        ))}
      </div>

      <div className="w-px h-8 bg-white/10 mx-1" />

      {/* 核心推进按钮 */}
      <button
        onClick={() => onAdvance(selectedDays)}
        disabled={isLoading}
        className="group relative px-6 py-2.5 rounded-xl bg-gradient-to-r from-indigo-500 to-sky-500 text-white font-black text-[10px] uppercase tracking-[0.2em] shadow-lg shadow-indigo-500/20 hover:scale-105 active:scale-95 transition-all duration-300 disabled:opacity-50 overflow-hidden"
      >
        <div className="relative z-10 flex items-center gap-2">
          {isLoading ? (
            <div className="w-3 h-3 border-2 border-white/30 border-t-white rounded-full animate-spin" />
          ) : (
            <FastForward size={14} />
          )}
          <span>{isLoading ? 'SYNCING...' : `ADVANCE ${selectedDays}D`}</span>
        </div>
        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:animate-[shimmer_2s_infinite]" />
      </button>
    </div>
  )
}

export default TimeControls
