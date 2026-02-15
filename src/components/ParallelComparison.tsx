import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLifeStore } from '../stores/lifeStore';
import { GameEvent } from '../../shared/types';
import { GitBranch, BarChart3, TrendingUp, Users, Target, Heart, Brain, Zap, Eye, EyeOff } from 'lucide-react';

interface ParallelLife {
  id: string;
  name: string;
  profileId: string;
  events: GameEvent[];
  currentState: any;
  createdAt: string;
  isActive: boolean;
}

interface ComparisonMetrics {
  health: number[];
  intelligence: number[];
  social: number[];
  achievement: number[];
  happiness: number[];
}

interface ParallelComparisonProps {
  currentProfileId: string;
}

const ParallelComparison: React.FC<ParallelComparisonProps> = ({ currentProfileId }) => {
  const { events, currentState } = useLifeStore();
  const [parallelLives, setParallelLives] = useState<ParallelLife[]>([]);
  const [selectedLives, setSelectedLives] = useState<string[]>([]);
  const [comparisonMode, setComparisonMode] = useState<'metrics' | 'timeline' | 'events'>('metrics');
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newLifeName, setNewLifeName] = useState('');

  // 初始化并行人生数据
  useEffect(() => {
    initializeParallelLives();
  }, [currentProfileId, events, currentState]);

  const initializeParallelLives = () => {
    // 基于当前人生的三种不同路径创建并行人生
    const baseLives: ParallelLife[] = [
      {
        id: 'parallel-1',
        name: '稳健发展路径',
        profileId: currentProfileId,
        events: createAlternativeEvents(events, 'conservative'),
        currentState: createAlternativeState(currentState, 'conservative'),
        createdAt: new Date().toISOString(),
        isActive: true
      },
      {
        id: 'parallel-2',
        name: '激进突破路径',
        profileId: currentProfileId,
        events: createAlternativeEvents(events, 'aggressive'),
        currentState: createAlternativeState(currentState, 'aggressive'),
        createdAt: new Date().toISOString(),
        isActive: true
      },
      {
        id: 'parallel-3',
        name: '平衡发展路径',
        profileId: currentProfileId,
        events: createAlternativeEvents(events, 'balanced'),
        currentState: createAlternativeState(currentState, 'balanced'),
        createdAt: new Date().toISOString(),
        isActive: true
      }
    ];

    setParallelLives(baseLives);
    setSelectedLives(baseLives.map(life => life.id));
  };

  // 创建替代事件路径
  const createAlternativeEvents = (originalEvents: GameEvent[], strategy: string): GameEvent[] => {
    return originalEvents.map(event => {
      if (!event.isCompleted || !event.choices) return event;
      
      // 根据策略选择不同的选项
      let selectedIndex = 0;
      switch (strategy) {
        case 'conservative':
          // 选择最安全的选项
          selectedIndex = 0;
          break;
        case 'aggressive':
          // 选择最具挑战性的选项
          selectedIndex = event.choices.length - 1;
          break;
        case 'balanced':
          // 选择中间选项
          selectedIndex = Math.floor(event.choices.length / 2);
          break;
        default:
          selectedIndex = Math.floor(Math.random() * event.choices.length);
      }

      return {
        ...event,
        choices: event.choices.map((choice, index) => ({
          ...choice,
          selected: index === selectedIndex
        }))
      };
    });
  };

  // 创建替代状态
  const createAlternativeState = (originalState: any, strategy: string) => {
    if (!originalState) return originalState;

    const modifiers: Record<string, number> = {
      conservative: 0.9,
      aggressive: 1.2,
      balanced: 1.05
    };

    const modifier = modifiers[strategy] || 1;

    return {
      ...originalState,
      health: Math.min(100, originalState.health * (strategy === 'aggressive' ? 0.8 : modifier)),
      intelligence: Math.min(100, originalState.intelligence * modifier),
      social: Math.min(100, originalState.social * (strategy === 'conservative' ? 1.1 : modifier)),
      achievement: Math.min(100, originalState.achievement * modifier),
      happiness: Math.min(100, originalState.happiness * (strategy === 'balanced' ? 1.1 : 0.9))
    };
  };

  // 计算对比指标
  const calculateComparisonMetrics = (): ComparisonMetrics => {
    const selectedLivesData = parallelLives.filter(life => selectedLives.includes(life.id));
    
    return {
      health: selectedLivesData.map(life => life.currentState?.health || 0),
      intelligence: selectedLivesData.map(life => life.currentState?.intelligence || 0),
      social: selectedLivesData.map(life => life.currentState?.social || 0),
      achievement: selectedLivesData.map(life => life.currentState?.achievement || 0),
      happiness: selectedLivesData.map(life => life.currentState?.happiness || 0)
    };
  };

  // 获取平均值
  const getAverage = (values: number[]): number => {
    return values.length > 0 ? values.reduce((a, b) => a + b, 0) / values.length : 0;
  };

  // 获取最大值
  const getMax = (values: number[]): number => {
    return values.length > 0 ? Math.max(...values) : 0;
  };

  // 获取最小值
  const getMin = (values: number[]): number => {
    return values.length > 0 ? Math.min(...values) : 0;
  };

  const metrics = calculateComparisonMetrics();
  const selectedLivesData = parallelLives.filter(life => selectedLives.includes(life.id));

  return (
    <div className="rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 overflow-hidden">
      {/* 头部控制面板 */}
      <div className="p-6 border-b border-white/10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <GitBranch className="w-6 h-6" />
            并行人生对比
          </h2>
          
          <div className="flex flex-wrap gap-3">
            {/* 对比模式切换 */}
            <div className="flex bg-white/5 rounded-lg p-1">
              {(['metrics', 'timeline', 'events'] as const).map(mode => (
                <button
                  key={mode}
                  onClick={() => setComparisonMode(mode)}
                  className={`px-3 py-1.5 text-sm rounded-md transition-all capitalize ${
                    comparisonMode === mode
                      ? 'bg-white text-slate-900 shadow-sm'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {mode === 'metrics' ? '指标对比' : mode === 'timeline' ? '时间线' : '事件分析'}
                </button>
              ))}
            </div>

            {/* 人生选择器 */}
            <div className="flex flex-wrap gap-2">
              {parallelLives.map(life => (
                <button
                  key={life.id}
                  onClick={() => {
                    if (selectedLives.includes(life.id)) {
                      setSelectedLives(selectedLives.filter(id => id !== life.id));
                    } else {
                      setSelectedLives([...selectedLives, life.id]);
                    }
                  }}
                  className={`px-3 py-1.5 text-sm rounded-lg transition-all ${
                    selectedLives.includes(life.id)
                      ? 'bg-indigo-500/20 text-indigo-300 border border-indigo-500/30'
                      : 'bg-white/5 text-slate-400 hover:bg-white/10'
                  }`}
                >
                  {life.name}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* 主要内容区域 */}
      <div className="p-6">
        <AnimatePresence mode="wait">
          {comparisonMode === 'metrics' && (
            <motion.div
              key="metrics"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* 统计概览卡片 */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <StatCard 
                  title="平均健康值" 
                  value={getAverage(metrics.health).toFixed(1)} 
                  icon={<Heart className="w-5 h-5" />}
                  color="text-red-400"
                />
                <StatCard 
                  title="平均智力值" 
                  value={getAverage(metrics.intelligence).toFixed(1)} 
                  icon={<Brain className="w-5 h-5" />}
                  color="text-blue-400"
                />
                <StatCard 
                  title="平均成就值" 
                  value={getAverage(metrics.achievement).toFixed(1)} 
                  icon={<Target className="w-5 h-5" />}
                  color="text-yellow-400"
                />
              </div>

              {/* 详细对比图表 */}
              <div className="p-6 rounded-xl bg-white/5 border border-white/10">
                <h3 className="text-lg font-bold text-white mb-4 flex items-center gap-2">
                  <BarChart3 className="w-5 h-5" />
                  维度详细对比
                </h3>
                
                <div className="space-y-4">
                  {Object.entries({
                    health: '健康',
                    intelligence: '智力',
                    social: '社交',
                    achievement: '成就',
                    happiness: '幸福'
                  }).map(([key, label]) => (
                    <DimensionComparison
                      key={key}
                      dimension={label}
                      values={metrics[key as keyof ComparisonMetrics] as number[]}
                      lives={selectedLivesData}
                      getIcon={(dim: string) => {
                        const icons: Record<string, React.ReactNode> = {
                          health: <Heart className="w-4 h-4" />,
                          intelligence: <Brain className="w-4 h-4" />,
                          social: <Users className="w-4 h-4" />,
                          achievement: <Target className="w-4 h-4" />,
                          happiness: <Zap className="w-4 h-4" />
                        };
                        return icons[dim.toLowerCase()] || <TrendingUp className="w-4 h-4" />;
                      }}
                    />
                  ))}
                </div>
              </div>

              {/* 差异分析 */}
              <div className="p-6 rounded-xl bg-white/5 border border-white/10">
                <h3 className="text-lg font-bold text-white mb-4">路径差异分析</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <PathDifference 
                    title="最佳健康表现" 
                    value={getMax(metrics.health).toFixed(1)}
                    path={selectedLivesData[metrics.health.indexOf(getMax(metrics.health))]?.name || ''}
                    icon={<Heart className="w-4 h-4 text-red-400" />}
                  />
                  <PathDifference 
                    title="最高智力发展" 
                    value={getMax(metrics.intelligence).toFixed(1)}
                    path={selectedLivesData[metrics.intelligence.indexOf(getMax(metrics.intelligence))]?.name || ''}
                    icon={<Brain className="w-4 h-4 text-blue-400" />}
                  />
                  <PathDifference 
                    title="最优社交网络" 
                    value={getMax(metrics.social).toFixed(1)}
                    path={selectedLivesData[metrics.social.indexOf(getMax(metrics.social))]?.name || ''}
                    icon={<Users className="w-4 h-4 text-green-400" />}
                  />
                  <PathDifference 
                    title="最大成就感" 
                    value={getMax(metrics.achievement).toFixed(1)}
                    path={selectedLivesData[metrics.achievement.indexOf(getMax(metrics.achievement))]?.name || ''}
                    icon={<Target className="w-4 h-4 text-yellow-400" />}
                  />
                </div>
              </div>
            </motion.div>
          )}

          {comparisonMode === 'timeline' && (
            <motion.div
              key="timeline"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
            >
              <TimelineComparison lives={selectedLivesData} />
            </motion.div>
          )}

          {comparisonMode === 'events' && (
            <motion.div
              key="events"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: 20 }}
            >
              <EventAnalysis lives={selectedLivesData} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// 统计卡片组件
const StatCard: React.FC<{
  title: string;
  value: string;
  icon: React.ReactNode;
  color: string;
}> = ({ title, value, icon, color }) => (
  <div className="p-4 rounded-xl bg-white/5 border border-white/10">
    <div className="flex items-center justify-between mb-2">
      <span className="text-slate-400 text-sm">{title}</span>
      <div className={`p-2 rounded-lg bg-white/10 ${color}`}>
        {icon}
      </div>
    </div>
    <div className={`text-2xl font-bold ${color}`}>{value}</div>
  </div>
);

// 维度对比组件
const DimensionComparison: React.FC<{
  dimension: string;
  values: number[];
  lives: ParallelLife[];
  getIcon: (dimension: string) => React.ReactNode;
}> = ({ dimension, values, lives, getIcon }) => {
  const maxValue = Math.max(...values, 1);
  
  return (
    <div>
      <div className="flex items-center justify-between mb-2">
        <div className="flex items-center gap-2">
          {getIcon(dimension)}
          <span className="font-medium text-white">{dimension}</span>
        </div>
        <span className="text-sm text-slate-400">0 - 100</span>
      </div>
      
      <div className="space-y-2">
        {lives.map((life, index) => (
          <div key={life.id} className="flex items-center gap-3">
            <span className="text-xs text-slate-400 w-24 truncate">{life.name}</span>
            <div className="flex-1 h-6 bg-slate-800 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${(values[index] / maxValue) * 100}%` }}
                transition={{ duration: 1, delay: index * 0.1 }}
                className="h-full bg-gradient-to-r from-indigo-500 to-purple-500 rounded-full"
              />
            </div>
            <span className="text-sm font-bold text-white w-12 text-right">
              {values[index].toFixed(1)}
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};

// 路径差异组件
const PathDifference: React.FC<{
  title: string;
  value: string;
  path: string;
  icon: React.ReactNode;
}> = ({ title, value, path, icon }) => (
  <div className="p-3 rounded-lg bg-white/5 border border-white/10">
    <div className="flex items-center gap-2 mb-1">
      {icon}
      <span className="text-sm font-medium text-slate-300">{title}</span>
    </div>
    <div className="text-lg font-bold text-white">{value}</div>
    <div className="text-xs text-slate-400 truncate">{path}</div>
  </div>
);

// 时间线对比组件
const TimelineComparison: React.FC<{ lives: ParallelLife[] }> = ({ lives }) => (
  <div className="space-y-6">
    <h3 className="text-xl font-bold text-white">时间线发展对比</h3>
    
    <div className="relative">
      {/* 时间轴 */}
      <div className="absolute left-8 top-0 bottom-0 w-0.5 bg-slate-700" />
      
      {lives[0]?.events.slice(0, 5).map((event, index) => (
        <div key={event.id} className="relative pl-16 pb-8">
          {/* 时间点 */}
          <div className="absolute left-6 top-2 w-4 h-4 bg-indigo-500 rounded-full border-4 border-slate-900" />
          
          <div className="bg-white/5 rounded-xl p-4 border border-white/10">
            <div className="text-sm text-slate-400 mb-2">
              {new Date(event.timestamp).toLocaleDateString()}
            </div>
            <h4 className="font-bold text-white mb-2">{event.description}</h4>
            
            {/* 各路径的不同选择 */}
            <div className="space-y-2">
              {lives.map(life => {
                const lifeEvent = life.events.find(e => e.id === event.id);
                const selectedChoice = lifeEvent?.choices?.find(c => c.selected);
                
                return (
                  <div key={life.id} className="flex items-center gap-2 text-sm">
                    <div className="w-2 h-2 rounded-full bg-indigo-400" />
                    <span className="text-slate-300">{life.name}:</span>
                    <span className="text-white font-medium">
                      {selectedChoice?.description || '未选择'}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      ))}
    </div>
  </div>
);

// 事件分析组件
const EventAnalysis: React.FC<{ lives: ParallelLife[] }> = ({ lives }) => (
  <div className="space-y-6">
    <h3 className="text-xl font-bold text-white">关键决策分析</h3>
    
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {lives[0]?.events.filter(e => e.choices && e.choices.length > 1).slice(0, 4).map(event => (
        <div key={event.id} className="p-4 rounded-xl bg-white/5 border border-white/10">
          <h4 className="font-bold text-white mb-3">{event.description}</h4>
          
          <div className="space-y-2">
            {event.choices?.map((choice, choiceIndex) => {
              const choiceStats = lives.map(life => {
                const lifeEvent = life.events.find(e => e.id === event.id);
                return lifeEvent?.choices?.find((c, i) => i === choiceIndex && c.selected) ? 1 : 0;
              });
              
              const selectionCount = choiceStats.reduce((a, b) => a + b, 0);
              const percentage = (selectionCount / lives.length) * 100;
              
              return (
                <div key={choiceIndex} className="flex items-center gap-3">
                  <div className="flex-1">
                    <div className="text-sm text-slate-300 mb-1">{choice.description}</div>
                    <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                      <div 
                        className="h-full bg-gradient-to-r from-green-500 to-emerald-500 rounded-full transition-all duration-500"
                        style={{ width: `${percentage}%` }}
                      />
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm font-bold text-white">{selectionCount}/{lives.length}</div>
                    <div className="text-xs text-slate-400">{percentage.toFixed(0)}%</div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  </div>
);

export default ParallelComparison;