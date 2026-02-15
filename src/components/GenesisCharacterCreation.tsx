import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useLifeStore } from '../stores/lifeStore';
import { LifeProfile } from '@shared/types';
import { 
  User, Calendar, MapPin, Star, Brain, TrendingUp, 
  Globe, GitBranch, Zap, Heart, Target, Sparkles 
} from 'lucide-react';

const GenesisCharacterCreation: React.FC = () => {
  const { createProfile, isLoading } = useLifeStore();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<Partial<Omit<LifeProfile, 'id' | 'createdAt'>>>({
    name: '',
    gender: 'male' as const,
    birthDate: '2000-01-01',
    birthLocation: '北京',
    initialConditions: {
      familyBackground: 'middle' as const,
      educationLevel: 'secondary' as const,
      healthStatus: 'good' as const,
    },
    personalityTraits: {
      riskTolerance: 50,
      ambition: 50,
      empathy: 50,
    },
  });

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }));
  };

  const handleNestedChange = (parent: string, field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [parent]: {
        ...(prev[parent as keyof typeof prev] as object),
        [field]: value
      }
    }));
  };

  const handleSubmit = async () => {
    if (!formData.name || !formData.birthDate || !formData.birthLocation) {
      return;
    }
    await createProfile(formData as Omit<LifeProfile, 'id' | 'createdAt'>);
  };

  // 量子粒子背景效果
  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    x: Math.random() * 100,
    y: Math.random() * 100,
    size: Math.random() * 4 + 1,
    delay: Math.random() * 2,
  }));

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-purple-950/10 to-slate-900 relative overflow-hidden">
      {/* 量子粒子背景 */}
      <div className="fixed inset-0 pointer-events-none">
        {particles.map((particle) => (
          <motion.div
            key={particle.id}
            className="absolute rounded-full bg-indigo-400/20"
            style={{
              left: `${particle.x}%`,
              top: `${particle.y}%`,
              width: particle.size,
              height: particle.size,
            }}
            animate={{
              y: [0, -20, 0],
              opacity: [0, 1, 0],
              scale: [0, 1, 0],
            }}
            transition={{
              duration: 3 + particle.delay,
              repeat: Infinity,
              ease: "easeInOut",
              delay: particle.delay,
            }}
          />
        ))}
      </div>

      {/* 渐变光晕 */}
      <div className="fixed inset-0 pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-indigo-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-80 h-80 bg-purple-500/10 rounded-full blur-3xl animate-pulse" style={{ animationDelay: '1s' }} />
      </div>

      <div className="relative z-10 max-w-6xl mx-auto px-4 py-12">
        <div className="grid lg:grid-cols-3 gap-12">
          {/* 主要表单区域 */}
          <div className="lg:col-span-2">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="relative"
            >
              {/* 发光边框效果 */}
              <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 rounded-3xl blur-xl opacity-30" />
              
              <div className="relative bg-slate-900/60 backdrop-blur-2xl rounded-3xl border border-white/10 overflow-hidden">
                {/* 顶部装饰条 */}
                <div className="h-1 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500" />
                
                <div className="p-8 md:p-12">
                  {/* 头部区域 */}
                  <motion.header 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.2 }}
                    className="mb-12 text-center"
                  >
                    <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-indigo-400 text-xs font-black uppercase tracking-widest mb-6">
                      <Star className="w-3 h-3 fill-current animate-pulse" />
                      <span>GENESIS PROTOCOL</span>
                    </div>
                    
                    <h1 className="text-4xl md:text-6xl font-black text-white mb-4 bg-gradient-to-r from-white via-indigo-200 to-purple-200 bg-clip-text text-transparent">
                      量子意识初始化
                    </h1>
                    
                    <p className="text-slate-400 text-lg max-w-2xl mx-auto leading-relaxed">
                      在多维时空中编织你的初始参数，每一个选择都将开启无数平行宇宙的可能性
                    </p>
                  </motion.header>

                  {/* 步骤指示器 */}
                  <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    className="mb-12"
                  >
                    <div className="flex justify-center gap-4 relative">
                      {[1, 2, 3].map((s) => (
                        <div key={s} className="flex flex-col items-center">
                          <motion.div
                            className={`w-12 h-12 rounded-full flex items-center justify-center text-lg font-black border-2 transition-all ${
                              step >= s
                                ? 'bg-white text-slate-900 border-white shadow-lg'
                                : 'bg-slate-800/50 text-slate-500 border-slate-700'
                            }`}
                            animate={step === s ? { scale: [1, 1.1, 1] } : {}}
                            transition={{ duration: 0.5 }}
                          >
                            {s}
                          </motion.div>
                          <span className={`mt-2 text-xs font-bold uppercase tracking-widest ${
                            step >= s ? 'text-white' : 'text-slate-600'
                          }`}>
                            {s === 1 ? '身份锚定' : s === 2 ? '环境编码' : '量子特性'}
                          </span>
                        </div>
                      ))}
                      
                      {/* 连接线 */}
                      <div className="absolute top-6 left-1/4 right-1/4 h-0.5 bg-slate-700 -z-10">
                        <motion.div
                          className="h-full bg-gradient-to-r from-indigo-500 to-purple-500"
                          initial={{ width: '0%' }}
                          animate={{ width: `${(step - 1) * 50}%` }}
                          transition={{ duration: 0.5 }}
                        />
                      </div>
                    </div>
                  </motion.div>

                  {/* 表单内容 */}
                  <div className="min-h-[400px]">
                    <AnimatePresence mode="wait">
                      {step === 1 && (
                        <motion.div
                          key="step1"
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ duration: 0.3 }}
                          className="space-y-8"
                        >
                          <QuantumInputField
                            label="意识标识符"
                            icon={<User className="w-5 h-5" />}
                            value={formData.name || ''}
                            onChange={(v) => handleInputChange('name', v)}
                            placeholder="请输入你的姓名..."
                            gradient="from-indigo-500 to-purple-500"
                          />
                          
                          <div className="grid md:grid-cols-2 gap-6">
                            <QuantumSelectField
                              label="量子极性"
                              icon={<Zap className="w-5 h-5" />}
                              value={formData.gender || 'male'}
                              onChange={(v) => handleInputChange('gender', v)}
                              options={[
                                { value: 'male', label: '阳子态', desc: '积极进取' },
                                { value: 'female', label: '阴子态', desc: '内敛包容' }
                              ]}
                            />
                            
                            <QuantumInputField
                              label="诞生时刻"
                              icon={<Calendar className="w-5 h-5" />}
                              type="date"
                              value={formData.birthDate || ''}
                              onChange={(v) => handleInputChange('birthDate', v)}
                              gradient="from-sky-500 to-cyan-500"
                            />
                          </div>
                          
                          <QuantumInputField
                            label="初始坐标"
                            icon={<MapPin className="w-5 h-5" />}
                            value={formData.birthLocation || ''}
                            onChange={(v) => handleInputChange('birthLocation', v)}
                            placeholder="例如：新东京 / 虚拟空间"
                            gradient="from-emerald-500 to-teal-500"
                          />
                        </motion.div>
                      )}

                      {step === 2 && (
                        <motion.div
                          key="step2"
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ duration: 0.3 }}
                          className="space-y-8"
                        >
                          {[
                            { 
                              field: 'familyBackground', 
                              label: '量子纠缠源', 
                              desc: '初始社会环境将影响你的基础频率',
                              options: [
                                { value: 'poor', label: '简约态', desc: '磨砺意志' },
                                { value: 'middle', label: '平衡态', desc: '稳健发展' },
                                { value: 'wealthy', label: '丰裕态', desc: '资源优势' }
                              ]
                            },
                            { 
                              field: 'educationLevel', 
                              label: '认知基频', 
                              desc: '知识结构决定信息处理能力',
                              options: [
                                { value: 'none', label: '原始态', desc: '野性成长' },
                                { value: 'primary', label: '基础态', desc: '启蒙教育' },
                                { value: 'secondary', label: '通识态', desc: '全面发展' },
                                { value: 'college', label: '专精态', desc: '深度探索' }
                              ]
                            },
                            { 
                              field: 'healthStatus', 
                              label: '载体稳定性', 
                              desc: '物理载体的质量影响意识传输效率',
                              options: [
                                { value: 'poor', label: '脆弱态', desc: '敏感细腻' },
                                { value: 'average', label: '标准态', desc: '普通适应' },
                                { value: 'good', label: '坚韧态', desc: '高度适应' },
                                { value: 'excellent', label: '完美态', desc: '极致潜能' }
                              ]
                            }
                          ].map((config) => (
                            <QuantumChoiceGrid
                              key={config.field}
                              label={config.label}
                              description={config.desc}
                              value={formData.initialConditions?.[config.field as keyof typeof formData.initialConditions]}
                              onChange={(v) => handleNestedChange('initialConditions', config.field, v)}
                              options={config.options}
                            />
                          ))}
                        </motion.div>
                      )}

                      {step === 3 && (
                        <motion.div
                          key="step3"
                          initial={{ opacity: 0, x: 20 }}
                          animate={{ opacity: 1, x: 0 }}
                          exit={{ opacity: 0, x: -20 }}
                          transition={{ duration: 0.3 }}
                          className="space-y-8"
                        >
                          {[
                            { 
                              key: 'riskTolerance', 
                              label: '不确定性容忍度', 
                              left: '保守共振', 
                              right: '冒险跃迁',
                              icon: <Heart className="w-5 h-5" />,
                              color: 'from-blue-500 to-indigo-500'
                            },
                            { 
                              key: 'ambition', 
                              label: '目标驱动力', 
                              left: '观察者态', 
                              right: '创造者态',
                              icon: <Target className="w-5 h-5" />,
                              color: 'from-purple-500 to-pink-500'
                            },
                            { 
                              key: 'empathy', 
                              label: '共情量子纠缠', 
                              left: '独立态', 
                              right: '连接态',
                              icon: <GitBranch className="w-5 h-5" />,
                              color: 'from-emerald-500 to-cyan-500'
                            }
                          ].map((trait) => (
                            <QuantumSlider
                              key={trait.key}
                              {...trait}
                              value={formData.personalityTraits?.[trait.key as keyof typeof formData.personalityTraits] || 50}
                              onChange={(v) => handleNestedChange('personalityTraits', trait.key, v)}
                            />
                          ))}
                        </motion.div>
                      )}
                    </AnimatePresence>
                  </div>

                  {/* 导航按钮 */}
                  <motion.div 
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: 0.5 }}
                    className="mt-12 flex justify-between"
                  >
                    <motion.button
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                      onClick={() => setStep(Math.max(1, step - 1))}
                      disabled={step === 1}
                      className="px-6 py-3 rounded-full border border-white/20 text-slate-400 hover:text-white hover:border-white/40 transition-all disabled:opacity-0"
                    >
                      ← 返回
                    </motion.button>
                    
                    {step < 3 ? (
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => setStep(step + 1)}
                        className="px-8 py-3 bg-gradient-to-r from-indigo-500 to-purple-500 text-white rounded-full font-bold hover:shadow-lg transition-all"
                      >
                        确认参数 →
                      </motion.button>
                    ) : (
                      <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={handleSubmit}
                        disabled={isLoading}
                        className="relative px-8 py-3 bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 text-white rounded-full font-bold overflow-hidden disabled:opacity-50"
                      >
                        <span className="relative z-10 flex items-center gap-2">
                          {isLoading && (
                            <motion.div
                              animate={{ rotate: 360 }}
                              transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                            >
                              <Sparkles className="w-4 h-4" />
                            </motion.div>
                          )}
                          {isLoading ? '量子坍缩中...' : '启动意识矩阵'}
                        </span>
                        
                        {/* 按钮发光效果 */}
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full animate-[shimmer_2s_infinite]" />
                      </motion.button>
                    )}
                  </motion.div>
                </div>
              </div>
            </motion.div>
          </div>

          {/* 信息侧边栏 */}
          <div className="space-y-6">
            <QuantumInfoCard 
              title="量子推演协议 v4.0" 
              icon={<Brain className="w-6 h-6" />}
              gradient="from-indigo-500 to-purple-500"
            >
              <p className="text-slate-300 text-sm leading-relaxed mb-4">
                基于贝叶斯网络的动态叙事系统，确保每一次选择都遵循因果律的同时保持情感张力。
              </p>
              
              <div className="space-y-4">
                {[
                  { icon: <TrendingUp className="w-4 h-4" />, title: '认知同步', desc: 'AI实时校准性格对事件的影响权重' },
                  { icon: <Globe className="w-4 h-4" />, title: '世界耦合', desc: '宏观事件作为背景噪声影响微观决策' },
                  { icon: <GitBranch className="w-4 h-4" />, title: '平行宇宙', desc: '量子并行系统允许窥视未选择的道路' }
                ].map((item, i) => (
                  <div key={i} className="flex gap-3">
                    <div className="mt-0.5 p-2 rounded-lg bg-white/5 text-indigo-400">
                      {item.icon}
                    </div>
                    <div>
                      <h4 className="font-bold text-white text-sm mb-1">{item.title}</h4>
                      <p className="text-slate-400 text-xs">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </QuantumInfoCard>

            <QuantumStatusCard />
          </div>
        </div>
      </div>
    </div>
  );
};

// 量子输入字段组件
const QuantumInputField: React.FC<{
  label: string;
  icon: React.ReactNode;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: string;
  gradient?: string;
}> = ({ label, icon, value, onChange, placeholder, type = 'text', gradient = 'from-indigo-500 to-purple-500' }) => (
  <div>
    <label className="block text-sm font-bold text-slate-300 mb-3 uppercase tracking-widest">
      {label}
    </label>
    <div className="relative group">
      <div className={`absolute -inset-0.5 bg-gradient-to-r ${gradient} rounded-xl blur opacity-0 group-focus-within:opacity-30 transition-opacity`} />
      <div className="relative">
        <input
          type={type}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full px-6 py-4 bg-slate-800/50 border border-slate-700 rounded-xl text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 transition-all"
        />
        <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-indigo-400 transition-colors">
          {icon}
        </div>
      </div>
    </div>
  </div>
);

// 量子选择字段组件
const QuantumSelectField: React.FC<{
  label: string;
  icon: React.ReactNode;
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string; desc: string }[];
}> = ({ label, icon, value, onChange, options }) => (
  <div>
    <label className="block text-sm font-bold text-slate-300 mb-3 uppercase tracking-widest">
      {label}
    </label>
    <div className="relative">
      <div className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500">
        {icon}
      </div>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-6 py-4 bg-slate-800/50 border border-slate-700 rounded-xl text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50 appearance-none pr-12"
      >
        {options.map(option => (
          <option key={option.value} value={option.value}>
            {option.label} - {option.desc}
          </option>
        ))}
      </select>
    </div>
  </div>
);

// 量子选择网格组件
const QuantumChoiceGrid: React.FC<{
  label: string;
  description: string;
  value: any;
  onChange: (value: any) => void;
  options: { value: any; label: string; desc: string }[];
}> = ({ label, description, value, onChange, options }) => (
  <div>
    <div className="mb-4">
      <h3 className="text-lg font-bold text-white mb-1">{label}</h3>
      <p className="text-slate-400 text-sm">{description}</p>
    </div>
    
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
      {options.map(option => (
        <motion.button
          key={option.value}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => onChange(option.value)}
          className={`p-4 rounded-xl border transition-all text-center ${
            value === option.value
              ? 'bg-white border-white shadow-lg text-slate-900'
              : 'bg-slate-800/50 border-slate-700 hover:border-slate-600 text-white'
          }`}
        >
          <div className="font-bold text-sm mb-1">{option.label}</div>
          <div className={`text-xs ${value === option.value ? 'text-slate-700' : 'text-slate-400'}`}>
            {option.desc}
          </div>
        </motion.button>
      ))}
    </div>
  </div>
);

// 量子滑块组件
const QuantumSlider: React.FC<{
  label: string;
  left: string;
  right: string;
  icon: React.ReactNode;
  color: string;
  value: number;
  onChange: (value: number) => void;
}> = ({ label, left, right, icon, color, value, onChange }) => (
  <div className="p-6 rounded-2xl bg-slate-800/30 border border-slate-700/50">
    <div className="flex items-center justify-between mb-4">
      <div className="flex items-center gap-2">
        <div className="p-2 rounded-lg bg-indigo-500/20 text-indigo-400">
          {icon}
        </div>
        <h3 className="font-bold text-white">{label}</h3>
      </div>
      <span className="text-2xl font-black bg-gradient-to-r from-indigo-400 to-purple-400 bg-clip-text text-transparent">
        {value}
      </span>
    </div>
    
    <div className="mb-3">
      <input
        type="range"
        min="0"
        max="100"
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className="w-full h-2 bg-slate-700 rounded-full appearance-none cursor-pointer slider"
      />
      <div className={`h-2 bg-gradient-to-r ${color} rounded-full mt-1 opacity-30`} 
           style={{ width: `${value}%` }} />
    </div>
    
    <div className="flex justify-between text-xs font-bold uppercase tracking-widest text-slate-500">
      <span>{left}</span>
      <span>{right}</span>
    </div>
  </div>
);

// 量子信息卡片组件
const QuantumInfoCard: React.FC<{
  title: string;
  icon: React.ReactNode;
  gradient: string;
  children: React.ReactNode;
}> = ({ title, icon, gradient, children }) => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="relative p-6 rounded-2xl bg-slate-900/40 backdrop-blur-xl border border-white/10"
  >
    <div className="absolute top-0 right-0 p-4 opacity-10">
      <Brain className="w-16 h-16" />
    </div>
    
    <div className="flex items-center gap-3 mb-4">
      <div className={`p-3 rounded-xl bg-gradient-to-r ${gradient} text-white`}>
        {icon}
      </div>
      <h3 className="text-xl font-bold text-white">{title}</h3>
    </div>
    
    {children}
  </motion.div>
);

// 量子状态卡片组件
const QuantumStatusCard: React.FC = () => (
  <motion.div
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: 0.2 }}
    className="p-6 rounded-2xl bg-gradient-to-br from-slate-800/40 to-slate-900/40 backdrop-blur-xl border border-white/5"
  >
    <p className="text-xs font-bold uppercase tracking-widest text-slate-500 mb-3">系统状态</p>
    
    <div className="flex items-center gap-3">
      <div className="relative">
        <div className="w-3 h-3 bg-emerald-500 rounded-full animate-pulse" />
        <div className="absolute inset-0 w-3 h-3 bg-emerald-500 rounded-full animate-ping opacity-30" />
      </div>
      <span className="text-sm font-medium text-slate-300">量子意识矩阵就绪</span>
    </div>
  </motion.div>
);

export default GenesisCharacterCreation;