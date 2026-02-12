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
  private baseURL: string = 'http://localhost:8001' // 使用简化版后端服务

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
}

// 全局API服务实例
export const apiService = new APIService()