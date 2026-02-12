import React from 'react'
import { useLifeStore } from '../stores/lifeStore'
import { Save, Download, Upload, Trash2, Brain, Cpu, Wifi, Shield } from 'lucide-react'

const Settings: React.FC = () => {
  const { 
    aiSettings, 
    updateAISettings, 
    currentProfile, 
    saveGame,
    loadGame 
  } = useLifeStore()

  const handleAISettingChange = (setting: keyof typeof aiSettings, value: any) => {
    updateAISettings({ [setting]: value })
  }

  const handleSaveGame = async () => {
    await saveGame()
    alert('游戏已保存')
  }

  const handleExportSave = () => {
    // 导出存档功能（待实现）
    alert('导出存档功能开发中...')
  }

  const handleImportSave = () => {
    // 导入存档功能（待实现）
    alert('导入存档功能开发中...')
  }

  const handleDeleteSave = () => {
    if (confirm('确定要删除当前存档吗？此操作不可恢复。')) {
      // 删除存档功能（待实现）
      alert('删除存档功能开发中...')
    }
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">系统设置</h1>
        <p className="text-gray-600">
          配置AI推演引擎和游戏参数
        </p>
      </div>

      <div className="space-y-8">
        {/* AI引擎设置 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center mb-4">
            <Brain className="text-indigo-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-900">AI引擎设置</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                本地模型使用
              </label>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={aiSettings.useLocalModel}
                  onChange={(e) => handleAISettingChange('useLocalModel', e.target.checked)}
                  className="mr-2"
                />
                <span className="text-sm text-gray-600">
                  启用本地量化模型（离线优先）
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                本地模型响应更快，但推理能力有限
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                本地模型大小
              </label>
              <select
                value={aiSettings.localModelSize}
                onChange={(e) => handleAISettingChange('localModelSize', e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
                disabled={!aiSettings.useLocalModel}
              >
                <option value="1.5B">1.5B（快速，基础推理）</option>
                <option value="3B">3B（平衡，中等推理）</option>
                <option value="7B">7B（强大，高级推理）</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                免费API使用
              </label>
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={aiSettings.useFreeAPI}
                  onChange={(e) => handleAISettingChange('useFreeAPI', e.target.checked)}
                  className="mr-2"
                />
                <span className="text-sm text-gray-600">
                  启用免费公共API（需网络）
                </span>
              </div>
              <p className="text-xs text-gray-500 mt-1">
                免费API提供更强大的推理能力
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                自定义API端点
              </label>
              <input
                type="text"
                value={aiSettings.customAPI || ''}
                onChange={(e) => handleAISettingChange('customAPI', e.target.value)}
                placeholder="https://api.example.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
              <p className="text-xs text-gray-500 mt-1">
                可选，用于连接自定义AI服务
              </p>
            </div>
          </div>
        </div>

        {/* 性能设置 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center mb-4">
            <Cpu className="text-green-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-900">性能设置</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                推演精度
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="fast">快速模式（基础推理）</option>
                <option value="balanced">平衡模式（推荐）</option>
                <option value="detailed">详细模式（深度推理）</option>
              </select>
              <p className="text-xs text-gray-500 mt-1">
                精度越高，推演时间越长
              </p>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                事件生成频率
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="low">低频（每月1-2个事件）</option>
                <option value="medium">中频（每周1-2个事件）</option>
                <option value="high">高频（每天1-2个事件）</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                自动保存间隔
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="5">每5分钟</option>
                <option value="15">每15分钟</option>
                <option value="30">每30分钟</option>
                <option value="manual">手动保存</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                内存使用限制
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="low">低内存（&lt; 100MB）</option>
                <option value="medium">中等内存（&lt; 300MB）</option>
                <option value="high">高内存（无限制）</option>
              </select>
            </div>
          </div>
        </div>

        {/* 数据管理 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center mb-4">
            <Shield className="text-blue-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-900">数据管理</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <button
              onClick={handleSaveGame}
              className="flex items-center justify-center space-x-2 px-4 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <Save size={18} />
              <span>立即保存游戏</span>
            </button>

            <button
              onClick={handleExportSave}
              className="flex items-center justify-center space-x-2 px-4 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <Download size={18} />
              <span>导出存档</span>
            </button>

            <button
              onClick={handleImportSave}
              className="flex items-center justify-center space-x-2 px-4 py-3 bg-yellow-600 text-white rounded-lg hover:bg-yellow-700 transition-colors"
            >
              <Upload size={18} />
              <span>导入存档</span>
            </button>

            <button
              onClick={handleDeleteSave}
              className="flex items-center justify-center space-x-2 px-4 py-3 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              disabled={!currentProfile}
            >
              <Trash2 size={18} />
              <span>删除存档</span>
            </button>
          </div>

          {/* 当前存档信息 */}
          {currentProfile && (
            <div className="mt-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="font-medium text-gray-700 mb-2">当前存档信息</h3>
              <div className="text-sm text-gray-600 space-y-1">
                <div>角色: {currentProfile.name}</div>
                <div>创建时间: {new Date(currentProfile.createdAt).toLocaleDateString()}</div>
                <div>总游戏时间: {Math.floor(currentProfile.totalPlayTime / 60)}小时{currentProfile.totalPlayTime % 60}分钟</div>
              </div>
            </div>
          )}
        </div>

        {/* 网络设置 */}
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <div className="flex items-center mb-4">
            <Wifi className="text-purple-600 mr-3" size={24} />
            <h2 className="text-xl font-semibold text-gray-900">网络设置</h2>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                API路由策略
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="auto">自动选择（推荐）</option>
                <option value="silicon">硅基流动优先</option>
                <option value="zhipu">智谱AI优先</option>
                <option value="baidu">百度文心优先</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                请求超时时间
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="10">10秒</option>
                <option value="30">30秒</option>
                <option value="60">60秒</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                重试次数
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="1">1次</option>
                <option value="2">2次</option>
                <option value="3">3次</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                并发限制
              </label>
              <select className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500">
                <option value="1">单线程</option>
                <option value="3">3线程</option>
                <option value="5">5线程</option>
              </select>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings