import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Rule, RuleCategory } from '@shared/types';
import { Plus, Edit, Trash2, Save, X, Eye, EyeOff, Filter, Search, Copy, Download, Upload } from 'lucide-react';

interface CustomRuleEditorProps {
  onRulesChange?: (rules: Rule[]) => void;
}

const CustomRuleEditor: React.FC<CustomRuleEditorProps> = ({ onRulesChange }) => {
  const [rules, setRules] = useState<Rule[]>([]);
  const [categories, setCategories] = useState<RuleCategory[]>([]);
  const [editingRule, setEditingRule] = useState<Rule | null>(null);
  const [isCreating, setIsCreating] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [showAdvanced, setShowAdvanced] = useState(false);

  // 初始化默认规则和分类
  useEffect(() => {
    initializeDefaultRules();
  }, []);

  const initializeDefaultRules = () => {
    // 默认规则分类
    const defaultCategories: RuleCategory[] = [
      { id: 'health', name: '健康系统', description: '身体健康相关规则' },
      { id: 'career', name: '职业发展', description: '工作和事业发展规则' },
      { id: 'relationship', name: '人际关系', description: '社交和感情关系规则' },
      { id: 'personal', name: '个人成长', description: '自我提升和学习规则' },
      { id: 'finance', name: '财务管理', description: '金钱和投资相关规则' }
    ];

    // 默认规则模板
    const defaultRules: Rule[] = [
      {
        id: 'custom-1',
        name: '早睡早起',
        description: '晚上11点前睡觉，早上7点起床',
        category: 'health',
        condition: {
          type: 'time',
          operator: 'between',
          value: ['23:00', '07:00']
        },
        effect: {
          health: 2,
          energy: 1,
          productivity: 1
        },
        priority: 1,
        enabled: true,
        createdAt: new Date().toISOString()
      },
      {
        id: 'custom-2',
        name: '每日学习',
        description: '每天至少学习1小时新知识',
        category: 'personal',
        condition: {
          type: 'daily',
          operator: 'gte',
          value: 1
        },
        effect: {
          intelligence: 1,
          skills: 1,
          satisfaction: 0.5
        },
        priority: 2,
        enabled: true,
        createdAt: new Date().toISOString()
      }
    ];

    setCategories(defaultCategories);
    setRules(defaultRules);
  };

  // 过滤规则
  const filteredRules = rules.filter(rule => {
    const matchesSearch = rule.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         rule.description.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || rule.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  // 处理规则创建/编辑
  const handleSaveRule = (ruleData: Omit<Rule, 'id' | 'createdAt'>) => {
    if (editingRule) {
      // 更新现有规则
      const updatedRules = rules.map(rule => 
        rule.id === editingRule.id 
          ? { ...rule, ...ruleData, updatedAt: new Date().toISOString() }
          : rule
      );
      setRules(updatedRules);
      setEditingRule(null);
    } else {
      // 创建新规则
      const newRule: Rule = {
        ...ruleData,
        id: `custom-${Date.now()}`,
        createdAt: new Date().toISOString()
      };
      setRules([...rules, newRule]);
      setIsCreating(false);
    }
    
    if (onRulesChange) {
      onRulesChange(rules);
    }
  };

  const handleDeleteRule = (ruleId: string) => {
    setRules(rules.filter(rule => rule.id !== ruleId));
    if (editingRule?.id === ruleId) {
      setEditingRule(null);
    }
  };

  const handleToggleRule = (ruleId: string) => {
    setRules(rules.map(rule => 
      rule.id === ruleId 
        ? { ...rule, enabled: !rule.enabled, updatedAt: new Date().toISOString() }
        : rule
    ));
  };

  return (
    <div className="rounded-2xl bg-white/5 backdrop-blur-xl border border-white/10 overflow-hidden">
      {/* 头部控制面板 */}
      <div className="p-6 border-b border-white/10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <h2 className="text-2xl font-bold text-white flex items-center gap-2">
            <Edit className="w-6 h-6" />
            自定义规则编辑器
          </h2>
          
          <div className="flex flex-wrap gap-3">
            {/* 搜索框 */}
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-500" />
              <input
                type="text"
                placeholder="搜索规则..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 pr-4 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
              />
            </div>

            {/* 分类筛选 */}
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white"
            >
              <option value="all">全部分类</option>
              {categories.map(category => (
                <option key={category.id} value={category.id}>
                  {category.name}
                </option>
              ))}
            </select>

            {/* 创建按钮 */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => {
                setEditingRule(null);
                setIsCreating(true);
              }}
              className="flex items-center gap-2 px-4 py-2 bg-indigo-500/20 border border-indigo-500/30 text-indigo-300 rounded-lg hover:bg-indigo-500/30 transition-all"
            >
              <Plus className="w-4 h-4" />
              新建规则
            </motion.button>
          </div>
        </div>
      </div>

      {/* 主要内容区域 */}
      <div className="p-6">
        {/* 规则列表 */}
        <div className="space-y-4">
          {filteredRules.length === 0 ? (
            <div className="text-center py-12">
              <div className="w-16 h-16 mx-auto mb-4 bg-slate-800/50 rounded-full flex items-center justify-center">
                <Filter className="w-8 h-8 text-slate-600" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">未找到匹配规则</h3>
              <p className="text-slate-400">
                {searchTerm ? '尝试调整搜索条件' : '创建你的第一条自定义规则'}
              </p>
            </div>
          ) : (
            filteredRules.map((rule) => (
              <RuleCard
                key={rule.id}
                rule={rule}
                onEdit={() => setEditingRule(rule)}
                onDelete={() => handleDeleteRule(rule.id)}
                onToggle={() => handleToggleRule(rule.id)}
                getCategoryName={(categoryId) => 
                  categories.find(c => c.id === categoryId)?.name || categoryId
                }
              />
            ))
          )}
        </div>

        {/* 创建/编辑模态框 */}
        <AnimatePresence>
          {(isCreating || editingRule) && (
            <RuleModal
              rule={editingRule}
              categories={categories}
              onSave={handleSaveRule}
              onCancel={() => {
                setIsCreating(false);
                setEditingRule(null);
              }}
              showAdvanced={showAdvanced}
              onToggleAdvanced={() => setShowAdvanced(!showAdvanced)}
            />
          )}
        </AnimatePresence>
      </div>
    </div>
  );
};

// 规则卡片组件
const RuleCard: React.FC<{
  rule: Rule;
  onEdit: () => void;
  onDelete: () => void;
  onToggle: () => void;
  getCategoryName: (categoryId: string) => string;
}> = ({ rule, onEdit, onDelete, onToggle, getCategoryName }) => (
  <motion.div
    layout
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    className="p-4 rounded-xl bg-white/5 border border-white/10 hover:bg-white/8 transition-all"
  >
    <div className="flex items-start justify-between">
      <div className="flex-1">
        <div className="flex items-center gap-3 mb-2">
          <h3 className="font-bold text-white">{rule.name}</h3>
          <span className={`px-2 py-1 text-xs rounded-full ${
            rule.enabled 
              ? 'bg-green-500/20 text-green-400' 
              : 'bg-red-500/20 text-red-400'
          }`}>
            {rule.enabled ? '启用' : '禁用'}
          </span>
          <span className="px-2 py-1 bg-white/10 text-slate-300 text-xs rounded-full">
            {getCategoryName(rule.category)}
          </span>
        </div>
        
        <p className="text-slate-300 text-sm mb-3">{rule.description}</p>
        
        {/* 效果预览 */}
        <div className="flex flex-wrap gap-2">
          {Object.entries(rule.effect).map(([key, value]) => (
            <div key={key} className="flex items-center gap-1">
              <div className={`w-2 h-2 rounded-full ${
                value > 0 ? 'bg-green-400' : value < 0 ? 'bg-red-400' : 'bg-slate-500'
              }`} />
              <span className="text-xs text-slate-400 capitalize">{key}</span>
              <span className={`text-xs font-bold ${
                value > 0 ? 'text-green-400' : value < 0 ? 'text-red-400' : 'text-slate-400'
              }`}>
                {value > 0 ? '+' : ''}{value}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 操作按钮 */}
      <div className="flex items-center gap-2 ml-4">
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onToggle}
          className={`p-2 rounded-lg transition-all ${
            rule.enabled 
              ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30' 
              : 'bg-green-500/20 text-green-400 hover:bg-green-500/30'
          }`}
        >
          {rule.enabled ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
        </motion.button>
        
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onEdit}
          className="p-2 rounded-lg bg-white/10 text-slate-300 hover:bg-white/20 transition-all"
        >
          <Edit className="w-4 h-4" />
        </motion.button>
        
        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={onDelete}
          className="p-2 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 transition-all"
        >
          <Trash2 className="w-4 h-4" />
        </motion.button>
      </div>
    </div>
  </motion.div>
);

// 规则编辑模态框
const RuleModal: React.FC<{
  rule: Rule | null;
  categories: RuleCategory[];
  onSave: (ruleData: Omit<Rule, 'id' | 'createdAt'>) => void;
  onCancel: () => void;
  showAdvanced: boolean;
  onToggleAdvanced: () => void;
}> = ({ rule, categories, onSave, onCancel, showAdvanced, onToggleAdvanced }) => {
  const [formData, setFormData] = useState({
    name: rule?.name || '',
    description: rule?.description || '',
    category: rule?.category || categories[0]?.id || '',
    conditionType: rule?.condition?.type || 'daily',
    conditionOperator: rule?.condition?.operator || 'gte',
    conditionValue: rule?.condition?.value || '',
    effects: rule?.effect ? Object.entries(rule.effect).map(([key, value]) => ({ key, value })) : 
             [{ key: 'health', value: 1 }],
    priority: rule?.priority || 1,
    enabled: rule?.enabled ?? true
  });

  const handleSubmit = () => {
    const ruleData = {
      name: formData.name,
      description: formData.description,
      category: formData.category,
      condition: {
        type: formData.conditionType as any,
        operator: formData.conditionOperator as any,
        value: formData.conditionValue
      },
      effect: formData.effects.reduce((acc, eff) => {
        if (eff.key && eff.value !== '') {
          acc[eff.key] = Number(eff.value) || 0;
        }
        return acc;
      }, {} as Record<string, number>),
      priority: formData.priority,
      enabled: formData.enabled
    };
    
    onSave(ruleData);
  };

  const addEffect = () => {
    setFormData({
      ...formData,
      effects: [...formData.effects, { key: 'health', value: 1 }]
    });
  };

  const updateEffect = (index: number, field: 'key' | 'value', value: string) => {
    const newEffects = [...formData.effects];
    newEffects[index] = { ...newEffects[index], [field]: value };
    setFormData({ ...formData, effects: newEffects });
  };

  const removeEffect = (index: number) => {
    if (formData.effects.length > 1) {
      setFormData({
        ...formData,
        effects: formData.effects.filter((_, i) => i !== index)
      });
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center z-50 p-4"
      onClick={onCancel}
    >
      <motion.div
        initial={{ scale: 0.9, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        exit={{ scale: 0.9, opacity: 0 }}
        className="bg-slate-900 rounded-2xl border border-white/10 w-full max-w-2xl max-h-[90vh] overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* 头部 */}
        <div className="p-6 border-b border-white/10">
          <div className="flex items-center justify-between">
            <h3 className="text-xl font-bold text-white">
              {rule ? '编辑规则' : '创建新规则'}
            </h3>
            <button
              onClick={onCancel}
              className="p-2 rounded-lg hover:bg-white/10 transition-colors"
            >
              <X className="w-5 h-5 text-slate-400" />
            </button>
          </div>
        </div>

        {/* 表单内容 */}
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-140px)]">
          <div className="space-y-6">
            {/* 基本信息 */}
            <div>
              <h4 className="font-bold text-white mb-3">基本信息</h4>
              <div className="space-y-4">
                <InputField
                  label="规则名称"
                  value={formData.name}
                  onChange={(v) => setFormData({ ...formData, name: v })}
                  placeholder="例如：每日锻炼"
                />
                <TextAreaField
                  label="规则描述"
                  value={formData.description}
                  onChange={(v) => setFormData({ ...formData, description: v })}
                  placeholder="详细描述这条规则的作用和意义"
                />
                <SelectField
                  label="规则分类"
                  value={formData.category}
                  onChange={(v) => setFormData({ ...formData, category: v })}
                  options={categories.map(cat => ({ value: cat.id, label: cat.name }))}
                />
              </div>
            </div>

            {/* 条件设置 */}
            <div>
              <h4 className="font-bold text-white mb-3">触发条件</h4>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <SelectField
                  label="条件类型"
                  value={formData.conditionType}
                  onChange={(v) => setFormData({ ...formData, conditionType: v })}
                  options={[
                    { value: 'daily', label: '每日' },
                    { value: 'weekly', label: '每周' },
                    { value: 'monthly', label: '每月' },
                    { value: 'time', label: '时间点' }
                  ]}
                />
                <SelectField
                  label="比较运算符"
                  value={formData.conditionOperator}
                  onChange={(v) => setFormData({ ...formData, conditionOperator: v })}
                  options={[
                    { value: 'eq', label: '等于' },
                    { value: 'neq', label: '不等于' },
                    { value: 'gt', label: '大于' },
                    { value: 'gte', label: '大于等于' },
                    { value: 'lt', label: '小于' },
                    { value: 'lte', label: '小于等于' }
                  ]}
                />
                <InputField
                  label="条件值"
                  value={formData.conditionValue.toString()}
                  onChange={(v) => setFormData({ ...formData, conditionValue: v })}
                  placeholder="例如：1（小时）"
                />
              </div>
            </div>

            {/* 效果设置 */}
            <div>
              <div className="flex items-center justify-between mb-3">
                <h4 className="font-bold text-white">效果设置</h4>
                <button
                  onClick={addEffect}
                  className="flex items-center gap-1 px-3 py-1 bg-indigo-500/20 text-indigo-300 rounded-lg hover:bg-indigo-500/30 transition-colors"
                >
                  <Plus className="w-4 h-4" />
                  添加效果
                </button>
              </div>
              
              <div className="space-y-3">
                {formData.effects.map((effect, index) => (
                  <div key={index} className="flex items-end gap-3">
                    <SelectField
                      label="维度"
                      value={effect.key}
                      onChange={(v) => updateEffect(index, 'key', v)}
                      options={[
                        { value: 'health', label: '健康' },
                        { value: 'intelligence', label: '智力' },
                        { value: 'social', label: '社交' },
                        { value: 'achievement', label: '成就' },
                        { value: 'happiness', label: '幸福' },
                        { value: 'energy', label: '精力' },
                        { value: 'skills', label: '技能' }
                      ]}
                      className="flex-1"
                    />
                    <InputField
                      label="数值"
                      type="number"
                      value={effect.value.toString()}
                      onChange={(v) => updateEffect(index, 'value', v)}
                      placeholder="例如：2"
                      className="flex-1"
                    />
                    {formData.effects.length > 1 && (
                      <button
                        onClick={() => removeEffect(index)}
                        className="p-2 bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-colors"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </div>

            {/* 高级设置 */}
            <div>
              <button
                onClick={onToggleAdvanced}
                className="flex items-center gap-2 text-indigo-400 hover:text-indigo-300 transition-colors"
              >
                <span>{showAdvanced ? '收起' : '展开'}高级设置</span>
                <motion.div
                  animate={{ rotate: showAdvanced ? 180 : 0 }}
                  className="w-4 h-4"
                >
                  <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </motion.div>
              </button>

              <AnimatePresence>
                {showAdvanced && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="mt-4 space-y-4"
                  >
                    <InputField
                      label="优先级 (1-10)"
                      type="number"
                      min="1"
                      max="10"
                      value={formData.priority.toString()}
                      onChange={(v) => setFormData({ ...formData, priority: parseInt(v) || 1 })}
                    />
                    <div className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        id="enabled"
                        checked={formData.enabled}
                        onChange={(e) => setFormData({ ...formData, enabled: e.target.checked })}
                        className="w-4 h-4 text-indigo-500 bg-slate-800 border-slate-700 rounded focus:ring-indigo-500"
                      />
                      <label htmlFor="enabled" className="text-slate-300">
                        启用此规则
                      </label>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>

        {/* 底部按钮 */}
        <div className="p-6 border-t border-white/10 flex justify-end gap-3">
          <button
            onClick={onCancel}
            className="px-4 py-2 bg-white/10 text-slate-300 rounded-lg hover:bg-white/20 transition-colors"
          >
            取消
          </button>
          <button
            onClick={handleSubmit}
            disabled={!formData.name || !formData.description}
            className="px-4 py-2 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Save className="w-4 h-4 inline mr-2" />
            保存规则
          </button>
        </div>
      </motion.div>
    </motion.div>
  );
};

// 输入字段组件
const InputField: React.FC<{
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  type?: string;
  min?: string;
  max?: string;
  className?: string;
}> = ({ label, value, onChange, placeholder, type = 'text', min, max, className = '' }) => (
  <div className={className}>
    <label className="block text-sm font-medium text-slate-300 mb-2">{label}</label>
    <input
      type={type}
      min={min}
      max={max}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
    />
  </div>
);

// 文本域组件
const TextAreaField: React.FC<{
  label: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}> = ({ label, value, onChange, placeholder }) => (
  <div>
    <label className="block text-sm font-medium text-slate-300 mb-2">{label}</label>
    <textarea
      value={value}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      rows={3}
      className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/50 resize-none"
    />
  </div>
);

// 选择框组件
const SelectField: React.FC<{
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: { value: string; label: string }[];
  className?: string;
}> = ({ label, value, onChange, options, className = '' }) => (
  <div className={className}>
    <label className="block text-sm font-medium text-slate-300 mb-2">{label}</label>
    <select
      value={value}
      onChange={(e) => onChange(e.target.value)}
      className="w-full px-3 py-2 bg-white/5 border border-white/10 rounded-lg text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/50"
    >
      {options.map(option => (
        <option key={option.value} value={option.value}>
          {option.label}
        </option>
      ))}
    </select>
  </div>
);

export default CustomRuleEditor;