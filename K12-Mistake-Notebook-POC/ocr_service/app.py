"""
OCR服务 - 识别题目文字和数学公式
"""
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image
import io
import base64

app = FastAPI(title="K12错题本 OCR服务")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化PaddleOCR
ocr = PaddleOCR(
    use_angle_cls=True,
    lang='ch',
    use_gpu=False,
    show_log=False
)

@app.get("/")
async def root():
    return {"message": "K12错题本 OCR服务运行中", "version": "0.1.0"}

@app.post("/ocr/text")
async def recognize_text(file: UploadFile = File(...)):
    """
    识别图片中的文字内容
    """
    try:
        # 读取图片
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)

        # OCR识别
        result = ocr.ocr(image_np, cls=True)

        # 提取文本
        texts = []
        if result and result[0]:
            for line in result[0]:
                box, (text, confidence) = line
                texts.append({
                    "text": text,
                    "confidence": float(confidence),
                    "box": box
                })

        # 组合完整文本
        full_text = "\n".join([t["text"] for t in texts])

        return {
            "success": True,
            "text": full_text,
            "details": texts,
            "char_count": len(full_text)
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
    识别数学公式 (返回LaTeX格式)
    TODO: Week 2集成LaTeX-OCR
    """
    # 暂时使用普通OCR，公式识别需要额外模型
    result = await recognize_text(file)
    return {
        "success": result["success"],
        "latex": result["text"],  # 占位符
        "note": "公式识别功能将在Week 2实现"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
