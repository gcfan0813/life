import React from 'react'
import { CharacterState } from '@shared/types'
import { Heart, Brain, Users, Lightbulb, HeartHandshake, TrendingUp, MapPin, Clock, Star } from 'lucide-react'

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
      bgColor: 'bg-white/5',

      subDimensions: [
        { key: 'health', name: '健康', value: dimensions.physical?.health || 0 },
        { key: 'energy', name: '精力', value: dimensions.physical?.energy || 0 },
        { key: 'appearance', name: '外貌', value: dimensions.physical?.appearance || 0 },
        { key: 'fitness', name: '体能', value: dimensions.physical?.fitness || 0 }
      ]
    },
    {
      key: 'psychological' as const,
      name: '心理系统',
      icon: Brain,
      color: 'text-purple-500',
      bgColor: 'bg-white/5',

      subDimensions: [
        { key: 'happiness', name: '幸福感', value: dimensions.psychological?.happiness || 0 },
        { key: 'stress', name: '压力', value: dimensions.psychological?.stress || 0 },
        { key: 'resilience', name: '韧性', value: dimensions.psychological?.resilience || 0 }
      ]
    },
    {
      key: 'social' as const,
      name: '社会系统',
      icon: Users,
      color: 'text-blue-500',
      bgColor: 'bg-white/5',

      subDimensions: [
        { key: 'socialCapital', name: '社会资本', value: dimensions.social?.socialCapital || 0 },
        { key: 'career.level', name: '职业等级', value: dimensions.social?.career?.level || 0 },
        { key: 'career.satisfaction', name: '职业满意度', value: dimensions.social?.career?.satisfaction || 0 }
      ]
    },
    {
      key: 'cognitive' as const,
      name: '认知系统',
      icon: Lightbulb,
      color: 'text-yellow-500',
      bgColor: 'bg-white/5',

      subDimensions: [
        { key: 'knowledge.academic', name: '学术知识', value: dimensions.cognitive?.knowledge?.academic || 0 },
        { key: 'skills.communication', name: '沟通能力', value: dimensions.cognitive?.skills?.communication || 0 },
        { key: 'memory.longTerm', name: '长期记忆', value: dimensions.cognitive?.memory?.longTerm || 0 }
      ]
    },
    {
      key: 'relational' as const,
      name: '关系系统',
      icon: HeartHandshake,
      color: 'text-pink-500',
      bgColor: 'bg-white/5',

      subDimensions: [
        { key: 'intimacy.family', name: '家庭亲密度', value: dimensions.relational?.intimacy?.family || 0 },
        { key: 'intimacy.friends', name: '朋友亲密度', value: dimensions.relational?.intimacy?.friends || 0 },
        { key: 'network.quality', name: '网络质量', value: dimensions.relational?.network?.quality || 0 }
      ]
    }
  ]

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Overview Card */}
      <div className="relative overflow-hidden rounded-[40px] bg-slate-900/40 backdrop-blur-3xl border border-white/10 shadow-[0_32px_64px_-16px_rgba(0,0,0,0.5)] p-10 sm:p-12">
        <div className="absolute top-0 right-0 p-12 opacity-[0.03] pointer-events-none">
          <TrendingUp size={240} className="text-white" />
        </div>
        
        <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-12">
          <div className="space-y-6 flex-1">
            <div className="inline-flex items-center space-x-3 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-xs font-black uppercase tracking-[0.3em]">
              <div className="w-2 h-2 rounded-full bg-indigo-400 animate-pulse" />
              <span>Quantum Identity v2.0</span>
            </div>
            
            <div className="space-y-2">
              <h2 className="text-5xl sm:text-7xl font-black text-white tracking-tighter leading-none premium-gradient-text">
                {state.occupation || '探索者'}
              </h2>
              <div className="flex flex-wrap items-center gap-4 text-slate-400 text-lg font-bold">
                <span className="px-4 py-1 rounded-2xl bg-white/5 border border-white/10 text-white shadow-inner">
                  {state.lifeStage === 'childhood' ? '幼年' : 
                   state.lifeStage === 'teen' ? '少年' :
                   state.lifeStage === 'youngAdult' ? '青年' :
                   state.lifeStage === 'adult' ? '成年' :
                   state.lifeStage === 'middleAge' ? '中年' : '晚年'}
                </span>
                <span className="text-indigo-500/30 font-light text-2xl">/</span>
                <span className="flex items-center gap-2">
                  <MapPin size={20} className="text-sky-400" />
                  {state.location || '未知区域'}
                </span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-8 p-8 rounded-[32px] bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-white/10 shadow-2xl relative group overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-700" />
            <div className="relative z-10 text-right">
              <div className="text-xs font-black uppercase tracking-[0.3em] text-indigo-300 mb-2">Well-being Index</div>
              <div className="text-7xl font-black text-white leading-none tracking-tighter">
                {state.dimensions.psychological.happiness}<span className="text-2xl text-indigo-500/50 ml-1">%</span>
              </div>
            </div>
            <div className="relative z-10 text-6xl filter drop-shadow-2xl transform group-hover:scale-110 transition-transform duration-500">
              {getStatusIcon(state.dimensions.psychological.happiness)}
            </div>
          </div>
        </div>

        {/* Quick Stats Chips */}
        <div className="mt-12 flex flex-wrap gap-4">
          {[
            { label: '生存天数', value: state.daysSurvived, icon: Clock, color: 'text-sky-400', bg: 'bg-sky-500/5' },
            { label: '决策总量', value: state.totalDecisions, icon: Brain, color: 'text-indigo-400', bg: 'bg-indigo-500/5' },
            { label: '关键转折', value: state.totalEvents, icon: Star, color: 'text-amber-400', bg: 'bg-amber-500/5' },
          ].map((stat, i) => (
            <div key={i} className={`flex items-center space-x-4 px-6 py-4 rounded-[24px] ${stat.bg} border border-white/5 hover:border-white/10 transition-all hover:scale-105 cursor-default`}>
              <div className={`p-2 rounded-xl bg-white/5 ${stat.color}`}>
                <stat.icon size={20} />
              </div>
              <div className="flex flex-col">
                <span className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em]">{stat.label}</span>
                <span className="text-xl font-black text-white">{stat.value}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Five Dimensions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
        {dimensionCards.map((dimension) => {
          const Icon = dimension.icon
          const avgValue = dimension.subDimensions.reduce((sum, sub) => sum + sub.value, 0) / dimension.subDimensions.length
          
          return (
            <div key={dimension.key} className="group relative overflow-hidden rounded-[36px] bg-slate-900/40 backdrop-blur-2xl border border-white/10 p-8 transition-all duration-500 hover:-translate-y-2 hover:shadow-[0_24px_48px_-12px_rgba(0,0,0,0.5)] hover:bg-slate-800/60">
              <div className="relative z-10 space-y-8">
                <div className="flex items-center justify-between">
                  <div className={`p-4 rounded-2xl bg-white/5 ${dimension.color} border border-white/10 shadow-inner group-hover:scale-110 transition-transform`}>
                    <Icon size={24} />
                  </div>
                  <div className={`text-3xl font-black tracking-tighter ${getStatusColor(avgValue)}`}>
                    {Math.round(avgValue)}
                  </div>
                </div>
                
                <div className="space-y-6">
                  <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.3em]">{dimension.name}</h3>
                  <div className="space-y-5">
                    {dimension.subDimensions.map((subDim) => (
                      <div key={subDim.key} className="space-y-2">
                        <div className="flex items-center justify-between text-[10px] font-black uppercase tracking-widest">
                          <span className="text-slate-500">{subDim.name}</span>
                          <span className={getStatusColor(subDim.value)}>{subDim.value}</span>
                        </div>
                        <div className="h-2 w-full bg-slate-800/50 rounded-full overflow-hidden p-[1px] border border-white/5">
                          <div 
                            className={`h-full rounded-full transition-all duration-1000 group-hover:duration-700 shadow-[0_0_10px_rgba(255,255,255,0.1)] ${getStatusColor(subDim.value).replace('text-', 'bg-')}`}
                            style={{ width: `${subDim.value}%` }}
                          />
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              {/* Decorative background glow */}
              <div className={`absolute -bottom-16 -right-16 w-48 h-48 blur-[80px] opacity-0 group-hover:opacity-20 transition-opacity duration-1000 rounded-full ${dimension.color.replace('text-', 'bg-')}`} />
            </div>
          )
        })}
      </div>
    </div>

  )

}


export default StatusPanel