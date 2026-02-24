#!/bin/bash
# K12错题本POC - 快速启动脚本

echo "🎯 K12智能错题本 - POC环境启动"
echo "=================================="

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 未安装Python3，请先安装"
    exit 1
fi

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "❌ 未安装Node.js，请先安装"
    exit 1
fi

echo "✅ 环境检查通过"

# 安装Python依赖
echo ""
echo "📦 安装Python依赖..."
pip install -r requirements.txt

# 安装前端依赖
echo "📦 安装前端依赖..."
cd frontend
npm install
cd ..

# 检查Ollama
echo ""
echo "🤖 检查Ollama服务..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama已安装"

    # 检查模型
    if ollama list | grep -q "qwen2.5:7b"; then
        echo "✅ Qwen2.5-7B模型已下载"
    else
        echo "📥 下载Qwen2.5-7B模型(首次运行约5GB)..."
        ollama pull qwen2.5:7b
    fi
else
    echo "⚠️  Ollama未安装"
    echo "   请访问 https://ollama.ai 下载安装"
    echo "   安装后运行: ollama run qwen2.5:7b"
fi

echo ""
echo "🚀 启动服务..."
echo "=================================="
echo ""
echo "请在新终端窗口运行以下命令："
echo ""
echo "1. 启动OCR服务 (端口8001):"
echo "   python ocr_service/app.py"
echo ""
echo "2. 启动AI分析服务 (端口8002):"
echo "   python ai_service/app.py"
echo ""
echo "3. 启动前端服务 (端口5173):"
echo "   cd frontend && npm run dev"
echo ""
echo "然后访问: http://localhost:5173"
echo ""
