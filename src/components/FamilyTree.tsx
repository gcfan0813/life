import React, { useState, useEffect } from 'react'
import { apiService } from '../services/api'
import { Users, User, Heart, Baby, ChevronDown, ChevronUp, Crown } from 'lucide-react'

interface FamilyMember {
  id: string
  name: string
  gender: string
  birth_year: number
  death_year: number | null
  generation: number
  profile_id: string | null
}

interface FamilyLink {
  source: string
  target: string
  type: string
}

interface FamilyTreeProps {
  profileId: string
  onNavigateToProfile?: (profileId: string) => void
}

const FamilyTree: React.FC<FamilyTreeProps> = ({ profileId, onNavigateToProfile }) => {
  const [familyTree, setFamilyTree] = useState<{
    family_id: string
    founder_name: string
    nodes: FamilyMember[]
    links: FamilyLink[]
    stats: Record<string, any>
    legacies: any[]
  } | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [expandedGenerations, setExpandedGenerations] = useState<Set<number>>(new Set([0, 1]))
  const [showLegacy, setShowLegacy] = useState(false)

  useEffect(() => {
    loadFamilyTree()
  }, [profileId])

  const loadFamilyTree = async () => {
    setIsLoading(true)
    try {
      // 首先获取角色的家族ID
      // 这里假设角色有一个family_id属性，实际需要从profile获取
      const legacyResponse = await apiService.getProfileLegacy(profileId)
      
      // 尝试获取家族树（这里需要实际的family_id）
      // 暂时使用profile_id作为family_id的替代
      const response = await apiService.getFamilyTree(`family_${profileId.slice(-8)}`)
      
      if (response.success && response.data) {
        setFamilyTree(response.data as any)
      }
    } catch (error) {
      console.log('家族树尚未创建')
    }
    setIsLoading(false)
  }

  const toggleGeneration = (gen: number) => {
    setExpandedGenerations(prev => {
      const newSet = new Set(prev)
      if (newSet.has(gen)) {
        newSet.delete(gen)
      } else {
        newSet.add(gen)
      }
      return newSet
    })
  }

  const getMembersByGeneration = () => {
    if (!familyTree) return {}
    
    const generations: Record<number, FamilyMember[]> = {}
    familyTree.nodes.forEach(member => {
      if (!generations[member.generation]) {
        generations[member.generation] = []
      }
      generations[member.generation].push(member)
    })
    
    return generations
  }

  const getGenderIcon = (gender: string) => {
    return gender === 'female' ? '👩' : '👨'
  }

  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-gray-200 rounded w-1/4"></div>
          <div className="h-32 bg-gray-100 rounded"></div>
        </div>
      </div>
    )
  }

  if (!familyTree) {
    return (
      <div className="bg-white rounded-lg shadow p-6 text-center">
        <Users className="w-12 h-12 text-gray-400 mx-auto mb-4" />
        <p className="text-gray-500">尚未创建家族</p>
        <p className="text-sm text-gray-400 mt-2">完成一生后将自动创建家族传承</p>
      </div>
    )
  }

  const generations = getMembersByGeneration()
  const genLabels = ['创始人', '第二代', '第三代', '第四代', '第五代+']

  return (
    <div className="bg-white rounded-lg shadow">
      {/* 头部 */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white p-4 rounded-t-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Crown className="w-6 h-6" />
            <div>
              <h3 className="font-semibold">{familyTree.founder_name}家族</h3>
              <p className="text-sm text-indigo-200">
                {familyTree.stats.total_generations}代 · {familyTree.stats.total_members}位成员
              </p>
            </div>
          </div>
          <button
            onClick={() => setShowLegacy(!showLegacy)}
            className="px-3 py-1 bg-white/20 rounded text-sm hover:bg-white/30 transition-colors"
          >
            家族遗产
          </button>
        </div>
      </div>

      {/* 家族遗产面板 */}
      {showLegacy && familyTree.legacies.length > 0 && (
        <div className="border-b p-4 bg-gray-50">
          <h4 className="font-medium text-gray-700 mb-3">可继承的家族遗产</h4>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {familyTree.legacies.map((legacy, index) => (
              <div key={index} className="bg-white p-3 rounded border">
                <p className="text-sm font-medium text-gray-800">{legacy.name}</p>
                <p className="text-xs text-gray-500">
                  继承概率: {(legacy.inherit_probability * 100).toFixed(0)}%
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 家族树 */}
      <div className="p-4 space-y-4">
        {Object.entries(generations).map(([gen, members]) => (
          <div key={gen} className="border rounded-lg overflow-hidden">
            <button
              onClick={() => toggleGeneration(parseInt(gen))}
              className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center space-x-2">
                <span className="font-medium text-gray-700">
                  {genLabels[parseInt(gen)] || `第${parseInt(gen) + 1}代`}
                </span>
                <span className="text-sm text-gray-500">({members.length}人)</span>
              </div>
              {expandedGenerations.has(parseInt(gen)) ? (
                <ChevronUp className="w-4 h-4 text-gray-400" />
              ) : (
                <ChevronDown className="w-4 h-4 text-gray-400" />
              )}
            </button>
            
            {expandedGenerations.has(parseInt(gen)) && (
              <div className="p-3 grid grid-cols-2 md:grid-cols-4 gap-3">
                {members.map(member => (
                  <div
                    key={member.id}
                    className={`p-3 rounded-lg border-2 cursor-pointer transition-colors ${
                      member.profile_id === profileId
                        ? 'border-indigo-500 bg-indigo-50'
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                    onClick={() => member.profile_id && onNavigateToProfile?.(member.profile_id)}
                  >
                    <div className="flex items-center space-x-2">
                      <span className="text-2xl">{getGenderIcon(member.gender)}</span>
                      <div>
                        <p className="font-medium text-gray-800">{member.name}</p>
                        <p className="text-xs text-gray-500">
                          {member.birth_year}年
                          {member.death_year && ` - ${member.death_year}年`}
                        </p>
                      </div>
                    </div>
                    {member.profile_id === profileId && (
                      <span className="inline-block mt-2 text-xs px-2 py-0.5 bg-indigo-100 text-indigo-700 rounded">
                        当前角色
                      </span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* 家族统计 */}
      <div className="border-t p-4 bg-gray-50">
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-2xl font-bold text-indigo-600">{familyTree.stats.total_members}</p>
            <p className="text-sm text-gray-500">家族成员</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-purple-600">{familyTree.stats.total_generations}</p>
            <p className="text-sm text-gray-500">传承代数</p>
          </div>
          <div>
            <p className="text-2xl font-bold text-green-600">{familyTree.stats.family_reputation || 50}</p>
            <p className="text-sm text-gray-500">家族声望</p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default FamilyTree
