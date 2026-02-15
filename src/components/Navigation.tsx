import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useLifeStore } from '../stores/lifeStore'
import { Home, Settings, User, Brain, Calendar } from 'lucide-react'

const Navigation: React.FC = () => {
  const location = useLocation()
  const { currentProfile, currentState } = useLifeStore()

  const navItems = [
    {
      path: '/',
      label: currentProfile ? '时光卷轴' : '首页',
      icon: currentProfile ? Calendar : Home,
      show: true
    },
    {
      path: '/settings',
      label: '设置',
      icon: Settings,
      show: true
    },
  ]

  const isActive = (path: string) => {
    if (path === '/' && location.pathname === '/') return true
    if (path !== '/' && location.pathname.startsWith(path)) return true
    return false
  }

  return (
    <nav className="sticky top-0 z-50 backdrop-blur-3xl bg-slate-950/40 border-b border-white/5 shadow-[0_20px_50px_rgba(0,0,0,0.3)]">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16 sm:h-20">

          {/* Left Side: Logo & Profile Summary */}
          <div className="flex items-center space-x-4 sm:space-x-8">
            <Link to="/" className="flex items-center space-x-4 group">
              <div className="relative p-3 rounded-[20px] bg-gradient-to-br from-indigo-500 via-sky-500 to-purple-500 shadow-2xl group-hover:scale-110 group-hover:rotate-3 transition-all duration-500">
                <Brain className="text-white" size={28} />
                <div className="absolute inset-0 rounded-[20px] bg-white/30 blur opacity-0 group-hover:opacity-100 transition-opacity" />
              </div>
              <div className="hidden xs:block leading-none">
                <div className="text-[10px] font-black uppercase tracking-[0.4em] text-indigo-300 mb-1 high-contrast-text">Infinite Life</div>
                <div className="text-2xl font-black text-white tracking-tighter high-contrast-text">无限人生<span className="text-indigo-400/70">.</span>io</div>
              </div>
            </Link>
            
            {currentProfile && currentState && (
              <div className="hidden md:flex items-center space-x-5 py-2 px-5 rounded-[20px] bg-white/[0.03] border border-white/5 text-slate-200 shadow-inner group/prof">
                <div className="flex items-center space-x-2 border-r border-white/10 pr-4">
                  <div className="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center border border-indigo-500/30">
                    <User size={16} className="text-indigo-400" />
                  </div>
                  <span className="text-sm font-black tracking-tight truncate max-w-[120px] group-hover/prof:text-white transition-colors">{currentProfile.name}</span>
                </div>
                <div className="flex items-center space-x-3 text-[10px] font-black uppercase tracking-widest">
                  <span className="px-3 py-1 rounded-lg bg-indigo-500/20 text-indigo-300 border border-indigo-500/20">{currentState.age} 岁</span>
                  <div className="flex items-center space-x-2 text-slate-500">
                    <Calendar size={14} className="text-sky-400/50" />
                    <span>{currentState.currentDate}</span>
                  </div>
                </div>
              </div>
            )}
          </div>


          {/* Right Side: Menu Items */}
          <div className="flex items-center space-x-4 sm:space-x-6">
            <div className="flex items-center p-1.5 rounded-[22px] bg-white/[0.03] border border-white/5">
              {navItems.map((item) => {
                if (!item.show) return null
                
                const Icon = item.icon
                const active = isActive(item.path)
                
                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    className={`flex items-center space-x-3 px-6 py-3 rounded-[18px] text-[10px] font-black uppercase tracking-[0.2em] transition-all duration-500 ${
                      active
                        ? 'bg-white text-slate-950 shadow-2xl scale-105'
                        : 'text-slate-500 hover:text-white hover:bg-white/5'
                    }`}
                  >
                    <Icon size={18} strokeWidth={active ? 3 : 2} />
                    <span className="hidden sm:inline">{item.label}</span>
                  </Link>
                )
              })}
            </div>
            
            {/* AI Status Indicator */}
            <div className="flex items-center ml-2">
              <div className={`relative flex h-4 w-4 ${currentProfile ? 'animate-pulse' : ''}`}>
                <div className={`absolute inline-flex h-full w-full rounded-full opacity-40 ${currentProfile ? 'bg-emerald-400 animate-ping' : 'bg-slate-700'}`}></div>
                <div className={`relative inline-flex rounded-full h-4 w-4 ${currentProfile ? 'bg-emerald-500' : 'bg-slate-800'} border-2 border-slate-950 shadow-lg shadow-emerald-500/20`}></div>
              </div>
            </div>
          </div>
        </div>


        {/* Mobile Mini Profile Header */}
        {currentProfile && currentState && (
          <div className="md:hidden py-2 border-t border-white/5 overflow-x-auto whitespace-nowrap scrollbar-hide">
            <div className="flex items-center space-x-4 text-xs font-medium text-slate-300 px-3">
              <div className="flex items-center space-x-1.5">
                <User size={12} className="text-indigo-400 flex-shrink-0" />
                <span className="truncate max-w-[80px]">{currentProfile.name}</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <div className="w-1 h-1 rounded-full bg-slate-600" />
                <span>{currentState.age}岁</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <Calendar size={12} className="text-sky-400 flex-shrink-0" />
                <span className="truncate max-w-[100px]">{currentState.currentDate}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navigation