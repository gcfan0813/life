import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLifeStore } from '../stores/lifeStore';
import { GameEvent } from '../../shared/types';
import { Brain, Lightbulb, Zap, Target, Users, Heart, AlertTriangle, CheckCircle, XCircle } from 'lucide-react';

interface AIRecommendation {
  id: string;
  type: 'choice' | 'timing' | 'strategy' | 'warning';
  title: string;
  description: string;
  confidence: number; // 0-100
  priority: 'high' | 'medium' | 'low';
  suggestedAction: string;
  rationale: string;
  alternativeOptions: string[];
}

interface DecisionContext {
  currentEvent: GameEvent;
  currentState: any;
  previousChoices: string[];
  timelinePosition: number;
}

interface AIAssistantProps {
  currentEvent?: GameEvent;
  onDecisionMade?: (choiceIndex: number, recommendationId: string) => void;
}

const AIAssistant: React.FC<AIAssistantProps> = ({ currentEvent, onDecisionMade }) => {
  const { currentState, events } = useLifeStore();
  const [recommendations, setRecommendations] = useState<AIRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<'suggestions' | 'analysis' | 'history'>('suggestions');
  const [showDetail, setShowDetail] = useState<string | null>(null);

  // 当事件改变时重新生成建议
  useEffect(() => {
    if (currentEvent && currentState) {
      generateRecommendations();
    }
  }, [currentEvent, currentState]);

  const generateRecommendations = async () => {
    setIsLoading(true);
    
    // 模拟AI分析过程
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    if (!currentEvent || !currentState) return;

    const context: DecisionContext = {
      currentEvent,
      currentState,
      previousChoices: events
        .filter(e => e.isCompleted)
        .flatMap(e => e.choices || [])
        .map(c => c.description),
      timelinePosition: events.filter(e => e.isCompleted).length
    };

    const newRecommendations = analyzeEventWithContext(context);
    setRecommendations(newRecommendations);
    setIsLoading(false);
  };

  const analyzeEventWithContext = (context: DecisionContext): AIRecommendation[] => {
    const recommendations: AIRecommendation[] = [];
    const { currentEvent, currentState, previousChoices, timelinePosition } = context;

    // 1. 基于事件类型的建议
    if (currentEvent.type === 'career') {
      recommendations.push({
        id: 'career-1',
        type: 'choice',
        title: '职业发展建议',
        description: '根据你的技能水平和当前市场状况',
        confidence: 85,
        priority: 'high',
        suggestedAction: currentEvent.choices?.[0]?.description || '选择第一个选项',
        rationale: '你的智力和成就指数表明你适合挑战性工作',
        alternativeOptions: currentEvent.choices?.slice(1).map(c => c.description) || []
      });
    }

    // 2. 基于个人状态的警告
    if (currentState.health < 30) {
      recommendations.push({
        id: 'health-warning',
        type: 'warning',
        title: '健康风险提醒',
        description: '当前健康状况需要特别关注',
        confidence: 90,
        priority: 'high',
        suggestedAction: '优先选择有利于健康的选项',
        rationale: '低健康值会影响所有其他维度的发展',
        alternativeOptions: []
      });
    }

    // 3. 基于历史选择的模式分析
    const recentChoices = previousChoices.slice(-5);
    const aggressiveChoices = recentChoices.filter(choice => 
      choice.toLowerCase().includes('冒险') || 
      choice.toLowerCase().includes('挑战') ||
      choice.toLowerCase().includes('全力')
    );

    if (aggressiveChoices.length >= 3) {
      recommendations.push({
        id: 'pattern-analysis',
        type: 'strategy',
        title: '行为模式分析',
        description: '检测到连续激进行为模式',
        confidence: 75,
        priority: 'medium',
        suggestedAction: '考虑平衡发展策略',
        rationale: '连续激进选择可能导致长期风险积累',
        alternativeOptions: ['选择稳健发展路径', '寻求平衡点']
      });
    }

    // 4. 时机建议
    if (timelinePosition < 10) {
      recommendations.push({
        id: 'timing-early',
        type: 'timing',
        title: '早期发展阶段',
        description: '人生初期建议多尝试和学习',
        confidence: 80,
        priority: 'medium',
        suggestedAction: '选择能带来多样化经验的选项',
        rationale: '年轻时期是探索和积累的最佳时机',
        alternativeOptions: []
      });
    }

    // 5. 维度平衡建议
    const dimensions = ['health', 'intelligence', 'social', 'achievement', 'happiness'];
    const lowestDimension = dimensions.reduce((min, dim) => 
      currentState[dim] < currentState[min] ? dim : min
    );

    if (currentState[lowestDimension] < 40) {
      recommendations.push({
        id: 'balance-' + lowestDimension,
        type: 'strategy',
        title: `${lowestDimension}维度需要关注`,
        description: `当前${lowestDimension}指数偏低`,
        confidence: 70,
        priority: 'medium',
        suggestedAction: `优先选择能提升${lowestDimension}的选项`,
        rationale: `平衡发展各维度有助于长期稳定成长`,
        alternativeOptions: [`寻找${lowestDimension}与其他维度的平衡点`]
      });
    }

    return recommendations.sort((a, b) => {
      // 按优先级排序：high > medium > low
      const priorityOrder = { high: 3, medium: 2, low: 1 };
      if (priorityOrder[a.priority] !== priorityOrder[b.priority]) {
        return priorityOrder[b.priority] - priorityOrder[a.priority];
      }
      // 同优先级按置信度排序
      return b.confidence - a.confidence;
    });
  };

  const getRecommendationIcon = (type: string) => {
    const icons: Record<string, React.ReactNode> = {
      choice: <Target className="w-5 h-5" />,
      timing: <Clock className="w-5 h-5" />,
      strategy: <Brain className="w-5 h-5" />,
      warning: <AlertTriangle className="w-5 h-5" />
    };
    return icons[type] || <Lightbulb className="w-5 h-5" />;
  };

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      high: 'from-red-500 to-orange-500',
      medium: 'from-yellow-500 to-amber-500',
      low: 'from-green-500 to-emerald-500'
    };
    return colors[priority] || 'from-gray-500 to-slate-500';
  };

  const handleRecommendationClick = (recommendation: AIRecommendation) => {
    if (recommendation.type === 'choice' && currentEvent?.choices) {
      // 尝试匹配建议的动作与现有选项
      const matchedChoice = currentEvent.choices.findIndex(choice => 
        recommendation.suggestedAction.includes(choice.description) ||
        choice.description.includes(recommendation.suggestedAction)
      );
      
      if (matchedChoice !== -1 && onDecisionMade) {
        onDecisionMade(matchedChoice, recommendation.id);
      }
    }
    setShowDetail(showDetail === recommendation.id ? null : recommendation.id);
  };

  if (!currentEvent) {
    return (
      <div className="p-6 text-center rounded-2xl bg-white/5 border border-white/10">
        <Brain className="w-12 h-12 mx-auto text-slate-600 mb-4" />
        <h3 className="text-xl font-bold text-white mb-2">AI助手待命中</h3>
        <p className="text-slate-400">等待事件发生以提供智能建议</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 overflow-hidden">
      {/* 头部 */}
      <div className="p-6 border-b border-white/10">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Brain className="w-6 h-6 text-indigo-400" />
            AI决策助手
          </h2>
          
          <div className="flex bg-white/5 rounded-lg p-1">
            {(['suggestions', 'analysis', 'history'] as const).map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-3 py-1.5 text-sm rounded-md transition-all capitalize ${
                  activeTab === tab
                    ? 'bg-white text-slate-900 shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 主要内容 */}
      <div className="p-6">
        <AnimatePresence mode="wait">
          {activeTab === 'suggestions' && (
            <motion.div
              key="suggestions"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
            >
              {isLoading ? (
                <div className="flex items-center justify-center py-12">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-8 h-8 border-2 border-indigo-500 border-t-transparent rounded-full"
                  />
                  <span className="ml-3 text-slate-400">AI分析中...</span>
                </div>
              ) : recommendations.length > 0 ? (
                <div className="space-y-4">
                  {recommendations.map((rec) => (
                    <RecommendationCard
                      key={rec.id}
                      recommendation={rec}
                      isSelected={showDetail === rec.id}
                      onClick={() => handleRecommendationClick(rec)}
                      getRecommendationIcon={getRecommendationIcon}
                      getPriorityColor={getPriorityColor}
                    />
                  ))}
                </div>
              ) : (
                <div className="text-center py-12">
                  <CheckCircle className="w-12 h-12 mx-auto text-green-500/50 mb-4" />
                  <h3 className="text-lg font-bold text-white mb-2">暂无特殊建议</h3>
                  <p className="text-slate-400">当前选择看起来都很合理</p>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'analysis' && (
            <motion.div
              key="analysis"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
            >
              <StateAnalysis currentState={currentState} currentEvent={currentEvent} />
            </motion.div>
          )}

          {activeTab === 'history' && (
            <motion.div
              key="history"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
            >
              <DecisionHistory events={events} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// 推荐卡片组件
const RecommendationCard: React.FC<{
  recommendation: AIRecommendation;
  isSelected: boolean;
  onClick: () => void;
  getRecommendationIcon: (type: string) => React.ReactNode;
  getPriorityColor: (priority: string) => string;
}> = ({ recommendation, isSelected, onClick, getRecommendationIcon, getPriorityColor }) => (
  <motion.div
    layout
    className={`relative p-4 rounded-xl border transition-all cursor-pointer ${
      isSelected 
        ? 'bg-white/10 border-indigo-400 shadow-lg' 
        : 'bg-white/5 border-white/10 hover:bg-white/8'
    }`}
    onClick={onClick}
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.98 }}
  >
    <div className="flex items-start gap-4">
      {/* 图标和优先级 */}
      <div className="flex flex-col items-center">
        <div className={`p-2 rounded-lg bg-gradient-to-r ${getPriorityColor(recommendation.priority)} text-white`}>
          {getRecommendationIcon(recommendation.type)}
        </div>
        <div className="mt-2 text-center">
          <div className="text-xs font-bold text-white capitalize">{recommendation.priority}</div>
          <div className="text-xs text-slate-400">{recommendation.confidence}%</div>
        </div>
      </div>

      {/* 内容 */}
      <div className="flex-1">
        <h3 className="font-bold text-white mb-1">{recommendation.title}</h3>
        <p className="text-slate-300 text-sm mb-3">{recommendation.description}</p>
        
        <div className="flex items-center gap-2 text-xs">
          <span className="px-2 py-1 bg-white/10 rounded-full text-slate-300">
            建议: {recommendation.suggestedAction}
          </span>
        </div>

        {/* 详细信息展开 */}
        <AnimatePresence>
          {isSelected && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="mt-3 pt-3 border-t border-white/10"
            >
              <div className="space-y-2">
                <div>
                  <h4 className="text-xs font-bold text-slate-300 mb-1">理由:</h4>
                  <p className="text-xs text-slate-400">{recommendation.rationale}</p>
                </div>
                
                {recommendation.alternativeOptions.length > 0 && (
                  <div>
                    <h4 className="text-xs font-bold text-slate-300 mb-1">替代方案:</h4>
                    <ul className="text-xs text-slate-400 space-y-1">
                      {recommendation.alternativeOptions.map((option, index) => (
                        <li key={index} className="flex items-center gap-1">
                          <div className="w-1 h-1 rounded-full bg-slate-500" />
                          {option}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* 展开指示器 */}
      <div className={`transition-transform ${isSelected ? 'rotate-180' : ''}`}>
        <svg className="w-4 h-4 text-slate-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </div>
    </div>
  </motion.div>
);

// 状态分析组件
const StateAnalysis: React.FC<{ currentState: any; currentEvent: GameEvent }> = ({ currentState, currentEvent }) => (
  <div className="space-y-6">
    <div>
      <h3 className="text-xl font-bold text-white mb-4">当前状态分析</h3>
      
      {/* 维度雷达图（简化版） */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
        {Object.entries({
          health: currentState.health,
          intelligence: currentState.intelligence,
          social: currentState.social,
          achievement: currentState.achievement,
          happiness: currentState.happiness
        }).map(([dimension, value]) => (
          <div key={dimension} className="text-center">
            <div className="relative w-16 h-16 mx-auto mb-2">
              <svg className="w-16 h-16 transform -rotate-90">
                <circle
                  cx="32"
                  cy="32"
                  r="28"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                  className="text-slate-700"
                />
                <circle
                  cx="32"
                  cy="32"
                  r="28"
                  stroke="currentColor"
                  strokeWidth="4"
                  fill="none"
                  strokeDasharray={`${2 * Math.PI * 28}`}
                  strokeDashoffset={`${2 * Math.PI * 28 * (1 - value / 100)}`}
                  className="text-indigo-400 transition-all duration-500"
                />
              </svg>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-xs font-bold text-white">{Math.round(value)}</span>
              </div>
            </div>
            <div className="text-xs text-slate-400 capitalize">{dimension}</div>
          </div>
        ))}
      </div>

      {/* 事件相关性分析 */}
      <div className="p-4 rounded-lg bg-white/5 border border-white/10">
        <h4 className="font-bold text-white mb-3">事件匹配度分析</h4>
        <div className="space-y-2">
          <AnalysisItem 
            label="技能匹配度" 
            value={85} 
            description="与你的专业技能高度匹配"
          />
          <AnalysisItem 
            label="风险承受度" 
            value={70} 
            description="在你的风险偏好范围内"
          />
          <AnalysisItem 
            label="时机适宜度" 
            value={90} 
            description="当前是行动的好时机"
          />
        </div>
      </div>
    </div>
  </div>
);

// 分析项目组件
const AnalysisItem: React.FC<{ label: string; value: number; description: string }> = ({ label, value, description }) => (
  <div className="flex items-center justify-between">
    <div>
      <div className="text-sm font-medium text-white">{label}</div>
      <div className="text-xs text-slate-400">{description}</div>
    </div>
    <div className="flex items-center gap-2">
      <div className="w-20 h-2 bg-slate-700 rounded-full overflow-hidden">
        <div 
          className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-500"
          style={{ width: `${value}%` }}
        />
      </div>
      <span className="text-sm font-bold text-indigo-400 w-8">{value}%</span>
    </div>
  </div>
);

// 决策历史组件
const DecisionHistory: React.FC<{ events: GameEvent[] }> = ({ events }) => {
  const completedEvents = events.filter(e => e.isCompleted).slice(-10);
  
  return (
    <div>
      <h3 className="text-xl font-bold text-white mb-4">近期决策历史</h3>
      
      {completedEvents.length === 0 ? (
        <div className="text-center py-8">
          <XCircle className="w-12 h-12 mx-auto text-slate-600 mb-3" />
          <p className="text-slate-400">暂无历史决策记录</p>
        </div>
      ) : (
        <div className="space-y-3">
          {completedEvents.map((event) => (
            <div key={event.id} className="p-3 rounded-lg bg-white/5 border border-white/10">
              <div className="flex items-center justify-between">
                <div>
                  <div className="font-medium text-white text-sm">{event.description}</div>
                  <div className="text-xs text-slate-400">
                    {new Date(event.timestamp).toLocaleDateString()}
                  </div>
                </div>
                <div className="px-2 py-1 bg-green-500/20 text-green-400 text-xs rounded-full">
                  已完成
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default AIAssistant;