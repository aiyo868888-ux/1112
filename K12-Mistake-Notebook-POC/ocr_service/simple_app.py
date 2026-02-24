"""
简化的OCR服务 - 用于POC测试（不依赖PaddleOCR）
使用Tesseract OCR（如果可用）或返回模拟数据
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import base64
import io
from PIL import Image
import numpy as np

app = FastAPI(title="K12错题本 OCR服务 (简化版)")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "K12错题本 OCR服务运行中 (简化版)", "version": "0.1.0-simple"}

@app.post("/ocr/text")
async def recognize_text(file: UploadFile = File(...)):
    """
    识别图片中的文字内容
    POC版本：返回模拟数据用于测试
    """
    try:
        # 读取图片（用于验证）
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))

        # POC阶段：返回模拟数据
        # 真实环境需要集成Tesseract或其他OCR引擎
        mock_text = """解方程 x² + 2x + 1 = 0

已知一元二次方程：x² + 2x + 1 = 0
求：方程的解

解题步骤：
1. 识别方程类型
2. 选择解法
3. 计算结果"""

        return {
            "success": True,
            "text": mock_text,
            "details": [
                {"text": "解方程 x² + 2x + 1 = 0", "confidence": 0.95},
                {"text": "已知一元二次方程：x² + 2x + 1 = 0", "confidence": 0.92},
                {"text": "求：方程的解", "confidence": 0.98}
            ],
            "char_count": len(mock_text),
            "note": "POC版本 - 返回模拟数据。生产环境需集成真实OCR引擎。"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": ""
        }

@app.post("/ocr/formula")
async def recognize_formula(file: UploadFile = File(...)):
    """
    识别数学公式
    POC版本：返回LaTeX格式的模拟数据
    """
    try:
        # 读取图片
        contents = await file.read()

        # 返回模拟的LaTeX公式
        mock_latex = r"x^2 + 2x + 1 = 0"

        return {
            "success": True,
            "latex": mock_latex,
            "note": "POC版本 - 返回模拟LaTeX。生产环境需集成LaTeX-OCR。"
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "latex": ""
        }

if __name__ == "__main__":
    import uvicorn
    print("OCR Service starting...")
    print("Address: http://localhost:8001")
    print("Note: POC simple version with mock data")
    uvicorn.run(app, host="0.0.0.0", port=8001)
