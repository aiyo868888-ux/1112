import React, { useState } from 'react'
import CapturePage from './components/CapturePage'
import MistakeList from './components/MistakeList'

function App() {
  const [currentPage, setCurrentPage] = useState('home')
  const [currentMistake, setCurrentMistake] = useState(null)

  const handleAnalysisComplete = (mistake) => {
    setCurrentMistake(mistake)
    setCurrentPage('list')
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航 */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <h1 className="text-xl font-bold text-indigo-600">
              🎯 K12智能错题本 <span className="text-xs text-gray-400 ml-2">POC v0.1</span>
            </h1>
            <div className="flex gap-4">
              <button
                onClick={() => setCurrentPage('home')}
                className={`px-4 py-2 rounded-lg ${currentPage === 'home' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-600'}`}
              >
                首页
              </button>
              <button
                onClick={() => setCurrentPage('capture')}
                className={`px-4 py-2 rounded-lg ${currentPage === 'capture' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-600'}`}
              >
                录入错题
              </button>
              <button
                onClick={() => setCurrentPage('list')}
                className={`px-4 py-2 rounded-lg ${currentPage === 'list' ? 'bg-indigo-100 text-indigo-600' : 'text-gray-600'}`}
              >
                错题本
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* 主内容区 */}
      <main className="max-w-7xl mx-auto px-4 py-8">
        {currentPage === 'home' && (
          <div className="text-center py-16">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">
              欢迎使用K12智能错题本
            </h2>
            <p className="text-gray-600 mb-8">
              拍照识别 → AI错因分析 → 智能复习推荐
            </p>
            <button
              onClick={() => setCurrentPage('capture')}
              className="px-8 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            >
              开始录入错题
            </button>

            <div className="mt-16 grid grid-cols-1 md:grid-cols-3 gap-8">
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <div className="text-4xl mb-4">📸</div>
                <h3 className="font-bold mb-2">智能识别</h3>
                <p className="text-sm text-gray-600">OCR识别题目，支持数学公式</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <div className="text-4xl mb-4">🧠</div>
                <h3 className="font-bold mb-2">AI诊断</h3>
                <p className="text-sm text-gray-600">三维分析错因，定位知识漏洞</p>
              </div>
              <div className="bg-white p-6 rounded-xl shadow-sm">
                <div className="text-4xl mb-4">📚</div>
                <h3 className="font-bold mb-2">智能复习</h3>
                <p className="text-sm text-gray-600">基于遗忘曲线的个性化复习</p>
              </div>
            </div>
          </div>
        )}

        {currentPage === 'capture' && (
          <CapturePage onAnalysisComplete={handleAnalysisComplete} />
        )}

        {currentPage === 'list' && <MistakeList />}
      </main>

      {/* 状态栏 */}
      <div className="fixed bottom-0 left-0 right-0 bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 py-2">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-600">📊 已录入错题: <strong>0</strong> 道</span>
            <span className="text-gray-600">🎯 今日复习: <strong>0</strong> 道</span>
            <span className="text-gray-400">POC验证版本</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
