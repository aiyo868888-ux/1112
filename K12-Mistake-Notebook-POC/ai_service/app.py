"""
AI错因分析服务 - 使用本地Qwen模型
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import json
from typing import List, Dict

app = FastAPI(title="K12错题本 AI分析服务")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ollama API配置
OLLAMA_BASE_URL = "http://localhost:11434"

class MistakeAnalysis(BaseModel):
    """错因分析请求"""
    question: str           # 题目内容
    wrong_answer: str       # 学生的错误答案
    correct_answer: str     # 正确答案
    subject: str = "数学"   # 科目
    grade: str = "初二"     # 年级

class ErrorDimension(BaseModel):
    """错误维度"""
    dimension: str          # 维度名称
    description: str        # 描述
    severity: str           # 严重程度: high/medium/low

class AnalysisResult(BaseModel):
    """分析结果"""
    error_type: str                     # 错误类型
    knowledge_point: str                # 知识点
    root_cause: str                     # 根本原因
    dimensions: List[ErrorDimension]    # 多维分析
    suggestions: List[str]              # 改进建议
    similar_concepts: List[str]         # 关联概念

def get_ollama_response(prompt: str, model: str = "qwen2.5:7b") -> str:
    """调用Ollama本地模型"""
    try:
        response = requests.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 500
                }
            },
            timeout=30
        )
        return response.json().get("response", "")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ollama调用失败: {str(e)}")

def build_analysis_prompt(mistake: MistakeAnalysis) -> str:
    """构建分析提示词"""
    return f"""你是一个专业的K12教育分析师。请分析以下错题：

【题目】
{mistake.question}

【学生的错误答案】
{mistake.wrong_answer}

【正确答案】
{mistake.correct_answer}

【科目】{mistake.subject}
【年级】{mistake.grade}

请从以下三个维度分析错误原因：

1. 知识点维度：是否掌握相关概念/公式/定理？
2. 思维路径维度：解题思路是否正确？在哪一步出错？
3. 学习习惯维度：是否存在审题不清/计算失误/跳步等问题？

请以JSON格式返回分析结果：
{{
    "error_type": "错误类型（如：概念错误/计算错误/思路错误）",
    "knowledge_point": "相关知识点",
    "root_cause": "根本原因的详细描述",
    "dimensions": [
        {{"dimension": "知识点", "description": "...", "severity": "high/medium/low"}},
        {{"dimension": "思维路径", "description": "...", "severity": "high/medium/low"}},
        {{"dimension": "学习习惯", "description": "...", "severity": "high/medium/low"}}
    ],
    "suggestions": ["改进建议1", "改进建议2"],
    "similar_concepts": ["关联概念1", "关联概念2"]
}}

请只返回JSON，不要有其他内容。"""

@app.get("/")
async def root():
    return {"message": "K12错题本 AI分析服务运行中", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    """检查Ollama服务状态"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        return {"ollama_connected": True, "models": response.json().get("models", [])}
    except:
        return {"ollama_connected": False, "error": "Ollama服务未启动，请先运行: ollama run qwen2.5:7b"}

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_mistake(mistake: MistakeAnalysis):
    """
    分析错题原因
    """
    # 构建提示词
    prompt = build_analysis_prompt(mistake)

    # 调用模型
    response_text = get_ollama_response(prompt)

    # 解析JSON结果
    try:
        # 提取JSON部分（模型可能返回额外文字）
        json_start = response_text.find("{")
        json_end = response_text.rfind("}") + 1
        json_str = response_text[json_start:json_end]

        result = json.loads(json_str)
        return AnalysisResult(**result)

    except Exception as e:
        # 如果解析失败，返回默认分析
        return AnalysisResult(
            error_type="分析失败",
            knowledge_point="未知",
            root_cause=f"AI模型输出解析错误: {str(e)}",
            dimensions=[
                ErrorDimension(dimension="知识点", description="请人工分析", severity="medium"),
                ErrorDimension(dimension="思维路径", description="请人工分析", severity="medium"),
                ErrorDimension(dimension="学习习惯", description="请人工分析", severity="medium")
            ],
            suggestions=["请重新提交", "确保Ollama服务正常运行"],
            similar_concepts=[]
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
