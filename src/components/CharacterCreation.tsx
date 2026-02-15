import React, { useState } from 'react'
import { useLifeStore } from '../stores/lifeStore'
import { LifeProfile } from '@shared/types'
import { User, Calendar, MapPin, Star, Brain, TrendingUp, Globe, GitBranch } from 'lucide-react'

const CharacterCreation: React.FC = () => {
  const { createProfile, isLoading } = useLifeStore()
  const [step, setStep] = useState(1)
  
  // 表单数据
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
  })

  const handleInputChange = (field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }))
  }

  const handleNestedChange = (parent: string, field: string, value: any) => {
    setFormData(prev => ({
      ...prev,
      [parent]: {
        ...(prev[parent as keyof typeof prev] as object),
        [field]: value
      }
    }))
  }

  const handleSubmit = async () => {
    if (!formData.name || !formData.birthDate || !formData.birthLocation) {
      alert('请填写完整信息')
      return
    }
    
    await createProfile(formData as Omit<LifeProfile, 'id' | 'createdAt'>)
  }

  return (
    <div className="max-w-7xl mx-auto py-8 sm:py-16 animate-fade-in px-4">
      <div className="grid gap-8 lg:gap-12 lg:grid-cols-[1fr_380px]">
        {/* Main Form Card */}
        <div className="relative group/main">
          <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 via-sky-500 to-purple-500 rounded-[42px] blur-2xl opacity-20 group-hover/main:opacity-30 transition-opacity duration-1000" />
          
          <div className="relative card-primary rounded-[40px] overflow-hidden shadow-[0_32px_80px_-20px_rgba(0,0,0,0.6)]">
            <div className="h-2 bg-gradient-to-r from-indigo-500 via-sky-500 to-emerald-500" />
            
            <div className="p-8 sm:p-12">
              <header className="mb-12 text-center lg:text-left space-y-5">
                <div className="inline-flex items-center space-x-3 px-4 py-2 rounded-full bg-white/5 border border-white/10 text-indigo-400 text-[10px] font-black uppercase tracking-[0.4em] shadow-inner">
                  <Star size={14} className="fill-current animate-pulse" />
                  <span>Genesis Initialization</span>
                </div>
                <div className="space-y-4">
                  <h1 className="text-5xl sm:text-7xl font-black text-white tracking-tighter leading-none premium-gradient-text high-contrast-text">
                    重塑您的命运
                  </h1>
                  <p className="text-slate-400 text-xl leading-relaxed max-w-2xl font-medium">
                    基于混沌理论与生物遗传算法。您的初始参数将编织出一条跨越时空的因果链条。
                  </p>
                </div>
              </header>

              {/* Stepper */}
              <div className="mb-16 relative">
                <div className="flex justify-between relative z-10 px-2 sm:px-10">
                  {[1, 2, 3].map((s) => (
                    <div key={s} className="flex flex-col items-center group/step">
                      <div className={`w-14 h-14 rounded-[20px] flex items-center justify-center text-xl font-black transition-all duration-700 border-2 ${
                        step >= s 
                          ? 'bg-white text-slate-950 border-white shadow-[0_0_30px_rgba(255,255,255,0.4)] scale-110' 
                          : 'bg-slate-900/50 text-slate-600 border-white/10'
                      }`}>
                        {s}
                      </div>
                      <span className={`mt-4 text-[10px] font-black tracking-[0.3em] uppercase transition-colors duration-500 ${step >= s ? 'text-white' : 'text-slate-600'}`}>
                        {s === 1 ? '核心' : s === 2 ? '环境' : '根性'}
                      </span>
                    </div>
                  ))}
                </div>
                <div className="absolute top-7 left-10 right-10 h-[2px] bg-white/5 -z-0">
                  <div 
                    className="h-full bg-gradient-to-r from-indigo-500 via-sky-500 to-white transition-all duration-1000 ease-in-out shadow-[0_0_15px_rgba(99,102,241,0.5)]"
                    style={{ width: `${(step - 1) * 50}%` }}
                  />
                </div>
              </div>

              {/* Form Steps */}
              <div className="min-h-[400px] transition-all duration-500">
                {step === 1 && (
                  <div className="space-y-12 animate-slide-up">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                      <div className="space-y-4">
                        <label className="text-xs font-black text-slate-500 uppercase tracking-[0.3em] ml-2">角色真名</label>
                        <div className="relative group/input">
                          <input
                            type="text"
                            value={formData.name || ''}
                            onChange={(e) => handleInputChange('name', e.target.value)}
                            className="w-full px-8 py-5 rounded-[24px] bg-white/5 border border-white/10 text-white text-lg font-bold placeholder:text-slate-700 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 focus:border-indigo-500/50 transition-all"
                            placeholder="如：林深"
                          />
                          <User className="absolute right-6 top-1/2 -translate-y-1/2 text-slate-600 group-focus-within/input:text-indigo-400 transition-colors" size={20} />
                        </div>
                      </div>
                      <div className="space-y-4">
                        <label className="text-xs font-black text-slate-500 uppercase tracking-[0.3em] ml-2">生命极性</label>
                        <div className="flex p-2 rounded-[24px] bg-white/5 border border-white/10 shadow-inner">
                          <button 
                            onClick={() => handleInputChange('gender', 'male')}
                            className={`flex-1 py-4 rounded-[18px] text-sm font-black transition-all duration-500 ${formData.gender === 'male' ? 'bg-white text-slate-950 shadow-[0_10px_20px_rgba(255,255,255,0.2)] scale-105' : 'text-slate-500 hover:text-slate-300'}`}
                          >男性 MALE</button>
                          <button 
                            onClick={() => handleInputChange('gender', 'female')}
                            className={`flex-1 py-4 rounded-[18px] text-sm font-black transition-all duration-500 ${formData.gender === 'female' ? 'bg-white text-slate-950 shadow-[0_10px_20px_rgba(255,255,255,0.2)] scale-105' : 'text-slate-500 hover:text-slate-300'}`}
                          >女性 FEMALE</button>
                        </div>
                      </div>
                      <div className="space-y-4">
                        <label className="text-xs font-black text-slate-500 uppercase tracking-[0.3em] ml-2">降生时刻</label>
                        <div className="relative group/input">
                          <input
                            type="date"
                            value={formData.birthDate || ''}
                            onChange={(e) => handleInputChange('birthDate', e.target.value)}
                            className="w-full px-8 py-5 rounded-[24px] bg-white/5 border border-white/10 text-white font-bold focus:outline-none focus:ring-4 focus:ring-indigo-500/20 transition-all [color-scheme:dark]"
                          />
                          <Calendar className="absolute right-6 top-1/2 -translate-y-1/2 text-slate-600 group-focus-within/input:text-sky-400 transition-colors" size={20} />
                        </div>
                      </div>
                      <div className="space-y-4">
                        <label className="text-xs font-black text-slate-500 uppercase tracking-[0.3em] ml-2">初始坐标</label>
                        <div className="relative group/input">
                          <input
                            type="text"
                            value={formData.birthLocation || ''}
                            onChange={(e) => handleInputChange('birthLocation', e.target.value)}
                            className="w-full px-8 py-5 rounded-[24px] bg-white/5 border border-white/10 text-white text-lg font-bold placeholder:text-slate-700 focus:outline-none focus:ring-4 focus:ring-indigo-500/20 transition-all"
                            placeholder="例如：新东京 / 虚拟空间"
                          />
                          <MapPin className="absolute right-6 top-1/2 -translate-y-1/2 text-slate-600 group-focus-within/input:text-emerald-400 transition-colors" size={20} />
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {step === 2 && (
                  <div className="space-y-12 animate-slide-up">
                    <div className="grid gap-10">
                      {[
                        { label: '血脉起源', field: 'familyBackground', options: [{v:'poor', l:'清寒', d:'磨砺意志的开端'}, {v:'middle', l:'平稳', d:'均衡发展的路径'}, {v:'wealthy', l:'优渥', d:'资源充沛的起点'}] },
                        { label: '认知基座', field: 'educationLevel', options: [{v:'none', l:'自习', d:'野蛮生长'}, {v:'primary', l:'启蒙', d:'基础构建'}, {v:'secondary', l:'通识', d:'社会化完成'}, {v:'college', l:'精进', d:'专业领域探索'}] },
                        { label: '载体强度', field: 'healthStatus', options: [{v:'poor', l:'纤弱', d:'感官敏锐'}, {v:'average', l:'标准', d:'普适形态'}, {v:'good', l:'坚韧', d:'高度适应'}, {v:'excellent', l:'无暇', d:'完美潜能'}] }
                      ].map((row) => (
                        <div key={row.field} className="space-y-6">
                          <label className="text-xs font-black text-slate-500 uppercase tracking-[0.3em] ml-2">{row.label}</label>
                          <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
                            {row.options.map(opt => (
                              <button
                                key={opt.v}
                                onClick={() => handleNestedChange('initialConditions', row.field, opt.v)}
                                className={`group/opt relative p-4 rounded-[24px] border transition-all duration-500 ${
                                  formData.initialConditions?.[row.field as keyof typeof formData.initialConditions] === opt.v
                                    ? 'bg-white border-white shadow-[0_20px_40px_rgba(255,255,255,0.15)] scale-105'
                                    : 'bg-white/5 border-white/5 hover:border-white/20'
                                }`}
                              >
                                <div className="space-y-1 text-center">
                                  <div className={`text-sm font-black transition-colors ${formData.initialConditions?.[row.field as keyof typeof formData.initialConditions] === opt.v ? 'text-slate-950' : 'text-white'}`}>
                                    {opt.l}
                                  </div>
                                  <div className={`text-[9px] font-bold opacity-50 ${formData.initialConditions?.[row.field as keyof typeof formData.initialConditions] === opt.v ? 'text-slate-800' : 'text-slate-400'}`}>
                                    {opt.d}
                                  </div>
                                </div>
                              </button>
                            ))}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {step === 3 && (
                  <div className="space-y-12 animate-slide-up">
                    <div className="grid gap-8">
                      {[
                        { key: 'riskTolerance', label: '风险映射', left: '防御型', right: '开拓型', color: 'from-blue-500 to-indigo-500' },
                        { key: 'ambition', label: '意志倾向', left: '观测者', right: '重塑者', color: 'from-purple-500 to-pink-500' },
                        { key: 'empathy', label: '感知模式', left: '绝对冷彻', right: '共鸣体', color: 'from-emerald-500 to-sky-500' },
                      ].map((trait) => (
                        <div key={trait.key} className="p-8 rounded-[32px] bg-white/5 border border-white/10 space-y-6 hover:bg-white/[0.08] transition-colors group/trait">
                          <div className="flex justify-between items-end">
                            <div className="space-y-1">
                              <label className="text-sm font-black text-white tracking-widest uppercase">{trait.label}</label>
                              <div className="text-[10px] font-bold text-slate-500 tracking-wider">Neural Pattern Mapping</div>
                            </div>
                            <span className="text-4xl font-black premium-gradient-text">
                              {formData.personalityTraits?.[trait.key as keyof typeof formData.personalityTraits] || 50}
                            </span>
                          </div>
                          <div className="relative py-4">
                            <input
                              type="range"
                              min="0"
                              max="100"
                              value={formData.personalityTraits?.[trait.key as keyof typeof formData.personalityTraits] || 50}
                              onChange={(e) => handleNestedChange('personalityTraits', trait.key, parseInt(e.target.value))}
                              className="w-full h-2 bg-slate-800 rounded-full appearance-none cursor-pointer accent-white relative z-10"
                            />
                            <div className={`absolute top-1/2 -translate-y-1/2 left-0 h-2 rounded-full opacity-30 blur-md transition-all duration-300 bg-gradient-to-r ${trait.color}`} 
                                 style={{ width: `${formData.personalityTraits?.[trait.key as keyof typeof formData.personalityTraits] || 50}%` }} />
                          </div>
                          <div className="flex justify-between text-[10px] font-black uppercase tracking-[0.3em] text-slate-600">
                            <span className="group-hover/trait:text-slate-400 transition-colors">{trait.left}</span>
                            <span className="group-hover/trait:text-slate-400 transition-colors">{trait.right}</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Navigation Buttons */}
              <div className="mt-20 flex flex-col sm:flex-row items-center justify-between gap-6">
                <button
                  onClick={() => setStep(Math.max(1, step - 1))}
                  disabled={step === 1}
                  className="w-full sm:w-auto px-12 py-5 rounded-[24px] font-black text-[10px] uppercase tracking-[0.4em] text-slate-500 hover:text-white disabled:opacity-0 transition-all border border-transparent hover:border-white/10"
                >
                  回溯上一层
                </button>
                
                {step < 3 ? (
                  <button
                    onClick={() => setStep(step + 1)}
                    className="w-full sm:w-auto px-16 py-6 rounded-[24px] bg-white text-slate-950 font-black text-xs uppercase tracking-[0.4em] shadow-[0_20px_40px_rgba(255,255,255,0.2)] hover:scale-105 active:scale-95 transition-all duration-500"
                  >
                    确立参数
                  </button>
                ) : (
                  <button
                    onClick={handleSubmit}
                    disabled={isLoading}
                    className="group/btn relative w-full sm:w-auto px-16 py-6 rounded-[24px] bg-gradient-to-r from-indigo-500 via-sky-500 to-purple-500 text-white font-black text-xs uppercase tracking-[0.4em] shadow-[0_20px_40px_rgba(99,102,241,0.3)] hover:scale-105 active:scale-95 disabled:opacity-50 transition-all duration-500 overflow-hidden"
                  >
                    <div className="relative z-10 flex items-center justify-center gap-3">
                      {isLoading && <div className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />}
                      <span>{isLoading ? '次元重组中...' : '启动坍缩演化'}</span>
                    </div>
                    <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover/btn:animate-[shimmer_2s_infinite]" />
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Sidebar Info */}
        <aside className="space-y-8">
          <div className="relative group/card overflow-hidden p-8 sm:p-10 rounded-[40px] card-primary shadow-2xl">
            <div className="absolute top-0 right-0 p-8 opacity-5 group-hover/card:opacity-10 transition-opacity">
              <Brain size={120} />
            </div>
            
            <h3 className="text-2xl font-black text-white mb-8 flex items-center tracking-tight">
              <div className="p-2 rounded-xl bg-indigo-500/20 text-indigo-400 mr-4">
                <TrendingUp size={24} />
              </div>
              推演协议 4.0
            </h3>
            
            <div className="space-y-8">
              <div className="space-y-3">
                <div className="text-[10px] font-black text-indigo-400 uppercase tracking-[0.3em]">Causality Engine</div>
                <p className="text-sm text-slate-400 leading-relaxed font-medium">
                  基于贝叶斯网络的动态叙事，确保每一个人生节点都具备逻辑一致性与情感张力。
                </p>
              </div>
              
              <div className="h-px bg-white/5" />
              
              <div className="space-y-6">
                {[
                  { icon: Brain, title: '认知同步', desc: 'AI 将实时校准您的性格特质对后续事件的权重影响。', color: 'text-purple-400' },
                  { icon: Globe, title: '世界耦合', desc: '宏观社会事件将作为背景噪声影响您的微观决策。', color: 'text-sky-400' },
                  { icon: GitBranch, title: '分叉预览', desc: '量子并行系统允许在某些节点窥视未曾选择的道路。', color: 'text-emerald-400' }
                ].map((item, i) => (
                  <div key={i} className="flex gap-5 group/item">
                    <div className={`mt-1 p-3 rounded-2xl bg-white/5 ${item.color} group-hover/item:bg-white/10 transition-colors shadow-inner`}>
                      <item.icon size={20}/>
                    </div>
                    <div className="space-y-1">
                      <h4 className="text-sm font-black text-white tracking-wide">{item.title}</h4>
                      <p className="text-xs text-slate-500 leading-relaxed font-medium">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="p-8 sm:p-10 rounded-[40px] card-tertiary relative overflow-hidden">
            <div className="absolute -bottom-4 -left-4 w-24 h-24 bg-indigo-500/10 blur-2xl rounded-full" />
            <div className="relative z-10 space-y-4">
              <p className="text-[10px] font-black uppercase tracking-[0.4em] text-slate-500">Node Status</p>
              <div className="flex items-center gap-3">
                <div className="flex h-2 w-2 relative">
                  <div className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></div>
                  <div className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></div>
                </div>
                <span className="text-xs font-black text-slate-300 tracking-widest">LOCAL ENCRYPTED STORAGE ACTIVE</span>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  )
}

export default CharacterCreation
