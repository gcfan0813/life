import { LifeProfile, CharacterState, GameEvent, Memory } from '../shared/types'

// 本地服务实现 - 直接调用Python模块
interface LocalService {
  initialize(): Promise<{ isInitialized: boolean }>
  createProfile(profileData: any): Promise<LifeProfile>
  advanceTime(profileId: string, days: number): Promise<{
    newState: CharacterState
    newEvents: GameEvent[]
    newMemories: Memory[]
    newDate: string
  }>
  makeDecision(profileId: string, eventId: string, choiceIndex: number): Promise<{
    newState: CharacterState
    newMemories: Memory[]
    immediateEffects: any[]
    longTermEffects: any[]
  }>
  saveGame(profileId: string): Promise<{ success: boolean }>
  loadGame(profileId: string): Promise<{
    profile: LifeProfile
    state: CharacterState
    events: GameEvent[]
    memories: Memory[]
  }>
  getProfiles(): Promise<LifeProfile[]>
  checkExistingData(): Promise<{ hasData: boolean }>
}

// 模拟本地服务实现（实际实现需要通过Python桥接）
export const localService: LocalService = {
  async initialize() {
    // 实际实现应该通过Python桥接调用
    console.log('初始化本地服务...')
    return { isInitialized: true }
  },

  async createProfile(profileData) {
    // 模拟创建档案
    return {
      id: `profile_${Date.now()}`,
      name: profileData.name,
      gender: profileData.gender,
      birthDate: profileData.birthDate,
      birthLocation: profileData.birthLocation,
      familyBackground: profileData.familyBackground,
      initialPersonality: profileData.initialPersonality,
      createdAt: new Date().toISOString(),
    }
  },

  async advanceTime(profileId, days) {
    // 模拟时间推进
    return {
      newState: {
        id: 'state_1',
        profileId,
        currentDate: new Date().toISOString().split('T')[0],
        age: 25,
        dimensions: {
          physical: { health: 80, energy: 70, appearance: 60 },
          psychological: { openness: 70, conscientiousness: 65, extraversion: 60, agreeableness: 75, neuroticism: 30 },
          social: { socialCapital: 50, career: { level: 3, title: '初级工程师' }, economic: 40000 },
          cognitive: { knowledge: 60, skills: 55, memory: 70 },
          relational: { intimacy: 40, network: 35 }
        },
        location: '北京',
        occupation: '软件工程师',
        education: '本科',
        lifeStage: 'youngAdult',
        totalEvents: 50,
        totalDecisions: 20,
        daysSurvived: 9125
      },
      newEvents: [],
      newMemories: [],
      newDate: new Date().toISOString().split('T')[0]
    }
  },

  async makeDecision(profileId, eventId, choiceIndex) {
    // 模拟决策处理
    return {
      newState: {
        id: 'state_1',
        profileId,
        currentDate: new Date().toISOString().split('T')[0],
        age: 25,
        dimensions: {
          physical: { health: 80, energy: 70, appearance: 60 },
          psychological: { openness: 70, conscientiousness: 65, extraversion: 60, agreeableness: 75, neuroticism: 30 },
          social: { socialCapital: 50, career: { level: 3, title: '初级工程师' }, economic: 40000 },
          cognitive: { knowledge: 60, skills: 55, memory: 70 },
          relational: { intimacy: 40, network: 35 }
        },
        location: '北京',
        occupation: '软件工程师',
        education: '本科',
        lifeStage: 'youngAdult',
        totalEvents: 50,
        totalDecisions: 21,
        daysSurvived: 9125
      },
      newMemories: [],
      immediateEffects: [],
      longTermEffects: []
    }
  },

  async saveGame(profileId) {
    // 模拟保存游戏
    console.log(`保存游戏: ${profileId}`)
    return { success: true }
  },

  async loadGame(profileId) {
    // 模拟加载游戏
    return {
      profile: {
        id: profileId,
        name: '测试用户',
        gender: 'male',
        birthDate: '2000-01-01',
        birthLocation: '北京',
        familyBackground: '普通家庭',
        initialPersonality: {
          openness: 70,
          conscientiousness: 65,
          extraversion: 60,
          agreeableness: 75,
          neuroticism: 30
        },
        createdAt: new Date().toISOString(),
      },
      state: {
        id: 'state_1',
        profileId,
        currentDate: '2025-01-01',
        age: 25,
        dimensions: {
          physical: { health: 80, energy: 70, appearance: 60 },
          psychological: { openness: 70, conscientiousness: 65, extraversion: 60, agreeableness: 75, neuroticism: 30 },
          social: { socialCapital: 50, career: { level: 3, title: '初级工程师' }, economic: 40000 },
          cognitive: { knowledge: 60, skills: 55, memory: 70 },
          relational: { intimacy: 40, network: 35 }
        },
        location: '北京',
        occupation: '软件工程师',
        education: '本科',
        lifeStage: 'youngAdult',
        totalEvents: 50,
        totalDecisions: 20,
        daysSurvived: 9125
      },
      events: [],
      memories: []
    }
  },

  async getProfiles() {
    // 模拟获取档案列表
    return [
      {
        id: 'profile_1',
        name: '测试用户',
        gender: 'male',
        birthDate: '2000-01-01',
        birthLocation: '北京',
        familyBackground: '普通家庭',
        initialPersonality: {
          openness: 70,
          conscientiousness: 65,
          extraversion: 60,
          agreeableness: 75,
          neuroticism: 30
        },
        createdAt: new Date().toISOString(),
      }
    ]
  },

  async checkExistingData() {
    // 模拟检查数据
    return { hasData: false }
  }
}