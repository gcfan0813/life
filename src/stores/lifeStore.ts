import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { LifeProfile, CharacterState, GameEvent, Memory } from '../../shared/types'

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
      currentDate: new Date().toISOString().split('T')[0],
      
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
          // 检查本地存储
          const db = await import('@core/storage/database')
          const hasData = await db.checkExistingData()
          
          if (hasData) {
            // 加载最新存档
            const profiles = await db.getProfiles()
            if (profiles.length > 0) {
              await get().loadGame(profiles[0].id)
            }
          }
          
          set({ isInitialized: true, isLoading: false })
        } catch (error) {
          console.error('初始化失败:', error)
          set({ isInitialized: true, isLoading: false })
        }
      },
      
      // 创建角色档案
      createProfile: async (profileData) => {
        set({ isLoading: true })
        
        try {
          const db = await import('@core/storage/database')
          const engine = await import('@core/engine/character')
          
          // 创建新档案
          const profile = await db.createProfile(profileData)
          
          // 初始化角色状态
          const initialState = await engine.initializeCharacterState(profile)
          await db.saveState(profile.id, initialState)
          
          set({
            currentProfile: profile,
            currentState: initialState,
            events: [],
            memories: [],
            currentDate: profile.birthDate,
            isLoading: false,
          })
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
          const engine = await import('@core/engine/simulation')
          const db = await import('@core/storage/database')
          
          // 执行时间推进
          const result = await engine.advanceTime(currentProfile.id, currentState, days)
          
          // 更新状态
          set({
            currentState: result.newState,
            events: [...get().events, ...result.newEvents],
            memories: [...get().memories, ...result.newMemories],
            currentDate: result.newDate,
            isLoading: false,
          })
          
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
          const engine = await import('@core/engine/simulation')
          const db = await import('@core/storage/database')
          
          // 处理决策
          const result = await engine.processDecision(
            currentProfile.id,
            currentState,
            eventId,
            choiceIndex
          )
          
          // 更新事件状态
          const updatedEvents = events.map(event => 
            event.id === eventId 
              ? { ...event, isCompleted: true, selectedChoice: choiceIndex }
              : event
          )
          
          set({
            currentState: result.newState,
            events: updatedEvents,
            memories: [...get().memories, ...result.newMemories],
            isLoading: false,
          })
          
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
          const db = await import('@core/storage/database')
          await db.saveGameState(currentProfile.id, {
            state: currentState,
            events,
            memories,
            lastSaved: new Date().toISOString(),
          })
        } catch (error) {
          console.error('保存游戏失败:', error)
        }
      },
      
      // 加载游戏
      loadGame: async (profileId) => {
        set({ isLoading: true })
        
        try {
          const db = await import('@core/storage/database')
          const gameState = await db.loadGameState(profileId)
          
          set({
            currentProfile: gameState.profile,
            currentState: gameState.state,
            events: gameState.events,
            memories: gameState.memories,
            currentDate: gameState.state.currentDate,
            isLoading: false,
          })
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