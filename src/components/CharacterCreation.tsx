import React, { useState } from 'react'
import { useLifeStore } from '../stores/lifeStore'
import { LifeProfile } from '@shared/types'
import { User, Calendar, MapPin, Star } from 'lucide-react'

const CharacterCreation: React.FC = () => {
  const { createProfile, isLoading } = useLifeStore()
  const [step, setStep] = useState(1)
  
  // 表单数据
  const [formData, setFormData] = useState<Partial<Omit<LifeProfile, 'id' | 'createdAt'>>>({
    name: '',
    gender: 'male' as const,
    birthDate: '2000-01-01',
    birthLocation: '北京',
    initialConditions: {
      familyBackground: 'middle' as const,
      educationLevel: 'secondary' as const,
      healthStatus: 'good' as const,
    },
    personalityTraits: {
      riskTolerance: 50,
      ambition: 50,
      empathy: 50,
    },
  })

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleNestedChange = (parent: string, field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [parent]: {
        ...(prev[parent as keyof typeof prev] as object),
        [field]: value
      }
    }))
  }

  const handleSubmit = async () => {
    if (!formData.name || !formData.birthDate || !formData.birthLocation) {
      alert('请填写完整信息')
      return
    }
    
    await createProfile(formData as Omit<LifeProfile, 'id' | 'createdAt'>)
  }

  const renderStep1 = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-gray-900 flex items-center">
        <User className="mr-2" size={20} />
        基本信息
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            姓名
          </label>
          <input
            type="text"
            value={formData.name || ''}
            onChange={(e) => handleInputChange('name', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="请输入您的姓名"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            性别
          </label>
          <div className="flex space-x-4">
            <label className="flex items-center">
              <input
                type="radio"
                name="gender"
                value="male"
                checked={formData.gender === 'male'}
                onChange={(e) => handleInputChange('gender', e.target.value)}
                className="mr-2"
              />
              男性
            </label>
            <label className="flex items-center">
              <input
                type="radio"
                name="gender"
                value="female"
                checked={formData.gender === 'female'}
                onChange={(e) => handleInputChange('gender', e.target.value)}
                className="mr-2"
              />
              女性
            </label>
          </div>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <Calendar className="inline mr-1" size={14} />
            出生日期
          </label>
          <input
            type="date"
            value={formData.birthDate || ''}
            onChange={(e) => handleInputChange('birthDate', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            <MapPin className="inline mr-1" size={14} />
            出生地点
          </label>
          <input
            type="text"
            value={formData.birthLocation || ''}
            onChange={(e) => handleInputChange('birthLocation', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
            placeholder="例如：北京"
          />
        </div>
      </div>
    </div>
  )

  const renderStep2 = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-gray-900 flex items-center">
        <Star className="mr-2" size={20} />
        初始条件
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            家庭背景
          </label>
          <select
            value={formData.initialConditions?.familyBackground || 'middle'}
            onChange={(e) => handleNestedChange('initialConditions', 'familyBackground', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="poor">普通家庭</option>
            <option value="middle">中产家庭</option>
            <option value="wealthy">富裕家庭</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            教育水平
          </label>
          <select
            value={formData.initialConditions?.educationLevel || 'secondary'}
            onChange={(e) => handleNestedChange('initialConditions', 'educationLevel', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="none">未接受教育</option>
            <option value="primary">小学</option>
            <option value="secondary">中学</option>
            <option value="college">大学</option>
            <option value="graduate">研究生</option>
          </select>
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            健康状况
          </label>
          <select
            value={formData.initialConditions?.healthStatus || 'good'}
            onChange={(e) => handleNestedChange('initialConditions', 'healthStatus', e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="poor">较差</option>
            <option value="average">一般</option>
            <option value="good">良好</option>
            <option value="excellent">优秀</option>
          </select>
        </div>
      </div>
    </div>
  )

  const renderStep3 = () => (
    <div className="space-y-6">
      <h3 className="text-xl font-semibold text-gray-900">
        个性特征
      </h3>
      
      <div className="space-y-4">
        {[
          { key: 'riskTolerance', label: '风险承受度', description: '愿意承担风险的程度' },
          { key: 'ambition', label: '野心', description: '追求成功和成就的动力' },
          { key: 'empathy', label: '同理心', description: '理解他人感受的能力' },
        ].map((trait) => (
          <div key={trait.key} className="bg-gray-50 rounded-lg p-4">
            <div className="flex justify-between items-center mb-2">
              <label className="text-sm font-medium text-gray-700">
                {trait.label}
              </label>
              <span className="text-sm text-gray-500">
                {formData.personalityTraits?.[trait.key as keyof typeof formData.personalityTraits] || 50}
              </span>
            </div>
            <p className="text-xs text-gray-500 mb-3">{trait.description}</p>
            <input
              type="range"
              min="0"
              max="100"
              value={formData.personalityTraits?.[trait.key as keyof typeof formData.personalityTraits] || 50}
              onChange={(e) => handleNestedChange('personalityTraits', trait.key, parseInt(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>保守</span>
              <span>适中</span>
              <span>激进</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  )

  const getProgress = () => {
    if (!formData.name || !formData.birthDate || !formData.birthLocation) return 0
    return step * 33
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          创建您的人生档案
        </h1>
        <p className="text-gray-600 text-lg">
          基于真实世界规律，让AI为您推演无限可能的人生
        </p>
      </div>

      {/* 进度条 */}
      <div className="mb-8">
        <div className="flex justify-between text-sm text-gray-600 mb-2">
          <span>基本信息</span>
          <span>初始条件</span>
          <span>个性特征</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div 
            className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
            style={{ width: `${getProgress()}%` }}
          ></div>
        </div>
      </div>

      {/* 表单内容 */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 mb-6">
        {step === 1 && renderStep1()}
        {step === 2 && renderStep2()}
        {step === 3 && renderStep3()}
      </div>

      {/* 导航按钮 */}
      <div className="flex justify-between">
        <button
          onClick={() => setStep(Math.max(1, step - 1))}
          disabled={step === 1}
          className="px-6 py-2 border border-gray-300 rounded-lg text-gray-700 disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-50"
        >
          上一步
        </button>
        
        {step < 3 ? (
          <button
            onClick={() => setStep(step + 1)}
            className="px-6 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
          >
            下一步
          </button>
        ) : (
          <button
            onClick={handleSubmit}
            disabled={isLoading}
            className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
          >
            {isLoading ? '创建中...' : '开始人生推演'}
          </button>
        )}
      </div>
    </div>
  )
}

export default CharacterCreation