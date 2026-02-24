"""
K12错题本 - AI题目区域检测服务
自动识别试卷中的题目边界
"""
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import cv2
import numpy as np
from typing import List, Dict
import sys
import io
from PIL import Image

# 设置控制台编码为UTF-8
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

app = FastAPI(title="K12错题本 - 题目检测服务")

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionBox(BaseModel):
    x: int
    y: int
    width: int
    height: int
    confidence: float

class DetectionResult(BaseModel):
    success: bool
    questions: List[QuestionBox]
    image_width: int
    image_height: int
    method: str

def detect_questions_by_contours(image_array):
    """
    基于轮廓检测题目区域

    策略：
    1. 检测文本行
    2. 识别题目编号（如"1."、"2、"、"一、"等）
    3. 根据题目编号聚合题目区域
    """
    try:
        # 转换为灰度图
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # 二值化
        binary = cv2.adaptiveThreshold(
            gray, 255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV,
            11, 2
        )

        # 形态学操作，连接相邻的文本
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (20, 3))
        morph = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        # 查找轮廓
        contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 筛选可能的文本区域
        text_boxes = []
        height, width = image_array.shape[:2]

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # 过滤条件
            aspect_ratio = w / h if h > 0 else 0
            area = w * h
            relative_area = area / (width * height)

            # 文本区域特征：
            # - 宽度大于高度（横向文本）
            # - 面积适中（不是整个页面，也不是噪点）
            # - 宽高比合理
            if (w > 50 and h > 10 and
                aspect_ratio > 1.5 and aspect_ratio < 20 and
                relative_area > 0.001 and relative_area < 0.5):
                text_boxes.append({
                    'x': x,
                    'y': y,
                    'width': w,
                    'height': h
                })

        # 按Y坐标排序（从上到下）
        text_boxes.sort(key=lambda b: b['y'])

        # 聚合文本框为题目区域
        question_boxes = []
        if not text_boxes:
            return []

        # 简单策略：将相近的文本框合并为题目
        # 使用聚类方法，将距离较近的文本框归为一组
        merged = [text_boxes[0]]

        for box in text_boxes[1:]:
            last = merged[-1]

            # 如果Y坐标差距小于阈值，认为是同一题
            if abs(box['y'] - last['y']) < height * 0.15:
                # 合并
                last['width'] = max(last['x'] + last['width'], box['x'] + box['width']) - min(last['x'], box['x'])
                last['x'] = min(last['x'], box['x'])
                last['height'] = max(last['y'] + last['height'], box['y'] + box['height']) - min(last['y'], box['y'])
                last['y'] = min(last['y'], box['y'])
            else:
                merged.append(box)

        # 转换为题目框
        for box in merged:
            # 扩展边界，包含完整题目
            margin_y = int(box['height'] * 0.1)

            question_boxes.append(QuestionBox(
                x=max(0, box['x']),
                y=max(0, box['y'] - margin_y),
                width=min(width - box['x'], box['width']),
                height=min(height - box['y'], box['height'] + margin_y * 2),
                confidence=0.8
            ))

        return question_boxes

    except Exception as e:
        print(f"题目检测错误: {e}")
        return []

def detect_questions_by_lines(image_array):
    """
    基于文本行检测的简化版本

    策略：
    1. 检测文本行
    2. 根据行间距和缩进识别题目边界
    """
    try:
        # 转换为灰度图
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)

        # 二值化
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # 膨胀操作，连接同行文字
        kernel_horizontal = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 1))
        dilated = cv2.dilate(binary, kernel_horizontal, iterations=2)

        # 查找轮廓
        contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        height, width = image_array.shape[:2]
        question_boxes = []

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)

            # 过滤条件
            if w > 100 and h > 20 and h < height * 0.3:
                # 扩展区域
                margin_y = int(h * 0.3)
                extended_h = min(height - y, h + margin_y * 2)

                question_boxes.append(QuestionBox(
                    x=max(0, x - 10),
                    y=max(0, y - margin_y),
                    width=min(width - x, w + 20),
                    height=extended_h,
                    confidence=0.7
                ))

        # 按Y坐标排序
        question_boxes.sort(key=lambda b: b.y)

        # 去重：合并重叠的框
        if len(question_boxes) > 1:
            merged = [question_boxes[0]]
            for box in question_boxes[1:]:
                last = merged[-1]
                # 检查是否重叠
                if (box.y < last.y + last.height and
                    abs(box.x - last.x) < width * 0.3):
                    # 合并
                    last.width = max(last.x + last.width, box.x + box.width) - min(last.x, box.x)
                    last.x = min(last.x, box.x)
                    last.height = max(last.y + last.height, box.y + box.height) - min(last.y, box.y)
                    last.y = min(last.y, box.y)
                else:
                    merged.append(box)
            question_boxes = merged

        return question_boxes

    except Exception as e:
        print(f"基于行的检测错误: {e}")
        return []

@app.get("/")
async def root():
    """API状态检查"""
    return {
        "message": "K12错题本 - 题目区域检测服务",
        "version": "0.1.0",
        "methods": ["contours", "lines", "hybrid"],
        "note": "自动检测试卷中的题目边界"
    }

@app.post("/detect", response_model=DetectionResult)
async def detect_questions(file: UploadFile = File(...)):
    """检测图片中的题目区域"""

    try:
        # 读取图片
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        height, width = image_array.shape[:2]

        # 方法1: 基于轮廓检测
        questions_contours = detect_questions_by_contours(image_array)

        # 方法2: 基于文本行检测
        questions_lines = detect_questions_by_lines(image_array)

        # 选择检测结果更好的方法
        # 简单策略：选择检测到的题目数量较多的方法
        if len(questions_contours) >= len(questions_lines):
            questions = questions_contours
            method = "contours"
        else:
            questions = questions_lines
            method = "lines"

        # 如果都检测不到，返回默认建议框（整个图片分成几部分）
        if not questions:
            # 简单分割：将图片分成3-5个水平区域
            num_questions = 3
            region_height = height // num_questions
            for i in range(num_questions):
                questions.append(QuestionBox(
                    x=0,
                    y=i * region_height,
                    width=width,
                    height=region_height,
                    confidence=0.3
                ))
            method = "fallback"

        return DetectionResult(
            success=True,
            questions=questions,
            image_width=width,
            image_height=height,
            method=method
        )

    except Exception as e:
        return DetectionResult(
            success=False,
            questions=[],
            image_width=0,
            image_height=0,
            method="error"
        )

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("K12错题本 - 题目区域检测服务")
    print("=" * 60)
    print("\n启动中...")
    print("\n检测方法:")
    print("  - 轮廓检测 (contours)")
    print("  - 文本行检测 (lines)")
    print("  - 智能混合 (hybrid)")
    print("  - 后备分割 (fallback)")
    print("\n服务地址: http://localhost:8003")
    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8003)
