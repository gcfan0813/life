import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { LifeProfile, CharacterState, GameEvent, Memory } from '../../shared/types'
import { apiService, localService } from '../services'

interface LifeStore {
  // 当前状态
  currentProfile: LifeProfile | null
  currentState: CharacterState | null
  events: GameEvent[]
  memories: Memory[]
  
  // 系统状态
  isInitialized: boolean
  isLoading: boolean
  currentDate: string
  
  // 操作方法
  initialize: () => Promise<void>
  createProfile: (profile: Omit<LifeProfile, 'id' | 'createdAt'>) => Promise<void>
  advanceTime: (days?: number) => Promise<void>
  makeDecision: (eventId: string, choiceIndex: number) => Promise<void>
  saveGame: () => Promise<void>
  loadGame: (profileId: string) => Promise<void>
  
  // AI设置
  aiSettings: {
    useLocalModel: boolean
    localModelSize: '1.5B' | '3B' | '7B'
    useFreeAPI: boolean
    customAPI: string | null
  }
  updateAISettings: (settings: Partial<LifeStore['aiSettings']>) => void
}

export const useLifeStore = create<LifeStore>()(
  persist(
    (set, get) => ({
      // 初始状态
      currentProfile: null,
      currentState: null,
      events: [],
      memories: [],
      isInitialized: false,
      isLoading: false,
      currentDate: "1993-06-14",  // 初始化为数据库中的起始日期
      
      // AI设置
      aiSettings: {
        useLocalModel: true,
        localModelSize: '1.5B',
        useFreeAPI: true,
        customAPI: null,
      },
      
      // 初始化系统
      initialize: async () => {
        set({ isLoading: true })
        
        try {
          console.log('开始初始化无限人生系统...')
          
          // 尝试API健康检查
          const healthCheck = await apiService.healthCheck()
          console.log('API健康检查:', healthCheck.success ? '成功' : '失败')
          
          if (healthCheck.success) {
            console.log('使用API服务初始化')
            // 使用API服务
            const dataCheck = await apiService.checkExistingData()
            
            if (dataCheck.success && dataCheck.data?.hasData) {
              const profilesResult = await apiService.getProfiles()
              if (profilesResult.success && profilesResult.data && profilesResult.data.length > 0) {
                console.log('加载现有档案:', profilesResult.data[0].id)
                await get().loadGame(profilesResult.data[0].id)
              } else {
                console.log('没有找到现有档案')
              }
            } else {
              console.log('API服务无数据，尝试本地服务')
              throw new Error('API无数据')
            }
          } else {
            console.log('API健康检查失败，回退到本地服务')
            throw new Error('API不可用')
          }
          
          set({ isInitialized: true, isLoading: false })
          console.log('系统初始化完成')
        } catch (error) {
          console.warn('API初始化失败，回退到本地服务:', error)
          
          try {
            // 回退到本地服务
            const hasData = await localService.checkExistingData()
            console.log('本地服务数据检查:', hasData.hasData ? '有数据' : '无数据')
            
            if (hasData.hasData) {
              const profiles = await localService.getProfiles()
              if (profiles.length > 0) {
                console.log('加载本地档案:', profiles[0].id)
                await get().loadGame(profiles[0].id)
              }
            }
          } catch (localError) {
            console.warn('本地服务也失败:', localError)
          }
          
          // 无论成功失败都标记为已初始化，允许用户继续操作
          set({ isInitialized: true, isLoading: false })
          console.log('系统初始化完成（使用本地模式）')
        }
      },
      
      // 创建角色档案
      createProfile: async (profileData) => {
        set({ isLoading: true })
        
        try {
          // 尝试使用API服务
          const result = await apiService.createProfile(profileData)
          
          if (result.success && result.data) {
            const profile = result.data
            
            // 初始化角色状态
            const initialState: CharacterState = {
              id: `state_${profile.id}`,
              profileId: profile.id,
              currentDate: profile.birthDate,
              age: 0,
              dimensions: {
                physical: { health: 80, energy: 70, appearance: 60 },
                psychological: { 
                  openness: profile.initialPersonality.openness,
                  conscientiousness: profile.initialPersonality.conscientiousness,
                  extraversion: profile.initialPersonality.extraversion,
                  agreeableness: profile.initialPersonality.agreeableness,
                  neuroticism: profile.initialPersonality.neuroticism
                },
                social: { socialCapital: 50, career: { level: 0, title: '无' }, economic: 0 },
                cognitive: { knowledge: 40, skills: 30, memory: 70 },
                relational: { intimacy: 0, network: 0 }
              },
              location: profile.birthLocation,
              occupation: '无',
              education: '无',
              lifeStage: 'childhood',
              totalEvents: 0,
              totalDecisions: 0,
              daysSurvived: 0
            }
            
            set({
              currentProfile: profile,
              currentState: initialState,
              events: [],
              memories: [],
              currentDate: profile.birthDate,
              isLoading: false,
            })
          } else {
            // 回退到本地服务
            const profile = await localService.createProfile(profileData)
            const initialState = await localService.loadGame(profile.id)
            
            set({
              currentProfile: profile,
              currentState: initialState.state,
              events: initialState.events,
              memories: initialState.memories,
              currentDate: initialState.state.currentDate,
              isLoading: false,
            })
          }
        } catch (error) {
          console.error('创建档案失败:', error)
          set({ isLoading: false })
        }
      },
      
      // 推进时间
      advanceTime: async (days = 1) => {
        const { currentProfile, currentState, currentDate } = get()
        if (!currentProfile || !currentState) return
        
        set({ isLoading: true })
        
        try {
          // 尝试使用API服务
          const result = await apiService.advanceTime({
            profileId: currentProfile.id,
            days
          })
          
          if (result.success && result.data) {
            // 更新状态
            set({
              currentState: result.data.newState,
              events: [...get().events, ...result.data.newEvents],
              memories: [...get().memories, ...result.data.newMemories],
              currentDate: result.data.newDate,
              isLoading: false,
            })
          } else {
            // 回退到本地服务
            const localResult = await localService.advanceTime(currentProfile.id, days)
            
            set({
              currentState: localResult.newState,
              events: [...get().events, ...localResult.newEvents],
              memories: [...get().memories, ...localResult.newMemories],
              currentDate: localResult.newDate,
              isLoading: false,
            })
          }
          
          // 自动保存
          await get().saveGame()
        } catch (error) {
          console.error('推进时间失败:', error)
          set({ isLoading: false })
        }
      },
      
      // 做出决策
      makeDecision: async (eventId, choiceIndex) => {
        const { currentProfile, currentState, events } = get()
        if (!currentProfile || !currentState) return
        
        set({ isLoading: true })
        
        try {
          // 尝试使用API服务
          const result = await apiService.makeDecision({
            profileId: currentProfile.id,
            eventId,
            choiceIndex
          })
          
          if (result.success && result.data) {
            // 更新事件状态
            const updatedEvents = events.map(event => 
              event.id === eventId 
                ? { ...event, isCompleted: true, selectedChoice: choiceIndex }
                : event
            )
            
            set({
              currentState: result.data.newState,
              events: updatedEvents,
              memories: [...get().memories, ...result.data.newMemories],
              isLoading: false,
            })
          } else {
            // 回退到本地服务
            const localResult = await localService.makeDecision(currentProfile.id, eventId, choiceIndex)
            
            // 更新事件状态
            const updatedEvents = events.map(event => 
              event.id === eventId 
                ? { ...event, isCompleted: true, selectedChoice: choiceIndex }
                : event
            )
            
            set({
              currentState: localResult.newState,
              events: updatedEvents,
              memories: [...get().memories, ...localResult.newMemories],
              isLoading: false,
            })
          }
          
          // 自动保存
          await get().saveGame()
        } catch (error) {
          console.error('决策处理失败:', error)
          set({ isLoading: false })
        }
      },
      
      // 保存游戏
      saveGame: async () => {
        const { currentProfile, currentState, events, memories } = get()
        if (!currentProfile || !currentState) return
        
        try {
          // 尝试使用API服务
          const result = await apiService.saveGame(currentProfile.id)
          
          if (!result.success) {
            // 回退到本地服务
            await localService.saveGame(currentProfile.id)
          }
        } catch (error) {
          console.error('保存游戏失败:', error)
        }
      },
      
      // 加载游戏
      loadGame: async (profileId) => {
        set({ isLoading: true })
        
        try {
          // 尝试使用API服务
          const result = await apiService.loadGame(profileId)
          
          if (result.success && result.data) {
            set({
              currentProfile: result.data.profile,
              currentState: result.data.state,
              events: result.data.events,
              memories: result.data.memories,
              currentDate: result.data.state.currentDate,
              isLoading: false,
            })
          } else {
            // 回退到本地服务
            const gameState = await localService.loadGame(profileId)
            
            set({
              currentProfile: gameState.profile,
              currentState: gameState.state,
              events: gameState.events,
              memories: gameState.memories,
              currentDate: gameState.state.currentDate,
              isLoading: false,
            })
          }
        } catch (error) {
          console.error('加载游戏失败:', error)
          set({ isLoading: false })
        }
      },
      
      // 更新AI设置
      updateAISettings: (newSettings) => {
        set(state => ({
          aiSettings: { ...state.aiSettings, ...newSettings }
        }))
      },
    }),
    {
      name: 'life-settings-storage',
      partialize: (state) => ({ aiSettings: state.aiSettings }),
    }
  )
)