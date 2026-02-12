// 基础类型定义
export interface BaseEntity {
  id: string
  createdAt: string
  updatedAt: string
}

// 角色档案
export interface LifeProfile extends BaseEntity {
  name: string
  birthDate: string
  birthPlace: string
  gender: 'male' | 'female' | 'other'
  initialTraits: CharacterTraits
  era: string // 时代背景，如 '1990s', '2000s'
  difficulty: 'easy' | 'normal' | 'hard'
}

// 五维属性系统
export interface FiveDimensions {
  // 生理维度
  physiological: {
    health: number // 0-100
    energy: number // 0-100
    appearance: number // 0-100
    fitness: number // 0-100
  }
  
  // 心理维度
  psychological: {
    openness: number // 大五人格：开放性 0-100
    conscientiousness: number // 尽责性
    extraversion: number // 外向性
    agreeableness: number // 宜人性
    neuroticism: number // 神经质
    emotionalState: number // 当前情绪 -100到100
    resilience: number // 心理韧性 0-100
  }
  
  // 社会维度
  social: {
    socialCapital: number // 社会资本 0-100
    careerLevel: number // 职业等级 0-100
    economicStatus: number // 经济状况 -100到100
    reputation: number // 声誉 0-100
  }
  
  // 认知维度
  cognitive: {
    knowledge: number // 知识水平 0-100
    skills: Record<string, number> // 技能映射
    memoryCapacity: number // 记忆能力 0-100
    learningAbility: number // 学习能力 0-100
  }
  
  // 关系维度
  relational: {
    familyRelations: Record<string, Relationship> // 家庭成员关系
    friendships: Record<string, Relationship> // 朋友关系
    romanticRelations: Record<string, Relationship> // 浪漫关系
    networkSize: number // 社交网络规模
  }
}

// 人际关系
export interface Relationship {
  personId: string
  intimacy: number // 亲密度 0-100
  trust: number // 信任度 0-100
  lastInteraction: string
  relationshipType: 'family' | 'friend' | 'romantic' | 'colleague'
}

// 角色特质
export interface CharacterTraits {
  personalityType: string
  talents: string[]
  challenges: string[]
  values: string[]
  lifeGoals: string[]
}

// 角色状态
export interface CharacterState extends BaseEntity {
  profileId: string
  currentDate: string
  age: number
  dimensions: FiveDimensions
  currentLocation: string
  career: CareerInfo
  education: EducationInfo
  financial: FinancialInfo
  health: HealthInfo
  recentEvents: string[] // 最近事件ID
  memoryWeights: Record<string, number> // 记忆权重
}

// 职业信息
export interface CareerInfo {
  currentJob: string
  company: string
  position: string
  salary: number
  satisfaction: number // 0-100
  stress: number // 0-100
  skills: string[]
  experience: number // 工作经验年数
}

// 教育信息
export interface EducationInfo {
  highestDegree: string
  currentSchool: string
  major: string
  gpa: number
  graduationYear: number | null
}

// 财务信息
export interface FinancialInfo {
  cash: number
  assets: number
  debts: number
  income: number
  expenses: number
  netWorth: number
}

// 健康信息
export interface HealthInfo {
  conditions: HealthCondition[]
  lastCheckup: string
  lifestyle: LifestyleInfo
}

// 健康状况
export interface HealthCondition {
  name: string
  severity: number // 0-100
  diagnosisDate: string
  treatment: string
}

// 生活方式
export interface LifestyleInfo {
  diet: number // 饮食健康度 0-100
  exercise: number // 运动频率 0-100
  sleep: number // 睡眠质量 0-100
  stress: number // 压力水平 0-100
}

// 游戏事件
export interface GameEvent extends BaseEntity {
  profileId: string
  eventDate: string
  eventType: EventType
  title: string
  description: string
  narrative: string
  choices: EventChoice[]
  impacts: EventImpact[]
  isCompleted: boolean
  selectedChoice?: number
  plausibility: number // 0-100，事件合理性评分
  emotionalWeight: number // 0-1，情感权重
}

// 事件类型
export type EventType = 
  | 'daily'       // 日常事件
  | 'milestone'   // 里程碑事件
  | 'crisis'      // 危机事件
  | 'opportunity' // 机会事件
  | 'relationship' // 关系事件

// 事件选择
export interface EventChoice {
  id: number
  text: string
  immediateImpacts: EventImpact[]
  longTermEffects: string[]
  riskLevel: number // 0-100
}

// 事件影响
export interface EventImpact {
  dimension: keyof FiveDimensions
  subDimension: string
  change: number // 变化值
  duration: number // 影响持续时间（天数）
}

// 记忆
export interface Memory extends BaseEntity {
  profileId: string
  eventId: string
  summary: string
  emotionalWeight: number // 0-1
  recallCount: number // 回忆次数
  lastRecalled: string
  retention: number // 保留度 0-1
}

// AI 推演结果
export interface AIReasoningResult {
  candidateEvents: GameEvent[]
  reasoning: string
  confidence: number // 0-100
  modelUsed: string
  cost: number // Token成本
}

// 规则校验结果
export interface RuleValidationResult {
  plausibility: number // 0-100
  conflicts: string[]
  warnings: string[]
  suggestions: string[]
}

// 时代规则
export interface EraRules {
  era: string
  economicConditions: number // -100到100
  socialNorms: Record<string, number> // 社会规范
  technologicalLevel: number // 0-100
  historicalEvents: HistoricalEvent[]
}

// 历史事件
export interface HistoricalEvent {
  year: number
  event: string
  globalImpact: number // -100到100
  region: string
}

// API 配置
export interface AIConfig {
  provider: 'siliconflow' | 'zhipu' | 'baidu' | 'aliyun' | 'openai' | 'anthropic' | 'local'
  model: string
  endpoint: string
  apiKey?: string
  isFree: boolean
  rateLimit: number
}

export interface SystemConfig {
  // 性能配置
  devicePerformanceScore: number // 0-100
  localModelEnabled: boolean
  localModelSize: '1.5B' | '3B' | '7B'
  
  // 游戏配置
  autoSave: boolean
  difficulty: 'easy' | 'normal' | 'hard'
  
  // 隐私配置
  dataEncryption: boolean
  anonymousStats: boolean
}