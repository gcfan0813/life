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
  
  // 缓存状态
  cachedRequests: Map<string, any>
  lastApiCall: number
  
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
  
  // 工具方法
  _withLoading: <T>(fn: () => Promise<T>) => Promise<T>
  _cachedRequest: <T>(key: string, fn: () => Promise<T>) => Promise<T>
  _debouncedSave: () => void
}

// 防抖定时器
let saveTimer: NodeJS.Timeout | null = null

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
      currentDate: "1993-06-14",
      cachedRequests: new Map(),
      lastApiCall: 0,
      
      // AI设置
      aiSettings: {
        useLocalModel: true,
        localModelSize: '1.5B',
        useFreeAPI: true,
        customAPI: null,
      },
      
      // 带加载状态的包装函数
      _withLoading: async <T>(fn: () => Promise<T>): Promise<T> => {
        set({ isLoading: true })
        try {
          const result = await fn()
          set({ isLoading: false })
          return result
        } catch (error) {
          set({ isLoading: false })
          throw error
        }
      },
      
      // 缓存请求
      _cachedRequest: async <T>(key: string, fn: () => Promise<T>): Promise<T> => {
        const cache = get().cachedRequests
        const cached = cache.get(key)
        
        if (cached) {
          return cached
        }
        
        const result = await fn()
        cache.set(key, result)
        set({ cachedRequests: cache })
        
        // 5分钟后清除缓存
        setTimeout(() => {
          const newCache = new Map(cache)
          newCache.delete(key)
          set({ cachedRequests: newCache })
        }, 5 * 60 * 1000)
        
        return result
      },
      
      // 防抖保存
      _debouncedSave: () => {
        if (saveTimer) {
          clearTimeout(saveTimer)
        }
        
        saveTimer = setTimeout(async () => {
          try {
            await get().saveGame()
          } catch (error) {
            console.error('自动保存失败:', error)
          }
        }, 2000) // 2秒防抖
      },
      
      // 初始化系统
      initialize: async () => {
        return get()._withLoading(async () => {
          console.log('开始初始化无限人生系统...')
          
          try {
            // 使用缓存的健康检查
            const healthCheck = await get()._cachedRequest('health-check', () => apiService.healthCheck())
            console.log('API健康检查:', healthCheck.success ? '成功' : '失败')
            
            if (healthCheck.success) {
              console.log('使用API服务初始化')
              const dataCheck = await get()._cachedRequest('data-check', () => apiService.checkExistingData())
              
              if (dataCheck.success && dataCheck.data?.hasData) {
                const profilesResult = await get()._cachedRequest('profiles', () => apiService.getProfiles())
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
          } catch (error) {
            console.warn('API初始化失败，回退到本地服务:', error)
            
            try {
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
          }
          
          set({ isInitialized: true })
          console.log('系统初始化完成')
        })
      },
      
      // 创建角色档案
      createProfile: async (profileData) => {
        return get()._withLoading(async () => {
          try {
            const result = await apiService.createProfile(profileData)
            
            if (result.success && result.data) {
              const profile = result.data
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
              })
            }
            
            // 清除相关缓存
            const cache = get().cachedRequests
            cache.delete('profiles')
            cache.delete('data-check')
            set({ cachedRequests: cache })
            
          } catch (error) {
            console.error('创建档案失败:', error)
            throw error
          }
        })
      },
      
      // 推进时间
      advanceTime: async (days = 1) => {
        const { currentProfile, currentState } = get()
        if (!currentProfile || !currentState) return
        
        return get()._withLoading(async () => {
          try {
            const result = await apiService.advanceTime({
              profileId: currentProfile.id,
              days
            })
            
            if (result.success && result.data) {
              set(state => ({
                currentState: result.data.newState,
                events: [...state.events, ...result.data.newEvents],
                memories: [...state.memories, ...result.data.newMemories],
                currentDate: result.data.newDate,
              }))
            } else {
              // 回退到本地服务
              const localResult = await localService.advanceTime(currentProfile.id, days)
              
              // 修复本地服务无法递增的问题：如果本地服务没返回新日期，前端根据当前日期计算
              let nextDate = localResult.newDate;
              if (!nextDate && get().currentDate) {
                const date = new Date(get().currentDate);
                date.setDate(date.getDate() + days);
                nextDate = date.toISOString().split('T')[0];
              }

              set(state => ({
                currentState: {
                  ...state.currentState,
                  ...localResult.newState,
                  currentDate: nextDate || state.currentDate,
                  age: (state.currentState?.age || 0) + days / 365
                },
                events: [...state.events, ...localResult.newEvents],
                memories: [...state.memories, ...localResult.newMemories],
                currentDate: nextDate || state.currentDate,
              }))
            }
            
            // 防抖保存
            get()._debouncedSave()
            
          } catch (error) {
            console.error('推进时间失败:', error)
            throw error
          }
        })
      },
      
      // 做出决策
      makeDecision: async (eventId, choiceIndex) => {
        const { currentProfile, currentState, events } = get()
        if (!currentProfile || !currentState) return
        
        return get()._withLoading(async () => {
          try {
            const result = await apiService.makeDecision({
              profileId: currentProfile.id,
              eventId,
              choiceIndex
            })
            
            if (result.success && result.data) {
              // 批量更新状态，减少重渲染
              set(state => ({
                currentState: result.data.newState,
                events: state.events.map(event => 
                  event.id === eventId 
                    ? { ...event, isCompleted: true, selectedChoice: choiceIndex }
                    : event
                ),
                memories: [...state.memories, ...result.data.newMemories],
              }))
            } else {
              // 回退到本地服务
              const localResult = await localService.makeDecision(currentProfile.id, eventId, choiceIndex)
              
              set(state => ({
                currentState: localResult.newState,
                events: state.events.map(event => 
                  event.id === eventId 
                    ? { ...event, isCompleted: true, selectedChoice: choiceIndex }
                    : event
                ),
                memories: [...state.memories, ...localResult.newMemories],
              }))
            }
            
            // 防抖保存
            get()._debouncedSave()
            
          } catch (error) {
            console.error('决策处理失败:', error)
            throw error
          }
        })
      },
      
      // 保存游戏
      saveGame: async () => {
        const { currentProfile, currentState, events, memories } = get()
        if (!currentProfile || !currentState) return
        
        try {
          const result = await apiService.saveGame(currentProfile.id)
          
          if (!result.success) {
            await localService.saveGame(currentProfile.id)
          }
        } catch (error) {
          console.error('保存游戏失败:', error)
          // 即使保存失败也继续使用本地存储
          await localService.saveGame(currentProfile.id)
        }
      },
      
      // 加载游戏
      loadGame: async (profileId) => {
        return get()._withLoading(async () => {
          try {
            const result = await apiService.loadGame(profileId)
            
            if (result.success && result.data) {
              set({
                currentProfile: result.data.profile,
                currentState: result.data.state,
                events: result.data.events,
                memories: result.data.memories,
                currentDate: result.data.state.currentDate,
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
              })
            }
            
            // 清除相关缓存
            const cache = get().cachedRequests
            cache.delete(`game-${profileId}`)
            set({ cachedRequests: cache })
            
          } catch (error) {
            console.error('加载游戏失败:', error)
            throw error
          }
        })
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
      partialize: (state) => ({ 
        aiSettings: state.aiSettings,
        currentProfile: state.currentProfile,
        currentDate: state.currentDate
      }),
    }
  )
)