import React from 'react'
import { storageService } from '../services/api'

function MistakeList() {
  const [mistakes, setMistakes] = React.useState([])
  const [filter, setFilter] = React.useState('all') // all, today, week

  React.useEffect(() => {
    loadMistakes()
  }, [])

  const loadMistakes = () => {
    const all = storageService.getAllMistakes()
    setMistakes(all)
  }

  const getSeverityColor = (severity) => {
    switch(severity) {
      case 'high': return 'bg-red-100 text-red-700'
      case 'medium': return 'bg-yellow-100 text-yellow-700'
      case 'low': return 'bg-green-100 text-green-700'
      default: return 'bg-gray-100 text-gray-700'
    }
  }

  const getSeverityText = (severity) => {
    switch(severity) {
      case 'high': return '🔴 高'
      case 'medium': return '🟡 中'
      case 'low': return '🟢 低'
      default: return '⚪ 未知'
    }
  }

  return (
    <div>
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold">📚 我的错题本</h2>
        <div className="flex gap-2">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg ${filter === 'all' ? 'bg-indigo-100 text-indigo-600' : 'bg-white'}`}
          >
            全部({mistakes.length})
          </button>
          <button
            onClick={() => setFilter('today')}
            className={`px-4 py-2 rounded-lg ${filter === 'today' ? 'bg-indigo-100 text-indigo-600' : 'bg-white'}`}
          >
            今日(0)
          </button>
        </div>
      </div>

      {mistakes.length === 0 ? (
        <div className="bg-white rounded-xl p-12 shadow-sm text-center">
          <div className="text-6xl mb-4">📚</div>
          <h3 className="text-xl font-bold mb-2">还没有错题记录</h3>
          <p className="text-gray-600 mb-6">开始录入你的第一道错题吧！</p>
          <button className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
            去录入错题
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {mistakes.map((mistake) => (
            <div key={mistake.id} className="bg-white rounded-xl p-6 shadow-sm">
              {/* 标题行 */}
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm text-gray-500">
                  【{mistake.subject}】{mistake.grade} • {new Date(mistake.createdAt).toLocaleDateString()}
                </span>
                {mistake.analysis && (
                  <span className={`px-3 py-1 rounded-full text-sm font-medium ${getSeverityColor(mistake.analysis.dimensions[0]?.severity)}`}>
                    {mistake.analysis.error_type}
                  </span>
                )}
              </div>

              {/* 题目预览 */}
              <div className="bg-gray-50 rounded-lg p-4 mb-3">
                <p className="text-gray-800 line-clamp-2">{mistake.question}</p>
              </div>

              {/* 错因标签 */}
              {mistake.analysis && (
                <div className="flex items-center gap-2 mb-3">
                  {mistake.analysis.dimensions.slice(0, 2).map((dim, idx) => (
                    <span key={idx} className="text-sm px-3 py-1 bg-gray-100 rounded-full">
                      {dim.dimension}: {getSeverityText(dim.severity)}
                    </span>
                  ))}
                </div>
              )}

              {/* 操作按钮 */}
              <div className="flex items-center justify-between">
                <div className="flex gap-2">
                  <button className="text-sm text-gray-600 hover:text-indigo-600">
                    💬 笔记
                  </button>
                  <button className="text-sm text-gray-600 hover:text-indigo-600">
                    🔗 同类题
                  </button>
                </div>
                <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition">
                  开始复习
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default MistakeList
