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
    // 实际项目中，本地服务应从 IndexedDB 或 localStorage 获取当前状态
    // 这里为了演示递增逻辑，由于 localService 是单例，我们可以简单模拟状态
    console.log(`本地服务：推进角色 ${profileId} 的时间 ${days} 天`);
    
    // 注意：这里的模拟逻辑在页面刷新后会重置
    // 理想情况下，store 应该把当前日期传进来
    return {
      newState: {
        id: 'state_1',
        profileId,
        currentDate: "1993-06-15", // 这是一个占位，实际由 store 更新
        age: 0,
        dimensions: {
          physical: { health: 80, energy: 70, appearance: 60, fitness: 50 },
          psychological: { 
            openness: 70, conscientiousness: 65, extraversion: 60, agreeableness: 75, neuroticism: 30,
            happiness: 80, stress: 20, resilience: 60
          },
          social: { 
            socialCapital: 50, 
            career: { level: 0, title: '无', satisfaction: 0, income: 0 }, 
            economic: { wealth: 0, debt: 0, credit: 70 } 
          },
          cognitive: { 
            knowledge: { academic: 40, practical: 30, creative: 50 }, 
            skills: { communication: 30, problemSolving: 40, leadership: 20 }, 
            memory: { shortTerm: 70, longTerm: 60, emotional: 80 } 
          },
          relational: { 
            intimacy: { family: 80, friends: 40, romantic: 0 }, 
            network: { size: 10, quality: 60, diversity: 30 } 
          }
        },
        location: '北京',
        occupation: '无',
        education: '无',
        lifeStage: 'childhood',
        totalEvents: 1,
        totalDecisions: 0,
        daysSurvived: 0
      } as any,
      newEvents: [],
      newMemories: [],
      newDate: "" // 传空，让 store 根据逻辑自增或后端返回
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