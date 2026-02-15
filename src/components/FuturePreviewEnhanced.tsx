import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLifeStore } from '../stores/lifeStore';
import { GameEvent } from '../../shared/types';
import { Eye, GitBranch, ArrowRight, Clock, Brain, Target, Users, Heart, Zap, Sparkles } from 'lucide-react';

interface FutureBranch {
  id: string;
  path: string;
  probability: number;
  outcomes: {
    health: number;
    intelligence: number;
    social: number;
    achievement: number;
    happiness: number;
  };
  keyEvents: GameEvent[];
  riskLevel: 'low' | 'medium' | 'high';
}

interface FuturePreviewProps {
  profileId: string;
}

const FuturePreview: React.FC<FuturePreviewProps> = ({ profileId }) => {
  const { events, currentState, isLoading } = useLifeStore();
  const [branches, setBranches] = useState<FutureBranch[]>([]);
  const [selectedBranch, setSelectedBranch] = useState<string | null>(null);
  const [predictionDays, setPredictionDays] = useState<number>(365);
  const [isGenerating, setIsGenerating] = useState(false);

  // 生成未来分支预测
  useEffect(() => {
    if (currentState && !isLoading) {
      generateFutureBranches();
    }
  }, [currentState, predictionDays]);

  const generateFutureBranches = async () => {
    setIsGenerating(true);
    
    // 模拟AI生成过程
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    // 生成三个不同的未来分支
    const newBranches: FutureBranch[] = [
      {
        id: 'branch-1',
        path: '稳健发展路径',
        probability: 0.35,
        outcomes: {
          health: currentState.health + 2.5,
          intelligence: currentState.intelligence + 1.8,
          social: currentState.social + 3.2,
          achievement: currentState.achievement + 4.1,
          happiness: currentState.happiness + 2.7
        },
        keyEvents: generateKeyEvents('稳健'),
        riskLevel: 'low'
      },
      {
        id: 'branch-2',
        path: '激进突破路径',
        probability: 0.45,
        outcomes: {
          health: currentState.health - 1.2,
          intelligence: currentState.intelligence + 4.5,
          social: currentState.social + 1.8,
          achievement: currentState.achievement + 6.8,
          happiness: currentState.happiness + 0.5
        },
        keyEvents: generateKeyEvents('激进'),
        riskLevel: 'high'
      },
      {
        id: 'branch-3',
        path: '平衡发展路径',
        probability: 0.20,
        outcomes: {
          health: currentState.health + 1.5,
          intelligence: currentState.intelligence + 2.3,
          social: currentState.social + 2.1,
          achievement: currentState.achievement + 2.9,
          happiness: currentState.happiness + 3.4
        },
        keyEvents: generateKeyEvents('平衡'),
        riskLevel: 'medium'
      }
    ];

    setBranches(newBranches);
    setIsGenerating(false);
  };

  // 生成关键事件
  const generateKeyEvents = (strategy: string): GameEvent[] => {
    const baseEvents: Record<string, Partial<GameEvent>[]> = {
      '稳健': [
        { type: 'career', description: '获得稳定晋升机会' },
        { type: 'relationship', description: '建立深厚友谊关系' },
        { type: 'health', description: '养成良好生活习惯' }
      ],
      '激进': [
        { type: 'career', description: '创业挑战高风险项目' },
        { type: 'education', description: '深入学习前沿技术' },
        { type: 'crisis', description: '面临重大职业抉择' }
      ],
      '平衡': [
        { type: 'milestone', description: '达成工作生活平衡' },
        { type: 'relationship', description: '维护家庭和谐关系' },
        { type: 'health', description: '适度锻炼保持健康' }
      ]
    };

    return baseEvents[strategy].map((event, index) => ({
      id: `future-${strategy}-${index}`,
      profileId,
      timestamp: new Date(Date.now() + (index + 1) * 30 * 24 * 60 * 60 * 1000).toISOString(),
      type: event.type || 'milestone',
      description: event.description || '',
      choices: [],
      consequences: [],
      isCompleted: false,
      createdAt: new Date().toISOString()
    })) as GameEvent[];
  };

  // 获取风险等级颜色
  const getRiskColor = (riskLevel: string) => {
    const colors: Record<string, string> = {
      low: 'from-green-500 to-emerald-500',
      medium: 'from-yellow-500 to-amber-500',
      high: 'from-red-500 to-orange-500'
    };
    return colors[riskLevel] || 'from-gray-500 to-slate-500';
  };

  // 获取路径图标
  const getPathIcon = (path: string) => {
    if (path.includes('稳健')) return <Target className="w-5 h-5" />;
    if (path.includes('激进')) return <Zap className="w-5 h-5" />;
    return <Heart className="w-5 h-5" />;
  };

  if (isGenerating) {
    return (
      <div className="p-8 text-center rounded-2xl bg-white/5 border border-white/10">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
          className="w-12 h-12 border-4 border-indigo-500/30 border-t-indigo-500 rounded-full mx-auto mb-4"
        />
        <h3 className="text-xl font-bold text-white mb-2">量子预测中</h3>
        <p className="text-slate-400">正在计算多种未来可能性...</p>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 overflow-hidden">
      {/* 头部控制面板 */}
      <div className="p-6 border-b border-white/10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Eye className="w-6 h-6" />
            未来分支预览
          </h2>
          
          <div className="flex items-center gap-4">
            {/* 时间范围选择 */}
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-slate-400" />
              <select
                value={predictionDays}
                onChange={(e) => setPredictionDays(Number(e.target.value))}
                className="px-3 py-1.5 bg-white/5 border border-white/10 rounded-lg text-white text-sm"
              >
                <option value={90}>3个月</option>
                <option value={180}>6个月</option>
                <option value={365}>1年</option>
                <option value={730}>2年</option>
                <option value={1825}>5年</option>
              </select>
            </div>
            
            {/* 刷新按钮 */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={generateFutureBranches}
              disabled={isGenerating}
              className="px-4 py-2 bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 rounded-lg hover:bg-indigo-500/30 transition-all disabled:opacity-50"
            >
              <Sparkles className="w-4 h-4 inline mr-2" />
              重新预测
            </motion.button>
          </div>
        </div>
      </div>

      {/* 分支对比视图 */}
      <div className="p-6">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {branches.map((branch) => (
            <BranchCard
              key={branch.id}
              branch={branch}
              isSelected={selectedBranch === branch.id}
              onSelect={() => setSelectedBranch(selectedBranch === branch.id ? null : branch.id)}
              getPathIcon={getPathIcon}
              getRiskColor={getRiskColor}
            />
          ))}
        </div>

        {/* 详细分析面板 */}
        <AnimatePresence>
          {selectedBranch && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: 'auto', opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              className="mt-6 p-6 rounded-xl bg-white/5 border border-white/10"
            >
              <BranchDetailPanel 
                branch={branches.find(b => b.id === selectedBranch)!}
                currentState={currentState}
              />
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// 分支卡片组件
const BranchCard: React.FC<{
  branch: FutureBranch;
  isSelected: boolean;
  onSelect: () => void;
  getPathIcon: (path: string) => React.ReactNode;
  getRiskColor: (risk: string) => string;
}> = ({ branch, isSelected, onSelect, getPathIcon, getRiskColor }) => (
  <motion.div
    layout
    className={`relative p-5 rounded-xl border transition-all cursor-pointer ${
      isSelected 
        ? 'bg-white/10 border-indigo-400 shadow-lg scale-105' 
        : 'bg-white/5 border-white/10 hover:bg-white/8 hover:scale-102'
    }`}
    onClick={onSelect}
    whileHover={{ y: -5 }}
    whileTap={{ scale: 0.98 }}
  >
    {/* 概率指示器 */}
    <div className="absolute top-3 right-3">
      <div className="flex items-center gap-1">
        <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
        <span className="text-xs font-bold text-green-400">{(branch.probability * 100).toFixed(0)}%</span>
      </div>
    </div>

    {/* 风险等级标签 */}
    <div className="absolute top-3 left-3">
      <div className={`px-2 py-1 rounded-full text-xs font-bold text-white bg-gradient-to-r ${getRiskColor(branch.riskLevel)}`}>
        {branch.riskLevel === 'low' ? '低风险' : branch.riskLevel === 'medium' ? '中风险' : '高风险'}
      </div>
    </div>

    {/* 主要内容 */}
    <div className="pt-8">
      <div className="flex items-center gap-3 mb-4">
        <div className={`p-2 rounded-lg bg-gradient-to-r ${getRiskColor(branch.riskLevel)} text-white`}>
          {getPathIcon(branch.path)}
        </div>
        <h3 className="font-bold text-white text-lg">{branch.path}</h3>
      </div>

      {/* 预期结果概览 */}
      <div className="grid grid-cols-2 gap-3 mb-4">
        {Object.entries(branch.outcomes).map(([dimension, value]) => (
          <div key={dimension} className="flex items-center justify-between">
            <span className="text-xs text-slate-400 capitalize">{dimension}</span>
            <span className={`text-sm font-bold ${
              value > (currentState?.[dimension as keyof typeof currentState] || 0)
                ? 'text-green-400' : 'text-slate-400'
            }`}>
              {value.toFixed(1)}
            </span>
          </div>
        ))}
      </div>

      {/* 关键事件预览 */}
      <div className="space-y-2">
        <div className="text-xs text-slate-500 font-medium">关键节点:</div>
        {branch.keyEvents.slice(0, 2).map((event, index) => (
          <div key={event.id} className="flex items-center gap-2 text-xs">
            <div className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
            <span className="text-slate-300 truncate">{event.description}</span>
          </div>
        ))}
        {branch.keyEvents.length > 2 && (
          <div className="text-xs text-slate-500">+{branch.keyEvents.length - 2} 更多事件</div>
        )}
      </div>

      {/* 选择指示器 */}
      {isSelected && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="mt-4 pt-4 border-t border-white/10 flex items-center justify-center text-indigo-400"
        >
          <ArrowRight className="w-4 h-4" />
        </motion.div>
      )}
    </div>
  </motion.div>
);

// 分支详情面板
const BranchDetailPanel: React.FC<{ 
  branch: FutureBranch; 
  currentState: any 
}> = ({ branch, currentState }) => {
  // 计算变化量
  const changes = Object.keys(branch.outcomes).reduce((acc, key) => {
    const current = currentState?.[key as keyof typeof currentState] || 0;
    const future = branch.outcomes[key as keyof typeof branch.outcomes];
    acc[key] = future - current;
    return acc;
  }, {} as Record<string, number>);

  return (
    <div className="space-y-6">
      <div>
        <h3 className="text-xl font-bold text-white mb-2">{branch.path} - 详细分析</h3>
        <p className="text-slate-400">基于当前状态和选择的深度预测分析</p>
      </div>

      {/* 维度变化对比 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="p-4 rounded-lg bg-white/5 border border-white/10">
          <h4 className="font-bold text-white mb-3">维度发展预测</h4>
          <div className="space-y-3">
            {Object.entries(changes).map(([dimension, change]) => (
              <div key={dimension} className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <ImpactIcon dimension={dimension} />
                  <span className="text-sm text-slate-300 capitalize">{dimension}</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-slate-400">
                    {currentState?.[dimension as keyof typeof currentState]?.toFixed(1) || 0}
                  </span>
                  <ArrowRight className="w-3 h-3 text-slate-500" />
                  <span className={`text-sm font-bold ${
                    change > 0 ? 'text-green-400' : change < 0 ? 'text-red-400' : 'text-slate-400'
                  }`}>
                    {branch.outcomes[dimension as keyof typeof branch.outcomes].toFixed(1)}
                  </span>
                  <span className={`text-xs ${
                    change > 0 ? 'text-green-400' : change < 0 ? 'text-red-400' : 'text-slate-400'
                  }`}>
                    ({change > 0 ? '+' : ''}{change.toFixed(1)})
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 关键事件时间线 */}
        <div className="p-4 rounded-lg bg-white/5 border border-white/10">
          <h4 className="font-bold text-white mb-3">预期关键节点</h4>
          <div className="space-y-3">
            {branch.keyEvents.map((event, index) => (
              <div key={event.id} className="flex items-start gap-3">
                <div className="flex flex-col items-center mt-1">
                  <div className="w-2 h-2 rounded-full bg-indigo-400" />
                  {index < branch.keyEvents.length - 1 && (
                    <div className="w-0.5 h-8 bg-indigo-400/30" />
                  )}
                </div>
                <div className="flex-1">
                  <div className="text-sm font-medium text-white">{event.description}</div>
                  <div className="text-xs text-slate-500">
                    {new Date(event.timestamp).toLocaleDateString()}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* 风险评估 */}
      <div className="p-4 rounded-lg bg-white/5 border border-white/10">
        <h4 className="font-bold text-white mb-3">风险评估</h4>
        <div className="grid grid-cols-3 gap-4">
          <RiskMetric 
            label="成功概率" 
            value={`${(branch.probability * 100).toFixed(0)}%`} 
            color="green" 
          />
          <RiskMetric 
            label="风险等级" 
            value={branch.riskLevel === 'low' ? '低' : branch.riskLevel === 'medium' ? '中' : '高'} 
            color={branch.riskLevel === 'low' ? 'green' : branch.riskLevel === 'medium' ? 'yellow' : 'red'} 
          />
          <RiskMetric 
            label="预期收益" 
            value="+15%" 
            color="blue" 
          />
        </div>
      </div>
    </div>
  );
};

// 风险指标组件
const RiskMetric: React.FC<{ 
  label: string; 
  value: string; 
  color: string 
}> = ({ label, value, color }) => {
  const colorClasses: Record<string, string> = {
    green: 'text-green-400',
    yellow: 'text-yellow-400',
    red: 'text-red-400',
    blue: 'text-blue-400'
  };

  return (
    <div className="text-center">
      <div className={`text-2xl font-bold ${colorClasses[color]}`}>{value}</div>
      <div className="text-xs text-slate-400 mt-1">{label}</div>
    </div>
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

export default FuturePreview;