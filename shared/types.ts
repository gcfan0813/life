// 五维系统类型定义
export interface FiveDimensionSystem {
  // 生理系统
  physical: {
    health: number; // 健康值 (0-100)
    energy: number; // 精力值 (0-100)
    appearance: number; // 外貌 (0-100)
    fitness: number; // 体能 (0-100)
  };
  
  // 心理系统
  psychological: {
    // 大五人格
    openness: number; // 开放性 (0-100)
    conscientiousness: number; // 尽责性 (0-100)
    extraversion: number; // 外向性 (0-100)
    agreeableness: number; // 宜人性 (0-100)
    neuroticism: number; // 神经质 (0-100)
    
    // 情绪状态
    happiness: number; // 幸福感 (0-100)
    stress: number; // 压力值 (0-100)
    resilience: number; // 韧性 (0-100)
  };
  
  // 社会系统
  social: {
    socialCapital: number; // 社会资本 (0-100)
    career: {
      level: number; // 职业等级 (0-100)
      satisfaction: number; // 职业满意度 (0-100)
      income: number; // 月收入 (元)
    };
    economic: {
      wealth: number; // 财富值 (万元)
      debt: number; // 负债 (万元)
      credit: number; // 信用评分 (0-100)
    };
  };
  
  // 认知系统
  cognitive: {
    knowledge: {
      academic: number; // 学术知识 (0-100)
      practical: number; // 实用技能 (0-100)
      creative: number; // 创造力 (0-100)
    };
    skills: {
      communication: number; // 沟通能力 (0-100)
      problemSolving: number; // 解决问题能力 (0-100)
      leadership: number; // 领导力 (0-100)
    };
    memory: {
      shortTerm: number; // 短期记忆 (0-100)
      longTerm: number; // 长期记忆 (0-100)
      emotional: number; // 情感记忆 (0-100)
    };
  };
  
  // 关系系统
  relational: {
    intimacy: {
      family: number; // 家庭亲密度 (0-100)
      friends: number; // 朋友亲密度 (0-100)
      romantic: number; // 浪漫关系 (0-100)
    };
    network: {
      size: number; // 网络规模 (人数)
      quality: number; // 网络质量 (0-100)
      diversity: number; // 网络多样性 (0-100)
    };
  };
}

// 角色状态
export interface CharacterState {
  id: string;
  profile_id: string;
  current_date: string; // YYYY-MM-DD
  age: number;
  dimensions: FiveDimensionSystem;
  
  // 动态属性
  location: string;
  occupation: string;
  education: string;
  
  // 时间相关
  life_stage: 'childhood' | 'teen' | 'youngAdult' | 'adult' | 'middleAge' | 'senior';
  
  // 统计信息
  total_events: number;
  total_decisions: number;
  days_survived: number;
}

// 游戏事件
export interface GameEvent {
  id: string;
  profile_id: string;
  event_date: string;
  event_type: 'milestone' | 'crisis' | 'opportunity' | 'relationship' | 'daily';
  title: string;
  description: string;
  narrative: string;
  
  // 事件属性
  plausibility: number; // 可信度 (0-100)
  emotional_weight: number; // 情感权重 (0-1)
  
  // 影响
  impacts: any[];
  
  // 选择项
  choices: EventChoice[];
  
  // 状态
  is_completed: boolean;
  selected_choice?: number;
  created_at: string;
  updated_at: string;
}

// 事件选择项
export interface EventChoice {
  id: number;
  text: string;
  riskLevel: number; // 风险等级 (0-100)
  
  // 即时影响
  immediateImpacts: Array<{
    dimension: keyof FiveDimensionSystem;
    subDimension: string;
    change: number;
  }>;
  
  // 长期效果
  longTermEffects: string[];
  
  // 特殊效果
  specialConditions?: string[];
}

// 人生档案
export interface LifeProfile {
  id: string;
  name: string;
  birth_date: string; // YYYY-MM-DD
  birth_place: string;
  gender: 'male' | 'female';
  initial_traits: {
    familyBackground: 'poor' | 'middle' | 'wealthy';
    educationLevel: 'none' | 'primary' | 'secondary' | 'college' | 'graduate';
    healthStatus: 'poor' | 'average' | 'good' | 'excellent';
    riskTolerance: number; // 风险承受度 (0-100)
    ambition: number; // 野心 (0-100)
    empathy: number; // 同理心 (0-100)
  };
  era: string;
  difficulty: string;
  created_at: string;
  updated_at: string;
}

// 记忆
export interface Memory {
  id: string;
  profile_id: string;
  event_id: string;
  summary: string;
  emotional_weight: number;
  recall_count: number;
  last_recalled: string | null;
  retention: number;
  created_at: string;
  updated_at: string;
}

// AI设置
export interface AISettings {
  useLocalModel: boolean;
  localModelSize: '1.5B' | '3B' | '7B';
  useFreeAPI: boolean;
  customAPI: string | null;
}

// 规则相关
export interface Rule {
  id: string;
  name: string;
  category: string;
  description: string;
  
  // 学术依据
  academicBasis: {
    source: string;
    credibility: 'high' | 'medium' | 'low';
    validationData?: string;
  };
  
  // 规则逻辑
  conditions: RuleCondition[];
  effects: RuleEffect[];
  
  // 元数据
  version: string;
  lastUpdated: string;
  isActive: boolean;
}

export interface RuleCondition {
  type: 'dimension' | 'event' | 'time' | 'age';
  dimension?: keyof FiveDimensionSystem;
  subDimension?: string;
  operator: '>' | '<' | '>=' | '<=' | '==' | '!=';
  value: number;
}

export interface RuleEffect {
  type: 'modify' | 'trigger' | 'constraint';
  dimension?: keyof FiveDimensionSystem;
  subDimension?: string;
  change: number;
  probability: number; // 效果触发概率 (0-100)
}