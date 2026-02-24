import React, { useState, useRef } from 'react'
import { ocrService, aiService, storageService } from '../services/api'
import QuestionSelector from './QuestionSelector'
import UploadModeSelector from './UploadModeSelector'

function CapturePage({ onAnalysisComplete }) {
  const [step, setStep] = useState('mode') // mode, upload, select, preview, analyzing, result
  const [uploadMode, setUploadMode] = useState('single') // single, multi, crosspage
  const [image, setImage] = useState(null)
  const [selectedQuestions, setSelectedQuestions] = useState([])
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0)
  const [ocrResult, setOcrResult] = useState('')
  const [wrongAnswer, setWrongAnswer] = useState('')
  const [correctAnswer, setCorrectAnswer] = useState('')
  const [subject, setSubject] = useState('数学')
  const [grade, setGrade] = useState('初二')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const fileInputRef = useRef(null)

  // 处理模式选择
  const handleModeSelect = (mode) => {
    setUploadMode(mode)
    setStep('upload')
    // 自动触发文件选择
    setTimeout(() => {
      fileInputRef.current?.click()
    }, 100)
  }

  // 处理文件上传
  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => {
        setImage(reader.result)

        // 根据模式决定下一步
        if (uploadMode === 'single') {
          // 单题模式：直接进入预览，跳过选择
          setSelectedQuestions([{
            id: 1,
            imageData: reader.result,
            rect: null
          }])
          setCurrentQuestionIndex(0)
          setStep('preview')
        } else {
          // 多题/跨页模式：进入选择阶段
          setStep('select')
        }
      }
      reader.readAsDataURL(file)
    }
  }

  // 返回模式选择
  const handleBackToMode = () => {
    setStep('mode')
    setImage(null)
    setSelectedQuestions([])
  }

  // 处理题目选择完成
  const handleQuestionsSelected = (questions) => {
    setSelectedQuestions(questions)
    setCurrentQuestionIndex(0)
    setStep('preview')
  }

  // 取消题目选择
  const handleCancelSelect = () => {
    setStep('upload')
  }

  // 切换到上一题
  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      // 保存当前题目的答案
      saveCurrentQuestionAnswers()
      setCurrentQuestionIndex(currentQuestionIndex - 1)
      loadQuestionAnswers(currentQuestionIndex - 1)
    }
  }

  // 切换到下一题
  const handleNextQuestion = () => {
    if (currentQuestionIndex < selectedQuestions.length - 1) {
      // 保存当前题目的答案
      saveCurrentQuestionAnswers()
      setCurrentQuestionIndex(currentQuestionIndex + 1)
      loadQuestionAnswers(currentQuestionIndex + 1)
    }
  }

  // 保存当前题目的答案（临时存储）
  const saveCurrentQuestionAnswers = () => {
    const updated = [...selectedQuestions]
    updated[currentQuestionIndex] = {
      ...updated[currentQuestionIndex],
      ocrResult,
      wrongAnswer,
      correctAnswer
    }
    setSelectedQuestions(updated)
  }

  // 加载指定题目的答案
  const loadQuestionAnswers = (index) => {
    const q = selectedQuestions[index]
    setOcrResult(q.ocrResult || '')
    setWrongAnswer(q.wrongAnswer || '')
    setCorrectAnswer(q.correctAnswer || '')
  }

  // OCR识别
  const handleOCR = async () => {
    if (!selectedQuestions[currentQuestionIndex]) return

    setLoading(true)
    try {
      // 使用当前题目区域的图片进行OCR识别
      const questionImageData = selectedQuestions[currentQuestionIndex].imageData
      const file = await dataURLtoFile(questionImageData, `question_${currentQuestionIndex + 1}.jpg`)
      const result = await ocrService.recognizeText(file)

      if (result.success) {
        setOcrResult(result.text)
      } else {
        alert('OCR识别失败: ' + result.error)
      }
    } catch (error) {
      console.error('OCR错误:', error)
      alert('OCR识别出错')
    } finally {
      setLoading(false)
    }
  }

  // AI分析
  const handleAnalyze = async () => {
    if (!ocrResult || !wrongAnswer) {
      alert('请完成题目内容和错误答案')
      return
    }

    setLoading(true)
    setStep('analyzing')

    try {
      const result = await aiService.analyzeMistake({
        question: ocrResult,
        wrong_answer: wrongAnswer,
        correct_answer: correctAnswer || '待分析',
        subject: subject,
        grade: grade
      })

      setAnalysisResult(result)
      setStep('result')
    } catch (error) {
      console.error('AI分析错误:', error)
      alert('AI分析失败')
      setStep('preview')
    } finally {
      setLoading(false)
    }
  }

  // 保存错题
  const handleSave = () => {
    const mistake = {
      image: selectedQuestions[currentQuestionIndex].imageData,
      question: ocrResult,
      wrongAnswer,
      correctAnswer,
      subject,
      grade,
      analysis: analysisResult,
      questionNumber: currentQuestionIndex + 1,
      totalQuestions: selectedQuestions.length
    }

    storageService.saveMistake(mistake)
    alert(`✅ 第${currentQuestionIndex + 1}题已保存到错题本！`)

    // 如果还有下一题，询问是否继续
    if (currentQuestionIndex < selectedQuestions.length - 1) {
      if (confirm(`还有${selectedQuestions.length - currentQuestionIndex - 1}道题未处理，是否继续？`)) {
        handleNextQuestion()
        setStep('preview')
      } else {
        onAnalysisComplete(mistake)
      }
    } else {
      alert('🎉 所有题目已处理完成！')
      onAnalysisComplete(mistake)
    }
  }

  // 辅助函数: base64转File
  const dataURLtoFile = async (dataurl, filename) => {
    const res = await fetch(dataurl)
    const blob = await res.blob()
    return new File([blob], filename, { type: 'image/jpeg' })
  }

  return (
    <div className="max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-6">
        📸 录入错题
        {selectedQuestions.length > 0 && (
          <span className="text-lg font-normal text-gray-600 ml-2">
            (第 {currentQuestionIndex + 1}/{selectedQuestions.length} 题)
          </span>
        )}
      </h2>

      {/* 模式选择 */}
      {step === 'mode' && (
        <UploadModeSelector
          onModeSelect={handleModeSelect}
          onCancel={() => onAnalysisComplete(null)}
        />
      )}

      {/* 上传区域 */}
      {step === 'upload' && (
        <div className="bg-white rounded-xl p-8 shadow-sm">
          <div className="mb-4 text-center">
            <p className="text-sm text-gray-500 mb-2">当前模式</p>
            <p className="font-bold text-lg">
              {uploadMode === 'single' && '📝 单题录入'}
              {uploadMode === 'multi' && '📚 多题录入（AI自动检测）'}
              {uploadMode === 'crosspage' && '📖 跨页录入'}
            </p>
          </div>

          <div
            onClick={() => fileInputRef.current?.click()}
            className="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center cursor-pointer hover:border-indigo-500 transition"
          >
            <div className="text-5xl mb-4">📷</div>
            <p className="text-gray-600 mb-2">点击拍照或上传图片</p>
            <p className="text-sm text-gray-400">
              {uploadMode === 'single' && '支持 JPG、PNG 格式'}
              {uploadMode === 'multi' && '支持 JPG、PNG 格式，AI将自动检测题目区域'}
              {uploadMode === 'crosspage' && '支持 JPG、PNG 格式，可上传多页'}
            </p>
          </div>

          <input
            ref={fileInputRef}
            type="file"
            accept="image/*"
            onChange={handleFileUpload}
            className="hidden"
          />

          <button
            onClick={handleBackToMode}
            className="mt-4 w-full py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
          >
            ← 返回选择模式
          </button>
        </div>
      )}

      {/* 题目区域选择 */}
      {step === 'select' && image && (
        <QuestionSelector
          image={image}
          onQuestionsSelected={handleQuestionsSelected}
          onCancel={handleBackToMode}
          uploadMode={uploadMode}
        />
      )}

      {/* 预览和编辑 */}
      {step === 'preview' && (
        <div className="space-y-6">
          {/* 题目导航 */}
          {selectedQuestions.length > 1 && (
            <div className="bg-white rounded-xl p-4 shadow-sm">
              <div className="flex items-center justify-between">
                <button
                  onClick={handlePreviousQuestion}
                  disabled={currentQuestionIndex === 0}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition disabled:opacity-50"
                >
                  ← 上一题
                </button>
                <div className="flex gap-2">
                  {selectedQuestions.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => {
                        saveCurrentQuestionAnswers()
                        setCurrentQuestionIndex(index)
                        loadQuestionAnswers(index)
                      }}
                      className={`w-8 h-8 rounded-lg font-medium transition ${
                        index === currentQuestionIndex
                          ? 'bg-indigo-600 text-white'
                          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                      }`}
                    >
                      {index + 1}
                    </button>
                  ))}
                </div>
                <button
                  onClick={handleNextQuestion}
                  disabled={currentQuestionIndex === selectedQuestions.length - 1}
                  className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition disabled:opacity-50"
                >
                  下一题 →
                </button>
              </div>
            </div>
          )}

          {/* 图片预览 */}
          <div className="bg-white rounded-xl p-4 shadow-sm">
            <img
              src={selectedQuestions[currentQuestionIndex]?.imageData || image}
              alt={`第${currentQuestionIndex + 1}题`}
              className="w-full rounded-lg"
            />
          </div>

          {/* OCR结果 */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="font-bold mb-3">📝 题目内容</h3>
            <textarea
              value={ocrResult}
              onChange={(e) => setOcrResult(e.target.value)}
              className="w-full h-32 p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500"
              placeholder="OCR识别结果，可手动编辑..."
            />
            <button
              onClick={handleOCR}
              disabled={loading}
              className="mt-3 w-full py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
            >
              {loading ? '识别中...' : '🔄 重新识别'}
            </button>
          </div>

          {/* 错误答案 */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="font-bold mb-3">❌ 我的错误答案</h3>
            <textarea
              value={wrongAnswer}
              onChange={(e) => setWrongAnswer(e.target.value)}
              className="w-full h-24 p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500"
              placeholder="填写你的错误答案..."
            />
          </div>

          {/* 正确答案 */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="font-bold mb-3">✅ 正确答案 (可选)</h3>
            <textarea
              value={correctAnswer}
              onChange={(e) => setCorrectAnswer(e.target.value)}
              className="w-full h-24 p-3 border rounded-lg focus:ring-2 focus:ring-indigo-500"
              placeholder="填写正确答案，AI会辅助分析..."
            />
          </div>

          {/* 科目和年级 */}
          <div className="grid grid-cols-2 gap-4">
            <div className="bg-white rounded-xl p-4 shadow-sm">
              <label className="block text-sm font-medium mb-2">科目</label>
              <select
                value={subject}
                onChange={(e) => setSubject(e.target.value)}
                className="w-full p-2 border rounded-lg"
              >
                <option>数学</option>
                <option>物理</option>
                <option>化学</option>
                <option>英语</option>
                <option>语文</option>
              </select>
            </div>
            <div className="bg-white rounded-xl p-4 shadow-sm">
              <label className="block text-sm font-medium mb-2">年级</label>
              <select
                value={grade}
                onChange={(e) => setGrade(e.target.value)}
                className="w-full p-2 border rounded-lg"
              >
                <option>小学六年级</option>
                <option>初一</option>
                <option>初二</option>
                <option>初三</option>
                <option>高一</option>
                <option>高二</option>
                <option>高三</option>
              </select>
            </div>
          </div>

          {/* AI分析按钮 */}
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full py-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-bold"
          >
            {loading ? '分析中...' : '🧠 AI智能分析'}
          </button>
        </div>
      )}

      {/* 分析中 */}
      {step === 'analyzing' && (
        <div className="bg-white rounded-xl p-12 shadow-sm text-center">
          <div className="text-6xl mb-4 animate-pulse">🧠</div>
          <h3 className="text-xl font-bold mb-2">AI正在分析中...</h3>
          <p className="text-gray-600">这可能需要几秒钟</p>
        </div>
      )}

      {/* 分析结果 */}
      {step === 'result' && analysisResult && (
        <div className="space-y-6">
          {/* 错误类型 */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center mb-3">
              <span className="text-2xl mr-2">🔴</span>
              <h3 className="font-bold">错误类型</h3>
            </div>
            <p className="text-lg font-semibold text-red-600">{analysisResult.error_type}</p>
          </div>

          {/* 知识点 */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center mb-3">
              <span className="text-2xl mr-2">📚</span>
              <h3 className="font-bold">知识点</h3>
            </div>
            <p className="text-lg">{analysisResult.knowledge_point}</p>
          </div>

          {/* 根本原因 */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <div className="flex items-center mb-3">
              <span className="text-2xl mr-2">🎯</span>
              <h3 className="font-bold">根本原因</h3>
            </div>
            <p className="text-gray-700">{analysisResult.root_cause}</p>
          </div>

          {/* 三维分析 */}
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h3 className="font-bold mb-4">📊 三维分析</h3>
            <div className="space-y-3">
              {analysisResult.dimensions.map((dim, idx) => (
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
              {analysisResult.suggestions.map((suggestion, idx) => (
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
              onClick={() => setStep('preview')}
              className="flex-1 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
            >
              ← 返回修改
            </button>
            <button
              onClick={handleSave}
              className="flex-1 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-bold"
            >
              ✅ 保存到错题本
            </button>
          </div>
        </div>
      )}
    </div>
  )
}

export default CapturePage
