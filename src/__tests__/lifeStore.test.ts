/**
 * LifeStore 状态管理测试
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { useLifeStore } from '../stores/lifeStore'

// Mock API服务
vi.mock('../services', () => ({
  apiService: {
    healthCheck: vi.fn().mockResolvedValue({ success: true }),
    checkExistingData: vi.fn().mockResolvedValue({ success: true, data: { hasData: false } }),
    getProfiles: vi.fn().mockResolvedValue({ success: true, data: [] }),
    createProfile: vi.fn().mockResolvedValue({
      success: true,
      data: {
        id: 'test-profile-1',
        name: '测试角色',
        gender: 'male',
        birthDate: '1990-01-01',
        birthLocation: '北京',
        familyBackground: 'middle',
        initialPersonality: { openness: 50, conscientiousness: 50, extraversion: 50, agreeableness: 50, neuroticism: 50 },
        createdAt: '2026-01-01T00:00:00',
        startingAge: 0,
        era: '21世纪',
        difficulty: 'normal',
        updatedAt: '2026-01-01T00:00:00'
      }
    }),
    loadGame: vi.fn().mockResolvedValue({
      success: true,
      data: {
        profile: { id: 'test-profile-1', name: '测试角色' },
        state: { age: 25, dimensions: {}, currentDate: '2015-01-01' },
        events: [],
        memories: []
      }
    }),
    advanceTime: vi.fn().mockResolvedValue({
      success: true,
      data: {
        newState: { age: 26, currentDate: '2015-02-01' },
        newEvents: [],
        newMemories: [],
        newDate: '2015-02-01'
      }
    }),
    makeDecision: vi.fn().mockResolvedValue({
      success: true,
      data: {
        newState: { age: 25 },
        newMemories: []
      }
    }),
    saveGame: vi.fn().mockResolvedValue({ success: true })
  },
  localService: {
    checkExistingData: vi.fn().mockResolvedValue({ hasData: false }),
    getProfiles: vi.fn().mockResolvedValue([]),
    createProfile: vi.fn().mockResolvedValue({
      id: 'test-profile-1',
      name: '测试角色'
    }),
    loadGame: vi.fn().mockResolvedValue({
      profile: { id: 'test-profile-1', name: '测试角色' },
      state: { age: 25, currentDate: '2015-01-01' },
      events: [],
      memories: []
    }),
    advanceTime: vi.fn().mockResolvedValue({
      newState: { age: 26 },
      newEvents: [],
      newMemories: [],
      newDate: '2015-02-01'
    }),
    makeDecision: vi.fn().mockResolvedValue({
      newState: { age: 25 },
      newMemories: []
    }),
    saveGame: vi.fn().mockResolvedValue(undefined)
  }
}))

describe('LifeStore', () => {
  beforeEach(() => {
    // 重置store状态
    useLifeStore.setState({
      currentProfile: null,
      currentState: null,
      events: [],
      memories: [],
      isInitialized: false,
      isLoading: false,
      currentDate: '1993-06-14',
      cachedRequests: new Map(),
      lastApiCall: 0,
      aiSettings: {
        useLocalModel: true,
        localModelSize: '1.5B',
        useFreeAPI: true,
        customAPI: null,
      }
    })
  })

  describe('初始状态', () => {
    it('应该有正确的初始状态', () => {
      const state = useLifeStore.getState()
      
      expect(state.currentProfile).toBeNull()
      expect(state.currentState).toBeNull()
      expect(state.events).toEqual([])
      expect(state.memories).toEqual([])
      expect(state.isLoading).toBe(false)
      expect(state.isInitialized).toBe(false)
    })
  })

  describe('createProfile', () => {
    it('应该成功创建角色档案', async () => {
      const store = useLifeStore.getState()
      
      const profileData = {
        name: '测试角色',
        gender: 'male' as const,
        birthDate: '1990-01-01',
        birthLocation: '北京',
        familyBackground: 'middle',
        initialPersonality: { openness: 50, conscientiousness: 50, extraversion: 50, agreeableness: 50, neuroticism: 50 },
        era: '21世纪',
        difficulty: 'normal',
        updatedAt: '2026-01-01T00:00:00'
      }
      
      await store.createProfile(profileData)
      
      const newState = useLifeStore.getState()
      expect(newState.currentProfile).not.toBeNull()
      expect(newState.currentProfile?.name).toBe('测试角色')
    })
  })

  describe('loadGame', () => {
    it('应该成功加载游戏', async () => {
      const store = useLifeStore.getState()
      
      await store.loadGame('test-profile-1')
      
      const newState = useLifeStore.getState()
      expect(newState.currentProfile).not.toBeNull()
      expect(newState.currentState).not.toBeNull()
    })
  })

  describe('advanceTime', () => {
    it('应该成功推进时间', async () => {
      // 先设置一个profile
      useLifeStore.setState({
        currentProfile: { id: 'test-profile-1', name: '测试角色' } as any,
        currentState: { age: 25, currentDate: '2015-01-01' } as any
      })
      
      const store = useLifeStore.getState()
      await store.advanceTime(30)
      
      const newState = useLifeStore.getState()
      expect(newState.currentState).not.toBeNull()
    })
  })

  describe('updateAISettings', () => {
    it('应该成功更新AI设置', () => {
      const store = useLifeStore.getState()
      
      store.updateAISettings({ useLocalModel: false })
      
      const newState = useLifeStore.getState()
      expect(newState.aiSettings.useLocalModel).toBe(false)
    })
  })
})