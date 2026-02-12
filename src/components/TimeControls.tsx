import React, { useState } from 'react'
import { Play, Pause, SkipForward, RotateCcw } from 'lucide-react'

interface TimeControlsProps {
  onAdvance: (days: number) => void
  isLoading: boolean
}

const TimeControls: React.FC<TimeControlsProps> = ({ onAdvance, isLoading }) => {
  const [selectedDays, setSelectedDays] = useState(30)
  const [isPlaying, setIsPlaying] = useState(false)

  const timeOptions = [
    { days: 1, label: '1天', description: '日常推进' },
    { days: 7, label: '1周', description: '周计划' },
    { days: 30, label: '1月', description: '月度规划' },
    { days: 90, label: '3月', description: '季度规划' },
    { days: 365, label: '1年', description: '年度规划' }
  ]

  const handlePlayPause = () => {
    if (isPlaying) {
      setIsPlaying(false)
      // 停止自动播放逻辑
    } else {
      setIsPlaying(true)
      // 启动自动播放逻辑
    }
  }

  const handleSkip = () => {
    onAdvance(selectedDays)
  }

  const handleRewind = () => {
    // 回退功能（待实现）
    alert('时间回退功能开发中...')
  }

  return (
    <div className="flex items-center space-x-4">
      {/* 播放控制 */}
      <div className="flex items-center space-x-2">
        <button
          onClick={handlePlayPause}
          className={`p-2 rounded-full ${
            isPlaying 
              ? 'bg-red-100 text-red-600 hover:bg-red-200' 
              : 'bg-green-100 text-green-600 hover:bg-green-200'
          } transition-colors disabled:opacity-50`}
          disabled={isLoading}
        >
          {isPlaying ? <Pause size={16} /> : <Play size={16} />}
        </button>
        
        <button
          onClick={handleSkip}
          className="p-2 rounded-full bg-blue-100 text-blue-600 hover:bg-blue-200 transition-colors disabled:opacity-50"
          disabled={isLoading}
        >
          <SkipForward size={16} />
        </button>
        
        <button
          onClick={handleRewind}
          className="p-2 rounded-full bg-yellow-100 text-yellow-600 hover:bg-yellow-200 transition-colors disabled:opacity-50"
          disabled={isLoading}
        >
          <RotateCcw size={16} />
        </button>
      </div>

      {/* 时间选择器 */}
      <div className="flex items-center space-x-3">
        <span className="text-sm font-medium text-gray-700">推进时间:</span>
        <div className="flex space-x-1">
          {timeOptions.map((option) => (
            <button
              key={option.days}
              onClick={() => setSelectedDays(option.days)}
              className={`px-3 py-1 rounded-lg text-sm font-medium transition-colors ${
                selectedDays === option.days
                  ? 'bg-indigo-600 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
              disabled={isLoading}
            >
              {option.label}
            </button>
          ))}
        </div>
      </div>

      {/* 推进按钮 */}
      <button
        onClick={() => onAdvance(selectedDays)}
        disabled={isLoading}
        className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors font-medium"
      >
        {isLoading ? '推演中...' : `推进 ${selectedDays} 天`}
      </button>

      {/* 播放状态指示器 */}
      {isPlaying && (
        <div className="flex items-center space-x-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-xs text-green-600">自动播放中</span>
        </div>
      )}
    </div>
  )
}

export default TimeControls