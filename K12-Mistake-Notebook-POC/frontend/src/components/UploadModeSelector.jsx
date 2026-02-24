import React from 'react'

/**
 * 上传模式选择组件
 * 参考小牛错题的设计，提供三种模式选择
 */
function UploadModeSelector({ onModeSelect, onCancel }) {
  const modes = [
    {
      id: 'single',
      title: '单题录入',
      icon: '📝',
      description: '录入一道错题',
      feature: '适合单独题目',
      color: 'bg-blue-500',
      bgColor: 'bg-blue-50',
      borderColor: 'border-blue-200'
    },
    {
      id: 'multi',
      title: '多题录入',
      icon: '📚',
      description: '一次录入多道题',
      feature: 'AI自动检测题目',
      color: 'bg-green-500',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200'
    },
    {
      id: 'crosspage',
      title: '跨页录入',
      icon: '📖',
      description: '题目跨页时使用',
      feature: '支持拼接多页',
      color: 'bg-purple-500',
      bgColor: 'bg-purple-50',
      borderColor: 'border-purple-200'
    }
  ]

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <div className="text-center mb-6">
        <h2 className="text-2xl font-bold mb-2">📸 选择录入模式</h2>
        <p className="text-gray-600">根据你的题目情况选择合适的录入方式</p>
      </div>

      {/* 模式选择卡片 */}
      <div className="grid grid-cols-1 gap-4 mb-6">
        {modes.map((mode) => (
          <button
            key={mode.id}
            onClick={() => onModeSelect(mode.id)}
            className={`
              ${mode.bgColor} ${mode.borderColor} border-2 rounded-xl p-6
              text-left transition-all duration-200
              hover:shadow-lg hover:scale-[1.02]
              active:scale-[0.98]
            `}
          >
            <div className="flex items-center">
              <div className={`${mode.color} text-white text-4xl rounded-lg p-3 mr-4`}>
                {mode.icon}
              </div>
              <div className="flex-1">
                <h3 className="text-xl font-bold mb-1">{mode.title}</h3>
                <p className="text-gray-600 text-sm mb-1">{mode.description}</p>
                <p className="text-gray-500 text-xs">
                  ✨ {mode.feature}
                </p>
              </div>
              <div className="text-gray-400">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                </svg>
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* 取消按钮 */}
      <div className="flex gap-3">
        <button
          onClick={onCancel}
          className="flex-1 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
        >
          取消
        </button>
      </div>

      {/* 使用提示 */}
      <div className="mt-6 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium mb-2 text-sm">💡 选择建议</h4>
        <ul className="text-xs text-gray-600 space-y-1">
          <li>• <strong>单题录入</strong>：只有一道错题时使用</li>
          <li>• <strong>多题录入</strong>：一页有多道题时使用（推荐）</li>
          <li>• <strong>跨页录入</strong>：题目横跨两页时使用</li>
        </ul>
      </div>
    </div>
  )
}

export default UploadModeSelector
