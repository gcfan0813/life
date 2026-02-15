import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLifeStore } from '../stores/lifeStore';
import { GameEvent } from '../../shared/types';
import { GitBranch, ArrowRight, Clock, Brain, Target, Users, Heart, Zap } from 'lucide-react';

interface CausalityNode {
  id: string;
  eventId: string;
  eventType: string;
  description: string;
  timestamp: string;
  impact: {
    health: number;
    intelligence: number;
    social: number;
    achievement: number;
    happiness: number;
  };
  connections: string[]; // 连接到的节点ID
  level: number; // 层级深度
}

interface CausalityChainProps {
  profileId: string;
}

const CausalityChain: React.FC<CausalityChainProps> = ({ profileId }) => {
  const { events, currentState } = useLifeStore();
  const [causalityNodes, setCausalityNodes] = useState<CausalityNode[]>([]);
  const [selectedNode, setSelectedNode] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'timeline' | 'network' | 'impact'>('timeline');
  const [filterType, setFilterType] = useState<string>('all');

  // 构建因果网络
  useEffect(() => {
    if (events.length > 0 && currentState) {
      const nodes = buildCausalityNetwork(events, currentState);
      setCausalityNodes(nodes);
    }
  }, [events, currentState]);

  // 构建因果网络的核心算法
  const buildCausalityNetwork = (events: GameEvent[], currentState: any): CausalityNode[] => {
    const nodes: CausalityNode[] = [];
    let currentNodeId = 0;

    // 从最早的事件开始构建网络
    const sortedEvents = [...events].sort((a, b) => 
      new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime()
    );

    // 创建初始节点（出生事件）
    if (sortedEvents.length > 0) {
      const birthEvent = sortedEvents[0];
      nodes.push({
        id: `node-${currentNodeId++}`,
        eventId: birthEvent.id,
        eventType: birthEvent.type,
        description: birthEvent.description,
        timestamp: birthEvent.timestamp,
        impact: { health: 0, intelligence: 0, social: 0, achievement: 0, happiness: 0 },
        connections: [],
        level: 0
      });
    }

    // 为每个事件创建节点并建立因果关系
    for (let i = 1; i < sortedEvents.length; i++) {
      const event = sortedEvents[i];
      const previousEvent = sortedEvents[i - 1];
      
      // 计算事件影响
      const impact = calculateEventImpact(event, previousEvent);
      
      const node: CausalityNode = {
        id: `node-${currentNodeId++}`,
        eventId: event.id,
        eventType: event.type,
        description: event.description,
        timestamp: event.timestamp,
        impact,
        connections: [], // 将在下一步建立连接
        level: i
      };

      // 建立因果连接（简单的时间顺序连接）
      if (nodes.length > 0) {
        const previousNode = nodes[nodes.length - 1];
        previousNode.connections.push(node.id);
      }

      nodes.push(node);
    }

    return nodes;
  };

  // 计算事件影响
  const calculateEventImpact = (event: GameEvent, previousEvent: GameEvent) => {
    const impact = {
      health: 0,
      intelligence: 0,
      social: 0,
      achievement: 0,
      happiness: 0
    };

    // 根据事件类型和选择计算影响
    switch (event.type) {
      case 'education':
        impact.intelligence += 2;
        impact.achievement += 1;
        break;
      case 'career':
        impact.achievement += 3;
        impact.social += 1;
        break;
      case 'relationship':
        impact.social += 2;
        impact.happiness += 2;
        break;
      case 'health':
        impact.health += event.choices?.[0]?.outcomes?.health || 0;
        impact.happiness += event.choices?.[0]?.outcomes?.happiness || 0;
        break;
      default:
        // 默认影响
        impact.health += 0.5;
        impact.happiness += 0.5;
    }

    return impact;
  };

  // 获取节点的视觉表示
  const getNodeColor = (eventType: string) => {
    const colors: Record<string, string> = {
      birth: 'from-pink-500 to-rose-500',
      education: 'from-blue-500 to-cyan-500',
      career: 'from-green-500 to-emerald-500',
      relationship: 'from-purple-500 to-violet-500',
      health: 'from-red-500 to-orange-500',
      milestone: 'from-yellow-500 to-amber-500',
      crisis: 'from-gray-500 to-slate-500'
    };
    return colors[eventType] || 'from-indigo-500 to-purple-500';
  };

  // 获取影响力最大的维度
  const getPrimaryImpact = (impact: CausalityNode['impact']) => {
    const entries = Object.entries(impact);
    return entries.reduce((max, current) => 
      Math.abs(current[1]) > Math.abs(max[1]) ? current : max
    )[0];
  };

  // 过滤节点
  const filteredNodes = causalityNodes.filter(node => 
    filterType === 'all' || node.eventType === filterType
  );

  if (causalityNodes.length === 0) {
    return (
      <div className="p-8 text-center rounded-2xl bg-white/5 border border-white/10">
        <GitBranch className="w-12 h-12 mx-auto text-slate-600 mb-4" />
        <h3 className="text-xl font-bold text-white mb-2">因果网络构建中</h3>
        <p className="text-slate-400">等待更多人生事件来构建完整的因果链</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 overflow-hidden">
      {/* 头部控制面板 */}
      <div className="p-6 border-b border-white/10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <GitBranch className="w-6 h-6" />
            人生因果链追溯
          </h2>
          
          <div className="flex flex-wrap gap-3">
            {/* 视图模式切换 */}
            <div className="flex bg-white/5 rounded-lg p-1">
              {(['timeline', 'network', 'impact'] as const).map(mode => (
                <button
                  key={mode}
                  onClick={() => setViewMode(mode)}
                  className={`px-3 py-1.5 text-sm rounded-md transition-all ${
                    viewMode === mode
                      ? 'bg-white text-slate-900 shadow-sm'
                      : 'text-slate-400 hover:text-white'
                  }`}
                >
                  {mode === 'timeline' ? '时间线' : mode === 'network' ? '网络图' : '影响力'}
                </button>
              ))}
            </div>
            
            {/* 类型过滤器 */}
            <select
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
              className="px-3 py-1.5 bg-white/5 border border-white/10 rounded-lg text-white text-sm"
            >
              <option value="all">全部事件</option>
              <option value="education">教育</option>
              <option value="career">职业</option>
              <option value="relationship">关系</option>
              <option value="health">健康</option>
              <option value="milestone">里程碑</option>
            </select>
          </div>
        </div>
      </div>

      {/* 主要内容区域 */}
      <div className="p-6">
        <AnimatePresence mode="wait">
          {viewMode === 'timeline' && (
            <motion.div
              key="timeline"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-4"
            >
              {filteredNodes.map((node, index) => (
                <CausalityTimelineNode
                  key={node.id}
                  node={node}
                  isSelected={selectedNode === node.id}
                  onSelect={() => setSelectedNode(selectedNode === node.id ? null : node.id)}
                  getNextNode={() => filteredNodes[index + 1]}
                />
              ))}
            </motion.div>
          )}

          {viewMode === 'network' && (
            <motion.div
              key="network"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              className="min-h-96 flex items-center justify-center"
            >
              <CausalityNetworkView nodes={filteredNodes} />
            </motion.div>
          )}

          {viewMode === 'impact' && (
            <motion.div
              key="impact"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
            >
              <ImpactAnalysisPanel nodes={filteredNodes} />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// 时间线节点组件
const CausalityTimelineNode: React.FC<{
  node: CausalityNode;
  isSelected: boolean;
  onSelect: () => void;
  getNextNode: () => CausalityNode | undefined;
}> = ({ node, isSelected, onSelect, getNextNode }) => {
  const primaryImpact = getPrimaryImpact(node.impact);
  const nextNode = getNextNode();

  return (
    <motion.div
      layout
      className={`relative p-4 rounded-xl border transition-all cursor-pointer ${
        isSelected 
          ? 'bg-white/10 border-indigo-400 shadow-lg' 
          : 'bg-white/5 border-white/10 hover:bg-white/8'
      }`}
      onClick={onSelect}
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      {/* 连接线 */}
      {nextNode && (
        <div className="absolute left-8 top-full w-0.5 h-4 bg-gradient-to-b from-indigo-500/30 to-transparent" />
      )}

      <div className="flex items-start gap-4">
        {/* 时间标记 */}
        <div className="flex flex-col items-center">
          <div className={`w-4 h-4 rounded-full bg-gradient-to-r ${getNodeColor(node.eventType)}`} />
          <div className="text-xs text-slate-500 mt-1">
            {new Date(node.timestamp).toLocaleDateString()}
          </div>
        </div>

        {/* 内容区域 */}
        <div className="flex-1">
          <div className="flex items-start justify-between">
            <div>
              <h3 className="font-bold text-white mb-1">{node.description}</h3>
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <span className="px-2 py-1 bg-white/10 rounded-full">
                  {node.eventType}
                </span>
                <span>层级: {node.level}</span>
              </div>
            </div>
            
            {isSelected && (
              <motion.div
                initial={{ rotate: 0 }}
                animate={{ rotate: 180 }}
                className="text-indigo-400"
              >
                <ArrowRight className="w-4 h-4" />
              </motion.div>
            )}
          </div>

          {/* 影响力指标 */}
          <AnimatePresence>
            {isSelected && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: 'auto', opacity: 1 }}
                exit={{ height: 0, opacity: 0 }}
                className="mt-3 pt-3 border-t border-white/10"
              >
                <div className="grid grid-cols-2 gap-2">
                  {Object.entries(node.impact).map(([dimension, value]) => (
                    <div key={dimension} className="flex items-center gap-2">
                      <ImpactIcon dimension={dimension} />
                      <span className="text-xs text-slate-300 capitalize">{dimension}</span>
                      <span className={`text-xs font-bold ${
                        value > 0 ? 'text-green-400' : value < 0 ? 'text-red-400' : 'text-slate-400'
                      }`}>
                        {value > 0 ? '+' : ''}{value.toFixed(1)}
                      </span>
                    </div>
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </motion.div>
  );
};

// 网络视图组件
const CausalityNetworkView: React.FC<{ nodes: CausalityNode[] }> = ({ nodes }) => {
  // 简化的网络可视化
  return (
    <div className="relative w-full h-96">
      <svg className="w-full h-full" viewBox="0 0 800 400">
        {/* 连接线 */}
        {nodes.slice(0, -1).map((node, index) => {
          const nextNode = nodes[index + 1];
          if (!nextNode) return null;
          
          return (
            <line
              key={`line-${node.id}`}
              x1={100 + index * 150}
              y1={200}
              x2={100 + (index + 1) * 150}
              y2={200}
              stroke="url(#gradient)"
              strokeWidth="2"
              strokeDasharray="5,5"
            />
          );
        })}

        {/* 节点 */}
        {nodes.map((node, index) => (
          <g key={node.id}>
            <circle
              cx={100 + index * 150}
              cy={200}
              r="20"
              fill={`url(#${getNodeColor(node.eventType).split(' ')[1]})`}
              className="cursor-pointer hover:opacity-80 transition-opacity"
            />
            <text
              x={100 + index * 150}
              y={240}
              textAnchor="middle"
              className="text-xs fill-slate-300"
            >
              {node.eventType.substring(0, 3)}
            </text>
          </g>
        ))}

        {/* 渐变定义 */}
        <defs>
          <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stopColor="#818cf8" />
            <stop offset="100%" stopColor="#c084fc" />
          </linearGradient>
        </defs>
      </svg>
    </div>
  );
};

// 影响力分析面板
const ImpactAnalysisPanel: React.FC<{ nodes: CausalityNode[] }> = ({ nodes }) => {
  // 计算总体影响
  const totalImpact = nodes.reduce((acc, node) => {
    Object.keys(acc).forEach(key => {
      acc[key as keyof typeof acc] += node.impact[key as keyof typeof node.impact];
    });
    return acc;
  }, { health: 0, intelligence: 0, social: 0, achievement: 0, happiness: 0 });

  const impactEntries = Object.entries(totalImpact);

  return (
    <>
      {/* 总体影响力 */}
      <div className="col-span-full p-4 rounded-xl bg-white/5 border border-white/10">
        <h3 className="font-bold text-white mb-3">总体影响力分析</h3>
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
          {impactEntries.map(([dimension, value]) => (
            <div key={dimension} className="text-center">
              <ImpactIcon dimension={dimension} />
              <div className="text-xs text-slate-400 capitalize mt-1">{dimension}</div>
              <div className={`text-lg font-bold ${
                value > 0 ? 'text-green-400' : value < 0 ? 'text-red-400' : 'text-slate-400'
              }`}>
                {value > 0 ? '+' : ''}{value.toFixed(1)}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* 事件类型分布 */}
      <div className="p-4 rounded-xl bg-white/5 border border-white/10">
        <h3 className="font-bold text-white mb-3">事件类型分布</h3>
        <div className="space-y-2">
          {Array.from(new Set(nodes.map(n => n.eventType))).map(type => {
            const count = nodes.filter(n => n.eventType === type).length;
            const percentage = (count / nodes.length) * 100;
            
            return (
              <div key={type} className="flex items-center justify-between">
                <span className="text-sm text-slate-300 capitalize">{type}</span>
                <div className="flex items-center gap-2">
                  <div className="w-20 h-2 bg-slate-700 rounded-full overflow-hidden">
                    <div 
                      className={`h-full bg-gradient-to-r ${getNodeColor(type)}`}
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                  <span className="text-xs text-slate-400 w-8">{count}</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </>
  );
};

// 影响力图标组件
const ImpactIcon: React.FC<{ dimension: string }> = ({ dimension }) => {
  const icons: Record<string, React.ReactNode> = {
    health: <Heart className="w-4 h-4 text-red-400" />,
    intelligence: <Brain className="w-4 h-4 text-blue-400" />,
    social: <Users className="w-4 h-4 text-green-400" />,
    achievement: <Target className="w-4 h-4 text-yellow-400" />,
    happiness: <Zap className="w-4 h-4 text-purple-400" />
  };
  
  return icons[dimension] || <Clock className="w-4 h-4 text-slate-400" />;
};

// 导出辅助函数供其他组件使用
export const getCausalityStats = (nodes: CausalityNode[]) => {
  const stats = {
    totalEvents: nodes.length,
    positiveImpacts: nodes.filter(node => 
      Object.values(node.impact).some(val => val > 0)
    ).length,
    negativeImpacts: nodes.filter(node => 
      Object.values(node.impact).some(val => val < 0)
    ).length,
    mostAffectedDimension: getPrimaryImpact(
      nodes.reduce((acc, node) => {
        Object.keys(acc).forEach(key => {
          acc[key as keyof typeof acc] += Math.abs(node.impact[key as keyof typeof node.impact]);
        });
        return acc;
      }, { health: 0, intelligence: 0, social: 0, achievement: 0, happiness: 0 })
    )
  };
  
  return stats;
};

export default CausalityChain;