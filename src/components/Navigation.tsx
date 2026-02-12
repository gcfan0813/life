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
    <nav className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          {/* 左侧 Logo 和标题 */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Brain className="text-indigo-600" size={28} />
              <span className="text-xl font-bold text-gray-900">
                无限人生
              </span>
            </div>
            
            {/* 当前角色信息 */}
            {currentProfile && currentState && (
              <div className="hidden md:flex items-center space-x-4 text-sm text-gray-600">
                <div className="flex items-center space-x-2">
                  <User size={16} />
                  <span>{currentProfile.name}</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Calendar size={16} />
                  <span>{currentState.age}岁</span>
                  <span className="text-gray-400">|</span>
                  <span>{currentState.currentDate}</span>
                </div>
              </div>
            )}
          </div>

          {/* 右侧导航菜单 */}
          <div className="flex items-center space-x-1">
            {navItems.map((item) => {
              if (!item.show) return null
              
              const Icon = item.icon
              const active = isActive(item.path)
              
              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    active
                      ? 'bg-indigo-100 text-indigo-700'
                      : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'
                  }`}
                >
                  <Icon size={18} />
                  <span className="hidden sm:inline">{item.label}</span>
                </Link>
              )
            })}
            
            {/* AI 状态指示器 */}
            <div className="flex items-center space-x-2 ml-4 pl-4 border-l border-gray-200">
              <div className="flex items-center space-x-2 text-sm text-gray-500">
                <div className={`w-2 h-2 rounded-full ${
                  currentProfile ? 'bg-green-400' : 'bg-gray-400'
                }`}></div>
                <span className="hidden md:inline">
                  {currentProfile ? 'AI推演中' : '待机状态'}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* 移动端角色信息 */}
        {currentProfile && currentState && (
          <div className="md:hidden py-3 border-t border-gray-100">
            <div className="flex items-center justify-between text-sm text-gray-600">
              <div className="flex items-center space-x-3">
                <User size={14} />
                <span>{currentProfile.name}</span>
              </div>
              <div className="flex items-center space-x-3">
                <Calendar size={14} />
                <span>{currentState.age}岁</span>
                <span>{currentState.currentDate}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </nav>
  )
}

export default Navigation