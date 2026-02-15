import React from 'react'
import { GameEvent, EventChoice } from '../../shared/types'
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
    <div className={`relative overflow-hidden rounded-[40px] border transition-all duration-700 group/card ${
      isCurrent 
        ? 'bg-slate-900/60 backdrop-blur-3xl border-indigo-500/30 shadow-[0_32px_64px_-16px_rgba(79,70,229,0.3)] scale-[1.01]' 
        : 'bg-slate-900/20 backdrop-blur-xl border-white/5 shadow-xl opacity-60 hover:opacity-100'
    }`}>
      {/* Dynamic scan line effect */}
      {isCurrent && (
        <div className="absolute inset-0 pointer-events-none overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-transparent via-indigo-500/5 to-transparent -translate-y-full animate-[scan_4s_linear_infinite]" />
        </div>
      )}

      {/* Decorative accent side bar */}
      <div className={`absolute inset-y-0 left-0 w-2 transition-all duration-700 ${
        isCurrent ? 'bg-gradient-to-b from-indigo-500 via-sky-500 to-emerald-500 shadow-[2px_0_10px_rgba(79,70,229,0.5)]' : 'bg-slate-800'
      }`} />
      
      <div className="p-10 sm:p-12 space-y-10">
        {/* Header Section */}
        <div className="space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-6">
            <div className="flex items-center space-x-4">
              <span className={`px-5 py-2 rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] border shadow-lg backdrop-blur-md ${getEventTypeColor(event.eventType)}`}>
                {event.eventType === 'milestone' ? '重大里程碑' : 
                 event.eventType === 'crisis' ? '核心危机' : 
                 event.eventType === 'opportunity' ? '命运契机' : 
                 event.eventType === 'relationship' ? '因缘互联' : '生命实录'}
              </span>
              <div className="flex items-center space-x-2 text-slate-500 text-xs font-black uppercase tracking-widest">
                <Clock size={16} className="text-indigo-500/50" />
                <span>{event.eventDate}</span>
              </div>
            </div>
            
            <div className={`flex items-center space-x-3 px-4 py-2 rounded-2xl bg-white/5 border border-white/5 text-[10px] font-black tracking-[0.1em] ${getPlausibilityColor(event.plausibility)}`}>
              <div className={`w-2 h-2 rounded-full shadow-[0_0_8px_currentColor] animate-pulse ${event.plausibility < 60 ? 'bg-rose-500' : 'bg-emerald-500'}`} />
              <span>COHERENCE: {event.plausibility}%</span>
            </div>
          </div>
          
          <div className="space-y-4">
            <h3 className="text-4xl sm:text-5xl font-black text-white tracking-tighter leading-[1.05] premium-gradient-text">
              {event.title}
            </h3>
            <p className="text-slate-400 text-xl leading-relaxed font-medium max-w-4xl">
              {event.description}
            </p>
          </div>
        </div>

        {/* Narrative & Impacts Visualization */}
        {(event.narrative || event.impacts.length > 0) && (
          <div className="relative group/narrative">
            <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/5 to-purple-500/5 rounded-[32px] blur-xl opacity-0 group-hover/narrative:opacity-100 transition-opacity duration-700" />
            <div className="relative z-10 grid gap-8 p-8 rounded-[32px] bg-white/[0.02] border border-white/5 shadow-inner">
              {event.narrative && event.narrative !== event.description && (
                <div className="relative">
                  <div className="absolute -left-4 top-0 bottom-0 w-1 bg-indigo-500/20 rounded-full" />
                  <p className="text-slate-300 italic leading-relaxed text-lg font-medium pl-4">
                    "{event.narrative}"
                  </p>
                </div>
              )}
              
              {event.impacts.length > 0 && (
                <div className="space-y-4">
                  <div className="text-[10px] font-black uppercase tracking-[0.3em] text-slate-500 flex items-center gap-2">
                    <TrendingUp size={14} />
                    Dimensional Resonance
                  </div>
                  <div className="flex flex-wrap gap-3">
                    {event.impacts.map((impact, index) => (
                      <div key={index} className="px-4 py-2 rounded-2xl bg-slate-900/80 border border-white/10 flex items-center gap-3 group/impact hover:border-indigo-500/30 transition-all">
                        <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{impact.subDimension}</span>
                        <span className={`text-sm font-black ${impact.change > 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                          {impact.change > 0 ? '↑' : '↓'} {Math.abs(impact.change)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Action Section */}
        {!event.isCompleted ? (
          <div className="space-y-8">
            <div className="flex items-center space-x-6">
              <div className="h-px flex-1 bg-gradient-to-r from-transparent to-white/10" />
              <span className="text-[10px] font-black uppercase tracking-[0.4em] text-indigo-400 whitespace-nowrap animate-pulse">Choose Your Destiny</span>
              <div className="h-px flex-1 bg-gradient-to-l from-transparent to-white/10" />
            </div>
            
            <div className="grid gap-5">
              {event.choices.map((choice: EventChoice) => (
                <button
                  key={choice.id}
                  onClick={() => onDecision(event.id, choice.id)}
                  className={`group relative w-full text-left p-8 rounded-[32px] border transition-all duration-500 hover:-translate-y-1.5 hover:shadow-[0_20px_40px_-10px_rgba(0,0,0,0.5)] overflow-hidden ${
                    choice.riskLevel > 60 
                      ? 'bg-rose-500/[0.02] border-rose-500/10 hover:border-rose-500/40' 
                      : choice.riskLevel > 30
                      ? 'bg-amber-500/[0.02] border-amber-500/10 hover:border-amber-500/40'
                      : 'bg-emerald-500/[0.02] border-emerald-500/10 hover:border-emerald-500/40'
                  }`}
                >
                  <div className="absolute inset-0 bg-gradient-to-br from-white/[0.02] to-transparent opacity-0 group-hover:opacity-100 transition-opacity" />
                  
                  <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
                    <div className="space-y-2 flex-1">
                      <div className="flex items-center gap-3">
                        <span className="text-2xl font-black text-white group-hover:text-indigo-300 transition-colors tracking-tight">{choice.text}</span>
                        <div className={`w-1.5 h-1.5 rounded-full ${
                          choice.riskLevel > 60 ? 'bg-rose-500' : choice.riskLevel > 30 ? 'bg-amber-500' : 'bg-emerald-500'
                        } opacity-0 group-hover:opacity-100 transition-opacity shadow-[0_0_8px_currentColor]`} />
                      </div>
                      {choice.longTermEffects.length > 0 && (
                        <p className="text-[10px] font-black text-slate-500 uppercase tracking-[0.2em] group-hover:text-slate-400 transition-colors">
                          {choice.longTermEffects.join(' • ')}
                        </p>
                      )}
                    </div>
                    
                    <div className={`inline-flex items-center px-5 py-2 rounded-2xl text-[10px] font-black uppercase tracking-[0.2em] border transition-all duration-500 ${
                      choice.riskLevel > 60 
                        ? 'bg-rose-500/10 text-rose-400 border-rose-500/20 group-hover:bg-rose-500 group-hover:text-white group-hover:shadow-[0_0_20px_rgba(244,63,94,0.4)]' 
                        : choice.riskLevel > 30
                        ? 'bg-amber-500/10 text-amber-400 border-amber-500/20 group-hover:bg-amber-500 group-hover:text-white group-hover:shadow-[0_0_20px_rgba(245,158,11,0.4)]'
                        : 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20 group-hover:bg-emerald-500 group-hover:text-white group-hover:shadow-[0_0_20px_rgba(16,185,129,0.4)]'
                    }`}>
                      Risk Factor: {choice.riskLevel}%
                    </div>
                  </div>

                  {/* Immediate Impacts Reveal */}
                  {choice.immediateImpacts.length > 0 && (
                    <div className="mt-6 flex flex-wrap gap-3 relative z-10 opacity-40 group-hover:opacity-100 transition-opacity duration-500">
                      {choice.immediateImpacts.map((impact, idx) => (
                        <div key={idx} className="flex items-center gap-1.5 px-3 py-1 rounded-lg bg-black/40 border border-white/5 text-[9px] font-black uppercase tracking-widest text-slate-300">
                          {impact.subDimension} <span className={impact.change > 0 ? 'text-emerald-400' : 'text-rose-400'}>{impact.change > 0 ? '+' : ''}{impact.change}</span>
                        </div>
                      ))}
                    </div>
                  )}
                  
                  {/* Subtle sweep animation */}
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/[0.03] to-transparent -translate-x-full group-hover:animate-[shimmer_2s_infinite]" />
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="relative overflow-hidden p-10 rounded-[40px] bg-emerald-500/5 border border-emerald-500/20 flex items-center justify-between group/result">
            <div className="absolute inset-0 bg-[radial-gradient(circle_at_50%_50%,rgba(16,185,129,0.1),transparent_70%)] opacity-0 group-hover/result:opacity-100 transition-opacity duration-700" />
            <div className="relative z-10 space-y-3">
              <div className="inline-flex items-center gap-2 text-[10px] font-black uppercase tracking-[0.4em] text-emerald-400">
                <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
                Evolution Path Established
              </div>
              <span className="text-3xl font-black text-white tracking-tight">{event.choices[event.selectedChoice]?.text}</span>
            </div>
            <div className="relative z-10 p-5 rounded-3xl bg-emerald-500 text-white shadow-[0_12px_24px_rgba(16,185,129,0.4)] transform rotate-12 group-hover/result:rotate-0 transition-transform duration-500">
              <TrendingUp size={32} />
            </div>
          </div>
        )}
      </div>
    </div>

  )

}


export default EventCard