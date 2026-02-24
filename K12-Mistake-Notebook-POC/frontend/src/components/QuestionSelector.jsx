import React, { useState, useRef, useCallback, useEffect } from 'react'

/**
 * 题目区域选择组件（AI自动检测版）
 * 1. 上传图片后自动检测题目区域
 * 2. 用户可以调整框选区域
 * 3. 支持添加、删除、修改框选
 */
function QuestionSelector({ image, onQuestionsSelected, onCancel }) {
  const canvasRef = useRef(null)
  const [imageObj, setImageObj] = useState(null)
  const [rectangles, setRectangles] = useState([])
  const [currentRect, setCurrentRect] = useState(null)
  const [isDrawing, setIsDrawing] = useState(false)
  const [isDragging, setIsDragging] = useState(false)
  const [isResizing, setIsResizing] = useState(false)
  const [selectedRectIndex, setSelectedRectIndex] = useState(null)
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 })
  const [scale, setScale] = useState(1)
  const [isDetecting, setIsDetecting] = useState(true)
  const [detectionMethod, setDetectionMethod] = useState('')

  // 加载图片并自动检测题目
  useEffect(() => {
    const img = new Image()
    img.onload = async () => {
      setImageObj(img)
      // 自动检测题目区域
      await autoDetectQuestions(img)
    }
    img.src = image
  }, [image])

  // AI自动检测题目区域
  const autoDetectQuestions = async (img) => {
    setIsDetecting(true)
    try {
      // 调用检测服务
      const file = await dataURLtoFile(image, 'detect.jpg')
      const formData = new FormData()
      formData.append('file', file)

      const response = await fetch('http://localhost:8003/detect', {
        method: 'POST',
        body: formData
      })

      if (response.ok) {
        const result = await response.json()
        if (result.success && result.questions.length > 0) {
          setRectangles(result.questions)
          setDetectionMethod(result.method)
        } else {
          // 检测失败，不设置任何框
          setRectangles([])
        }
      }
    } catch (error) {
      console.log('自动检测失败，用户可手动框选:', error)
      // 检测失败不影响用户手动操作
    } finally {
      setIsDetecting(false)
    }
  }

  // base64转File
  const dataURLtoFile = async (dataurl, filename) => {
    const res = await fetch(dataurl)
    const blob = await res.blob()
    return new File([blob], filename, { type: 'image/jpeg' })
  }

  // 绘制画布
  const drawCanvas = useCallback(() => {
    const canvas = canvasRef.current
    if (!canvas || !imageObj) return

    const ctx = canvas.getContext('2d')

    // 计算缩放比例
    const containerWidth = canvas.parentElement.clientWidth - 32
    const originalWidth = imageObj.width
    const newScale = containerWidth / originalWidth
    setScale(newScale)

    canvas.width = originalWidth * newScale
    canvas.height = imageObj.height * newScale

    // 绘制图片
    ctx.drawImage(imageObj, 0, 0, canvas.width, canvas.height)

    // 绘制已保存的矩形
    rectangles.forEach((rect, index) => {
      const isSelected = index === selectedRectIndex
      drawRectangle(ctx, rect, index + 1, newScale, false, isSelected)
    })

    // 绘制当前正在画的矩形
    if (currentRect) {
      drawRectangle(ctx, currentRect, rectangles.length + 1, newScale, true, false)
    }
  }, [imageObj, rectangles, currentRect, selectedRectIndex])

  useEffect(() => {
    drawCanvas()
  }, [drawCanvas])

  // 绘制单个矩形
  const drawRectangle = (ctx, rect, number, scale, isPreview = false, isSelected = false) => {
    const { x, y, width, height } = rect

    // 选中的矩形用不同颜色
    const color = isSelected ? '#10B981' : (isPreview ? '#FF6B6B' : '#4F46E5')

    ctx.strokeStyle = color
    ctx.lineWidth = isSelected ? 4 : 3
    ctx.setLineDash(isPreview ? [5, 5] : [])

    ctx.strokeRect(
      x * scale,
      y * scale,
      width * scale,
      height * scale
    )

    ctx.setLineDash([])

    // 绘制半透明背景
    ctx.fillStyle = isPreview ? 'rgba(255, 107, 107, 0.1)' :
                     (isSelected ? 'rgba(16, 185, 129, 0.15)' : 'rgba(79, 70, 229, 0.1)')
    ctx.fillRect(
      x * scale,
      y * scale,
      width * scale,
      height * scale
    )

    // 绘制题号标签
    ctx.fillStyle = color
    ctx.fillRect(
      x * scale,
      y * scale - 28,
      40 * scale,
      28 * scale
    )

    ctx.fillStyle = 'white'
    ctx.font = `bold ${16 * scale}px Arial`
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    ctx.fillText(
      `${number}`,
      x * scale + 20 * scale,
      y * scale - 14 * scale
    )

    // 如果选中，绘制调整手柄
    if (isSelected && !isPreview) {
      const handleSize = 8 * scale
      const handles = [
        { x: x, y: y }, // 左上
        { x: x + width, y: y }, // 右上
        { x: x, y: y + height }, // 左下
        { x: x + width, y: y + height } // 右下
      ]

      ctx.fillStyle = '#10B981'
      handles.forEach(handle => {
        ctx.fillRect(
          handle.x * scale - handleSize / 2,
          handle.y * scale - handleSize / 2,
          handleSize,
          handleSize
        )
      })
    }
  }

  // 获取鼠标在画布上的位置
  const getMousePos = (e) => {
    const canvas = canvasRef.current
    const rect = canvas.getBoundingClientRect()
    return {
      x: (e.clientX - rect.left) / scale,
      y: (e.clientY - rect.top) / scale
    }
  }

  // 检查是否点击了某个矩形
  const getClickedRectIndex = (pos) => {
    for (let i = rectangles.length - 1; i >= 0; i--) {
      const rect = rectangles[i]
      if (pos.x >= rect.x && pos.x <= rect.x + rect.width &&
          pos.y >= rect.y && pos.y <= rect.y + rect.height) {
        return i
      }
    }
    return -1
  }

  // 鼠标按下
  const handleMouseDown = (e) => {
    const pos = getMousePos(e)
    const clickedIndex = getClickedRectIndex(pos)

    if (clickedIndex >= 0) {
      // 选中已有矩形，准备拖动或调整大小
      setSelectedRectIndex(clickedIndex)
      setIsDragging(true)
      setDragStart(pos)
    } else {
      // 取消选中，开始绘制新矩形
      setSelectedRectIndex(-1)
      setIsDrawing(true)
      setCurrentRect({
        x: pos.x,
        y: pos.y,
        width: 0,
        height: 0
      })
    }
  }

  // 鼠标移动
  const handleMouseMove = (e) => {
    const pos = getMousePos(e)

    if (isDragging && selectedRectIndex >= 0) {
      // 拖动已有矩形
      const dx = pos.x - dragStart.x
      const dy = pos.y - dragStart.y

      const updated = [...rectangles]
      updated[selectedRectIndex] = {
        ...updated[selectedRectIndex],
        x: updated[selectedRectIndex].x + dx,
        y: updated[selectedRectIndex].y + dy
      }
      setRectangles(updated)
      setDragStart(pos)
    } else if (isDrawing && currentRect) {
      // 绘制新矩形
      setCurrentRect({
        ...currentRect,
        width: pos.x - currentRect.x,
        height: pos.y - currentRect.y
      })
    }
  }

  // 鼠标松开
  const handleMouseUp = () => {
    if (isDrawing && currentRect) {
      // 标准化矩形
      const normalizedRect = {
        x: currentRect.width < 0 ? currentRect.x + currentRect.width : currentRect.x,
        y: currentRect.height < 0 ? currentRect.y + currentRect.height : currentRect.y,
        width: Math.abs(currentRect.width),
        height: Math.abs(currentRect.height)
      }

      if (normalizedRect.width > 20 && normalizedRect.height > 20) {
        setRectangles([...rectangles, normalizedRect])
        setSelectedRectIndex(rectangles.length)
      }
    }

    setIsDrawing(false)
    setIsDragging(false)
    setCurrentRect(null)
  }

  // 删除选中的矩形
  const handleDeleteSelected = () => {
    if (selectedRectIndex >= 0) {
      const updated = rectangles.filter((_, index) => index !== selectedRectIndex)
      setRectangles(updated)
      setSelectedRectIndex(-1)
    }
  }

  // 清除所有矩形
  const handleClear = () => {
    setRectangles([])
    setSelectedRectIndex(-1)
  }

  // 完成选择
  const handleComplete = () => {
    if (rectangles.length === 0) {
      alert('请至少框选一个题目区域')
      return
    }

    const croppedImages = rectangles.map((rect, index) => {
      const canvas = document.createElement('canvas')
      canvas.width = rect.width
      canvas.height = rect.height

      const ctx = canvas.getContext('2d')
      ctx.drawImage(
        imageObj,
        rect.x, rect.y, rect.width, rect.height,
        0, 0, rect.width, rect.height
      )

      return {
        id: index + 1,
        imageData: canvas.toDataURL('image/jpeg'),
        rect: rect
      }
    })

    onQuestionsSelected(croppedImages)
  }

  return (
    <div className="bg-white rounded-xl p-6 shadow-sm">
      <div className="mb-4">
        <h3 className="text-xl font-bold mb-2">🤖 AI自动检测题目区域</h3>
        <p className="text-gray-600 text-sm">
          {isDetecting
            ? '正在自动检测题目区域，请稍候...'
            : detectionMethod
              ? `已自动检测到 ${rectangles.length} 个题目区域 (检测方法: ${detectionMethod})`
              : '在图片上拖动鼠标框选题目，或点击已框选区域进行调整'}
        </p>
      </div>

      {/* 检测状态提示 */}
      {isDetecting && (
        <div className="mb-4 p-4 bg-blue-50 rounded-lg flex items-center">
          <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-600 mr-3"></div>
          <span className="text-blue-700">AI正在智能分析图片...</span>
        </div>
      )}

      {/* 自动检测成功提示 */}
      {!isDetecting && detectionMethod && rectangles.length > 0 && (
        <div className="mb-4 p-4 bg-green-50 rounded-lg">
          <p className="text-green-700 font-medium mb-2">
            ✅ 自动检测完成！检测到 {rectangles.length} 个题目区域
          </p>
          <p className="text-sm text-green-600">
            提示：点击框选区域可以选中调整，拖动可以移动位置
          </p>
        </div>
      )}

      {/* 画布容器 */}
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-4 mb-4 overflow-auto">
        <canvas
          ref={canvasRef}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseUp}
          className="cursor-crosshair w-full"
        />
      </div>

      {/* 已框选题目数 */}
      {rectangles.length > 0 && (
        <div className="mb-4 p-3 bg-indigo-50 rounded-lg">
          <p className="text-indigo-700 font-medium">
            {selectedRectIndex >= 0
              ? `✅ 已选中第 ${selectedRectIndex + 1} 个题目区域`
              : `✅ 共 ${rectangles.length} 个题目区域`}
          </p>
        </div>
      )}

      {/* 操作按钮 */}
      <div className="flex gap-3 flex-wrap">
        <button
          onClick={onCancel}
          className="px-4 py-3 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition"
        >
          取消
        </button>
        <button
          onClick={handleDeleteSelected}
          disabled={selectedRectIndex < 0}
          className="px-4 py-3 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition disabled:opacity-50"
        >
          🗑 删除选中
        </button>
        <button
          onClick={handleClear}
          disabled={rectangles.length === 0}
          className="px-4 py-3 bg-yellow-100 text-yellow-700 rounded-lg hover:bg-yellow-200 transition disabled:opacity-50"
        >
          🔄 清除全部
        </button>
        <button
          onClick={handleComplete}
          disabled={rectangles.length === 0}
          className="flex-1 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition font-bold disabled:opacity-50"
        >
          ✓ 完成 ({rectangles.length} 题)
        </button>
      </div>

      {/* 使用提示 */}
      <div className="mt-4 p-4 bg-gray-50 rounded-lg">
        <h4 className="font-medium mb-2">💡 操作提示</h4>
        <ul className="text-sm text-gray-600 space-y-1">
          <li>• 系统已自动检测题目区域（绿色边框为选中状态）</li>
          <li>• 点击任意框选区域可以选中，选中后可拖动调整位置</li>
          <li>• 点击空白处可以绘制新的框选区域</li>
          <li>• 点击"删除选中"可以删除不需要的框选</li>
          <li>• 调整完成后点击"完成"进行OCR识别</li>
        </ul>
      </div>
    </div>
  )
}

export default QuestionSelector
