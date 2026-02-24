// API服务配置
const API_BASE_URL = {
  OCR: 'http://localhost:8001',
  AI: 'http://localhost:8002'
}

// OCR服务
export const ocrService = {
  // 识别文字
  async recognizeText(file) {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_BASE_URL.OCR}/ocr/text`, {
        method: 'POST',
        body: formData
      })
      return await response.json()
    } catch (error) {
      console.error('OCR识别失败:', error)
      return { success: false, error: error.message, text: '' }
    }
  },

  // 识别公式
  async recognizeFormula(file) {
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${API_BASE_URL.OCR}/ocr/formula`, {
        method: 'POST',
        body: formData
      })
      return await response.json()
    } catch (error) {
      console.error('公式识别失败:', error)
      return { success: false, error: error.message, latex: '' }
    }
  }
}

// AI分析服务
export const aiService = {
  // 分析错题
  async analyzeMistake(data) {
    try {
      const response = await fetch(`${API_BASE_URL.AI}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      })
      return await response.json()
    } catch (error) {
      console.error('AI分析失败:', error)
      return {
        error_type: '分析失败',
        knowledge_point: '未知',
        root_cause: error.message,
        dimensions: [],
        suggestions: ['请检查AI服务是否正常运行'],
        similar_concepts: []
      }
    }
  },

  // 健康检查
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL.AI}/health`)
      return await response.json()
    } catch (error) {
      return { ollama_connected: false, error: error.message }
    }
  }
}

// 本地存储服务
export const storageService = {
  // 保存错题
  saveMistake(mistake) {
    const mistakes = this.getAllMistakes()
    mistakes.push({
      ...mistake,
      id: Date.now(),
      createdAt: new Date().toISOString()
    })
    localStorage.setItem('mistakes', JSON.stringify(mistakes))
  },

  // 获取所有错题
  getAllMistakes() {
    const data = localStorage.getItem('mistakes')
    return data ? JSON.parse(data) : []
  },

  // 获取单个错题
  getMistake(id) {
    const mistakes = this.getAllMistakes()
    return mistakes.find(m => m.id === id)
  },

  // 更新错题
  updateMistake(id, updates) {
    const mistakes = this.getAllMistakes()
    const index = mistakes.findIndex(m => m.id === id)
    if (index !== -1) {
      mistakes[index] = { ...mistakes[index], ...updates }
      localStorage.setItem('mistakes', JSON.stringify(mistakes))
    }
  },

  // 删除错题
  deleteMistake(id) {
    const mistakes = this.getAllMistakes()
    const filtered = mistakes.filter(m => m.id !== id)
    localStorage.setItem('mistakes', JSON.stringify(filtered))
  }
}
