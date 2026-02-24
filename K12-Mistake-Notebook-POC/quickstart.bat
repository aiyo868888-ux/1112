@echo off
REM K12错题本POC - Windows快速启动脚本

echo 🎯 K12智能错题本 - POC环境启动
echo ==================================

REM 检查Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装Python，请先安装
    pause
    exit /b 1
)

REM 检查Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装Node.js，请先安装
    pause
    exit /b 1
)

echo ✅ 环境检查通过

REM 安装Python依赖
echo.
echo 📦 安装Python依赖...
pip install -r requirements.txt

REM 安装前端依赖
echo 📦 安装前端依赖...
cd frontend
call npm install
cd ..

REM 检查Ollama
echo.
echo 🤖 检查Ollama服务...
ollama --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama未安装
    echo    请访问 https://ollama.ai 下载安装
    echo    安装后运行: ollama run qwen2.5:7b
) else (
    echo ✅ Ollama已安装

    REM 检查模型
    ollama list | findstr "qwen2.5:7b" >nul
    if errorlevel 1 (
        echo 📥 下载Qwen2.5-7B模型(首次运行约5GB)...
        ollama pull qwen2.5:7b
    ) else (
        echo ✅ Qwen2.5-7B模型已下载
    )
)

echo.
echo 🚀 启动服务...
echo ==================================
echo.
echo 请在新终端窗口运行以下命令:
echo.
echo 1. 启动OCR服务 (端口8001):
echo    python ocr_service\app.py
echo.
echo 2. 启动AI分析服务 (端口8002):
echo    python ai_service\app.py
echo.
echo 3. 启动前端服务 (端口5173):
echo    cd frontend ^&^& npm run dev
echo.
echo 然后访问: http://localhost:5173
echo.

pause
