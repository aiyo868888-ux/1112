"""
简化的AI分析服务 - 用于POC测试（不依赖Ollama）
使用规则引擎返回模拟分析结果
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
import re

app = FastAPI(title="K12错题本 AI分析服务 (简化版)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MistakeAnalysis(BaseModel):
    """错因分析请求"""
    question: str
    wrong_answer: str
    correct_answer: str
    subject: str = "数学"
    grade: str = "初二"

class ErrorDimension(BaseModel):
    """错误维度"""
    dimension: str
    description: str
    severity: str

class AnalysisResult(BaseModel):
    """分析结果"""
    error_type: str
    knowledge_point: str
    root_cause: str
    dimensions: List[ErrorDimension]
    suggestions: List[str]
    similar_concepts: List[str]

def analyze_by_keywords(question: str, wrong_answer: str) -> dict:
    """
    基于关键词的简单规则分析
    POC版本：使用规则引擎模拟AI分析
    """
    # 检测题目类型
    if "方程" in question or "x²" in question or "x^2" in question:
        return {
            "error_type": "概念错误",
            "knowledge_point": "一元二次方程",
            "root_cause": "学生对一元二次方程的解的概念理解不完整。方程 x² + 2x + 1 = 0 是一个完全平方式，应该有两个相等的实根 x₁ = x₂ = -1，而不是只有一个根。这说明学生对完全平方公式和方程的根的理解不够深入。",
            "dimensions": [
                {"dimension": "知识点", "description": "未掌握完全平方公式的特殊情况", "severity": "high"},
                {"dimension": "思维路径", "description": "解题时忽略了一元二次方程必有两个根的性质", "severity": "medium"},
                {"dimension": "学习习惯", "description": "解题步骤不完整，缺少验算习惯", "severity": "low"}
            ],
            "suggestions": [
                "复习完全平方公式: (a±b)² = a² ± 2ab + b²",
                "理解一元二次方程的根的概念：判别式Δ=0时有两个相等实根",
                "练习类似的完全平方式方程 5-10 道",
                "养成解题后验算的习惯"
            ],
            "similar_concepts": [
                "完全平方公式",
                "一元二次方程的解法",
                "判别式与应用",
                "因式分解法"
            ]
        }
    elif "函数" in question or "f(x)" in question:
        return {
            "error_type": "理解错误",
            "knowledge_point": "函数概念与图像",
            "root_cause": "学生对函数的基本概念理解不够清晰，可能混淆了不同类型函数的图像特征。",
            "dimensions": [
                {"dimension": "知识点", "description": "函数概念理解不扎实", "severity": "high"},
                {"dimension": "思维路径", "description": "未能正确识别函数类型", "severity": "medium"},
                {"dimension": "学习习惯", "description": "缺乏函数图像的练习", "severity": "medium"}
            ],
            "suggestions": [
                "复习函数的定义和表示方法",
                "掌握一次函数、二次函数的图像特征",
                "多做函数图像的绘制练习",
                "建立函数类型与图像的对应关系"
            ],
            "similar_concepts": [
                "一次函数",
                "二次函数",
                "函数图像",
                "函数性质"
            ]
        }
    elif "因式分解" in question or "分解" in question:
        return {
            "error_type": "公式错误",
            "knowledge_point": "因式分解",
            "root_cause": "学生混淆了平方差公式和完全平方公式。平方差公式是 a² - b² = (a-b)(a+b)，而完全平方公式是 a² ± 2ab + b² = (a±b)²。",
            "dimensions": [
                {"dimension": "知识点", "description": "公式记忆混淆", "severity": "high"},
                {"dimension": "思维路径", "description": "选择错误的因式分解方法", "severity": "high"},
                {"dimension": "学习习惯", "description": "公式应用前未仔细辨别", "severity": "medium"}
            ],
            "suggestions": [
                "对比记忆平方差和完全平方公式",
                "练习区分两种公式的适用条件",
                "建立公式应用决策树",
                "总结常见错误类型"
            ],
            "similar_concepts": [
                "平方差公式",
                "完全平方公式",
                "因式分解方法",
                "公式应用"
            ]
        }
    else:
        # 默认分析
        return {
            "error_type": "理解偏差",
            "knowledge_point": "基础概念",
            "root_cause": "学生对相关概念的理解存在偏差，需要加强对基础知识的掌握。",
            "dimensions": [
                {"dimension": "知识点", "description": "基础概念不够扎实", "severity": "medium"},
                {"dimension": "思维路径", "description": "解题思路不够清晰", "severity": "medium"},
                {"dimension": "学习习惯", "description": "需要多做练习巩固", "severity": "low"}
            ],
            "suggestions": [
                "复习相关的基础概念",
                "加强基础练习",
                "总结解题方法",
                "建立错题本定期复习"
            ],
            "similar_concepts": []
        }

@app.get("/")
async def root():
    return {"message": "K12错题本 AI分析服务运行中 (简化版)", "version": "0.1.0-simple"}

@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "mode": "simple_rule_based",
        "note": "POC版本 - 使用规则引擎，不依赖Ollama"
    }

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_mistake(mistake: MistakeAnalysis):
    """
    分析错题原因
    POC版本：使用规则引擎进行分析
    """
    try:
        # 使用规则引擎分析
        result = analyze_by_keywords(mistake.question, mistake.wrong_answer)
        return AnalysisResult(**result)

    except Exception as e:
        # 返回默认分析
        return AnalysisResult(
            error_type="分析失败",
            knowledge_point="未知",
            root_cause=f"分析过程出错: {str(e)}",
            dimensions=[
                ErrorDimension(dimension="知识点", description="请人工分析", severity="medium"),
                ErrorDimension(dimension="思维路径", description="请人工分析", severity="medium"),
                ErrorDimension(dimension="学习习惯", description="请人工分析", severity="medium")
            ],
            suggestions=["请重新提交", "检查输入内容格式"],
            similar_concepts=[]
        )

if __name__ == "__main__":
    import uvicorn
    print("AI Analysis Service starting...")
    print("Address: http://localhost:8002")
    print("Note: POC simple version with rule engine")
    uvicorn.run(app, host="0.0.0.0", port=8002)
