import { LifeProfile, CharacterState, GameEvent, Memory } from '../shared/types'

// API请求和响应类型定义
export interface APIResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

export interface CreateProfileRequest {
  name: string
  gender: 'male' | 'female'
  birthDate: string
  birthLocation: string
  familyBackground: string
  initialPersonality: {
    openness: number
    conscientiousness: number
    extraversion: number
    agreeableness: number
    neuroticism: number
  }
  startingAge?: number
}

export interface AdvanceTimeRequest {
  profileId: string
  days: number
}

export interface MakeDecisionRequest {
  profileId: string
  eventId: string
  choiceIndex: number
}

// API服务类
export class APIService {
  private baseURL: string = 'http://localhost:8000/api' // 使用完整版后端服务（端口8000）

  // 通用请求方法
  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<APIResponse<T>> {
    try {
      const url = `${this.baseURL}${endpoint}`

      const response = await fetch(url, {
        headers: {
          'Content-Type': 'application/json',
          ...options.headers,
        },
        ...options,
      })

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const data = await response.json()
      return data
    } catch (error) {
      console.error('API请求失败:', error)
      return {
        success: false,
        error: error instanceof Error ? error.message : '网络请求失败'
      }
    }
  }

  // 系统初始化
  async initialize(): Promise<APIResponse<{ isInitialized: boolean }>> {
    return this.request('/initialize')
  }

  // 创建角色档案
  async createProfile(profileData: CreateProfileRequest): Promise<APIResponse<LifeProfile>> {
    return this.request('/profiles', {
      method: 'POST',
      body: JSON.stringify(profileData)
    })
  }

  // 推进时间
  async advanceTime(request: AdvanceTimeRequest): Promise<APIResponse<{
    newState: CharacterState
    newEvents: GameEvent[]
    newMemories: Memory[]
    newDate: string
  }>> {
    return this.request(`/profiles/${request.profileId}/advance`, {
      method: 'POST',
      body: JSON.stringify({ days: request.days })
    })
  }

  // 做出决策
  async makeDecision(request: MakeDecisionRequest): Promise<APIResponse<{
    newState: CharacterState
    newMemories: Memory[]
    immediateEffects: any[]
    longTermEffects: any[]
  }>> {
    return this.request(`/profiles/${request.profileId}/decisions`, {
      method: 'POST',
      body: JSON.stringify({
        eventId: request.eventId,
        choiceIndex: request.choiceIndex
      })
    })
  }

  // 保存游戏
  async saveGame(profileId: string): Promise<APIResponse<{ success: boolean }>> {
    return this.request(`/profiles/${profileId}/save`, {
      method: 'POST'
    })
  }

  // 加载游戏
  async loadGame(profileId: string): Promise<APIResponse<{
    profile: LifeProfile
    state: CharacterState
    events: GameEvent[]
    memories: Memory[]
  }>> {
    return this.request(`/profiles/${profileId}/load`)
  }

  // 获取档案列表
  async getProfiles(): Promise<APIResponse<LifeProfile[]>> {
    return this.request('/profiles')
  }

  // 检查现有数据
  async checkExistingData(): Promise<APIResponse<{ hasData: boolean }>> {
    return this.request('/data/exists')
  }

  // 获取AI设置
  async getAISettings(): Promise<APIResponse<{
    useLocalModel: boolean
    localModelSize: '1.5B' | '3B' | '7B'
    useFreeAPI: boolean
    customAPI: string | null
  }>> {
    return this.request('/settings/ai')
  }

  // 更新AI设置
  async updateAISettings(settings: any): Promise<APIResponse<{ success: boolean }>> {
    return this.request('/settings/ai', {
      method: 'PUT',
      body: JSON.stringify(settings)
    })
  }

  // 健康检查
  async healthCheck(): Promise<APIResponse<{ status: string; version: string }>> {
    return this.request('/health')
  }

  // 未来预览
  async previewFuture(profileId: string, days: number = 90): Promise<APIResponse<{
    previewDays: number
    currentAge: number
    currentStage: string
    currentDimensions: Record<string, number>
    predictions: Array<{
      type: string
      title: string
      description: string
      probability: number
      suggestion: string
    }>
    generatedAt: string
  }>> {
    return this.request(`/profiles/${profileId}/preview?days=${days}`)
  }

  // 获取时间线
  async getTimeline(profileId: string, limit: number = 50): Promise<APIResponse<{
    timeline: Array<{
      type: string
      id: string
      date: string
      title?: string
      description?: string
      summary?: string
      isCompleted?: boolean
      emotionalWeight: number
      retention?: number
    }>
    total: number
  }>> {
    return this.request(`/profiles/${profileId}/timeline?limit=${limit}`)
  }

  // 获取单个事件的因果链
  async getEventCausality(profileId: string, eventId: string): Promise<APIResponse<{
    event: {
      id: string
      title: string
      description: string
      date: string
      type: string
      narrative: string
      emotionalWeight: number
    }
    causes: Array<{
      id: string
      title: string
      date: string
      type: string
      strength: number
    }>
    effects: Array<{
      id: string
      title: string
      date: string
      type: string
      strength: number
    }>
    relatedMemories: Array<{
      id: string
      summary: string
      emotionalWeight: number
      retention: number
    }>
    impacts: Record<string, any>
    decision: {
      selected: number
      choice: string
    } | null
    chain: {
      length: number
      complete: boolean
    }
  }>> {
    return this.request(`/profiles/${profileId}/causality/${eventId}`)
  }

  // 获取完整因果链网络
  async getFullCausalityChain(profileId: string): Promise<APIResponse<{
    nodes: Array<{
      id: string
      title: string
      date: string
      type: string
      isCompleted: boolean
      emotionalWeight: number
    }>
    links: Array<{
      source: string
      target: string
      type: string
    }>
    stats: {
      totalEvents: number
      typeDistribution: Record<string, number>
      completedEvents: number
      pendingEvents: number
    }
  }>> {
    return this.request(`/profiles/${profileId}/causality`)
  }

  // 获取规则库统计
  async getRulesStats(): Promise<APIResponse<{
    totalRules: number
    categories: Record<string, number>
    status: string
  }>> {
    return this.request('/rules/stats')
  }

  // 验证事件合理性
  async validateEvent(profileId: string, eventData: {
    id: string
    eventDate: string
    eventType: string
    title: string
    description: string
    narrative?: string
    choices?: string[]
    impacts?: Record<string, any>
    isCompleted?: boolean
    selectedChoice?: number
    plausibility?: number
    emotionalWeight?: number
  }): Promise<APIResponse<{
    plausibility: number
    conflicts: string[]
    warnings: string[]
    suggestions: string[]
    isValid: boolean
    quality: string
  }>> {
    return this.request(`/rules/validate-event?profile_id=${profileId}`, {
      method: 'POST',
      body: JSON.stringify(eventData)
    })
  }

  // 验证决策合理性
  async validateDecision(profileId: string, decisionData: {
    choiceIndex: number
    eventType: string
  }): Promise<APIResponse<{
    plausibility: number
    riskLevel: string
    suggestions: string[]
    isRecommended: boolean
  }>> {
    return this.request(`/rules/validate-decision?profile_id=${profileId}`, {
      method: 'POST',
      body: JSON.stringify(decisionData)
    })
  }

  // ==================== 宏观事件API ====================

  // 获取宏观事件列表
  async getMacroEvents(year: number): Promise<APIResponse<{
    year: number
    events: Array<{
      id: string
      name: string
      type: string
      yearRange: [number, number]
      description: string
      probability: number
    }>
    total: number
  }>> {
    return this.request(`/macro-events?year=${year}`)
  }

  // 获取宏观事件类型
  async getMacroEventTypes(): Promise<APIResponse<{
    types: Array<{ value: string; label: string }>
  }>> {
    return this.request('/macro-events/types')
  }

  // 检查角色宏观事件
  async checkMacroEvents(profileId: string, year: number): Promise<APIResponse<{
    year: number
    triggeredEvents: Array<{
      affected: boolean
      event_name: string
      impacts: Record<string, any>
      narrative: string
    }>
    total: number
  }>> {
    return this.request(`/profiles/${profileId}/check-macro-events?year=${year}`, {
      method: 'POST'
    })
  }

  // 触发宏观事件
  async triggerMacroEvent(profileId: string, eventId: string): Promise<APIResponse<{
    affected: boolean
    event_name: string
    impacts: Record<string, any>
    narrative: string
  }>> {
    return this.request(`/profiles/${profileId}/trigger-macro-event?event_id=${eventId}`, {
      method: 'POST'
    })
  }

  // ==================== 高敏事件API ====================

  // 获取高敏事件类型
  async getSensitiveEventTypes(): Promise<APIResponse<{
    types: Array<{ value: string; label: string }>
    sensitivity_levels: Array<{ value: string; label: string }>
  }>> {
    return this.request('/sensitive-events/types')
  }

  // 检查事件敏感度
  async checkEventSensitivity(eventData: Record<string, any>): Promise<APIResponse<{
    is_sensitive: boolean
    sensitivity_level: string | null
  }>> {
    return this.request('/events/check-sensitivity', {
      method: 'POST',
      body: JSON.stringify(eventData)
    })
  }

  // 获取高敏事件处理选项
  async getSensitiveEventOptions(eventId: string): Promise<APIResponse<{
    is_sensitive: boolean
    sensitivity_level: string
    event_type: string
    title: string
    description: string
    options: Array<{
      id: string
      label: string
      description: string
    }>
    support_resources: string[]
    warning: string
  }>> {
    return this.request(`/sensitive-events/${eventId}/options`)
  }

  // 处理高敏事件
  async processSensitiveEvent(
    eventId: string,
    handlingMode: 'skip' | 'soften' | 'full',
    profileId?: string
  ): Promise<APIResponse<{
    success: boolean
    event_id: string
    handling_mode: string
    narrative: string
    impacts: Record<string, any>
    support_resources: string[]
    sensitivity_level: string
  }>> {
    let url = `/sensitive-events/${eventId}/process?handling_mode=${handlingMode}`
    if (profileId) {
      url += `&profile_id=${profileId}`
    }
    return this.request(url, { method: 'POST' })
  }

  // 获取高敏事件列表
  async listSensitiveEvents(): Promise<APIResponse<{
    events: Array<{
      id: string
      type: string
      level: string
      title: string
      description: string
    }>
    total: number
  }>> {
    return this.request('/sensitive-events/list')
  }

  // ==================== 家族传承API ====================

  // 创建家族
  async createFamily(founderName: string, profileId: string): Promise<APIResponse<{
    family_id: string
    founder_name: string
    total_members: number
  }>> {
    return this.request(`/families?founder_name=${encodeURIComponent(founderName)}&profile_id=${profileId}`, {
      method: 'POST'
    })
  }

  // 获取家族树
  async getFamilyTree(familyId: string): Promise<APIResponse<{
    family_id: string
    founder_name: string
    nodes: Array<{
      id: string
      name: string
      gender: string
      birth_year: number
      death_year: number | null
      generation: number
      profile_id: string | null
    }>
    links: Array<{
      source: string
      target: string
      type: string
    }>
    stats: Record<string, any>
    legacies: Array<{
      type: string
      name: string
      value: any
      inherit_probability: number
    }>
  }>> {
    return this.request(`/families/${familyId}`)
  }

  // 获取家族总结
  async getFamilySummary(familyId: string): Promise<APIResponse<{
    family_id: string
    founder_name: string
    total_generations: number
    total_members: number
    generation_details: Record<number, string[]>
    family_reputation: number
    notable_achievements: string[]
  }>> {
    return this.request(`/families/${familyId}/summary`)
  }

  // 添加子女
  async addChildToFamily(
    familyId: string,
    parentProfileId: string,
    childName: string,
    childGender: string,
    birthYear: number
  ): Promise<APIResponse<{
    id: string
    name: string
    gender: string
    birthDate: string
    family_id: string
    generation: number
    parent_profile_id: string
    inheritance: Record<string, any>
  }>> {
    const url = `/families/${familyId}/children?parent_profile_id=${parentProfileId}&child_name=${encodeURIComponent(childName)}&child_gender=${childGender}&birth_year=${birthYear}`
    return this.request(url, { method: 'POST' })
  }

  // 计算遗产继承
  async calculateInheritance(familyId: string, childId: string): Promise<APIResponse<{
    family_id: string
    child_id: string
    inheritance: Record<string, any>
  }>> {
    return this.request(`/families/${familyId}/inheritance/${childId}`)
  }

  // 获取角色遗产
  async getProfileLegacy(profileId: string): Promise<APIResponse<{
    material: {
      wealth: number
      assets: string[]
    }
    social: {
      reputation: number
      connections: number
    }
    cognitive: {
      knowledge: number
      skills: string[]
    }
    psychological: {
      personality: Record<string, number>
      values: string[]
      wisdom: number
    }
    relational: {
      family_bonds: number
    }
    achievements: Array<{ title: string; date: string }>
  }>> {
    return this.request(`/profiles/${profileId}/legacy`)
  }
}

// 全局API服务实例
export const apiService = new APIService()