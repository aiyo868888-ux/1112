import React from 'react'

function AnalysisPage({ analysis, onEdit, onSave }) {
  if (!analysis) {
    return (
      <div className="bg-white rounded-xl p-12 shadow-sm text-center">
        <div className="text-6xl mb-4">🧠</div>
        <h3 className="text-xl font-bold mb-2">等待AI分析...</h3>
        <p className="text-gray-600">请先完成错题录入</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* 错误类型 */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center mb-3">
          <span className="text-2xl mr-2">🔴</span>
          <h3 className="font-bold">错误类型</h3>
        </div>
        <p className="text-lg font-semibold text-red-600">{analysis.error_type}</p>
      </div>

      {/* 知识点 */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center mb-3">
          <span className="text-2xl mr-2">📚</span>
          <h3 className="font-bold">知识点</h3>
        </div>
        <p className="text-lg">{analysis.knowledge_point}</p>
      </div>

      {/* 根本原因 */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center mb-3">
          <span className="text-2xl mr-2">🎯</span>
          <h3 className="font-bold">根本原因</h3>
        </div>
        <p className="text-gray-700">{analysis.root_cause}</p>
      </div>

      {/* 三维分析 */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <h3 className="font-bold mb-4">📊 三维分析</h3>
        <div className="space-y-3">
          {analysis.dimensions && analysis.dimensions.map((dim, idx) => (
            <div key={idx} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center">
                <span className="mr-2">
                  {dim.severity === 'high' && '🔴'}
                  {dim.severity === 'medium' && '🟡'}
                  {dim.severity === 'low' && '🟢'}
                </span>
                <span className="font-medium">{dim.dimension}</span>
              </div>
              <span className="text-sm text-gray-600">{dim.description}</span>
            </div>
          ))}
        </div>
      </div>

      {/* 改进建议 */}
      <div className="bg-white rounded-xl p-6 shadow-sm">
        <div className="flex items-center mb-3">
          <span className="text-2xl mr-2">💡</span>
          <h3 className="font-bold">改进建议</h3>
        </div>
        <ul className="space-y-2">
          {analysis.suggestions && analysis.suggestions.map((suggestion, idx) => (
            <li key={idx} className="flex items-start">
              <span className="text-indigo-600 mr-2">•</span>
              <span>{suggestion}</span>
            </li>
          ))}
        </ul>
      </div>

      {/* 操作按钮 */}
      <div className="flex gap-4">
        <button
          onClick={onEdit}
          className="flex-1 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
        >
          ← 返回修改
        </button>
        <button
          onClick={onSave}
          className="flex-1 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-bold"
        >
          ✅ 保存到错题本
        </button>
      </div>
    </div>
  )
}

export default AnalysisPage
