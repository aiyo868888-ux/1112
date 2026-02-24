@echo off
REM 启动后端服务 - 简化版（不依赖PaddleOCR和Ollama）

echo 🚀 启动K12错题本后端服务...
echo.

REM 启动OCR服务
echo [1/2] 启动OCR服务 (端口8001)...
start "OCR Service" cmd /k "cd /d %~dp0ocr_service && python simple_app.py"

REM 等待2秒
timeout /t 2 /nobreak >nul

REM 启动AI服务
echo [2/2] 启动AI分析服务 (端口8002)...
start "AI Service" cmd /k "cd /d %~dp0ai_service && python simple_app.py"

echo.
echo ✅ 后端服务启动完成！
echo.
echo 📍 OCR服务: http://localhost:8001
echo 📍 AI服务: http://localhost:8002
echo 📍 前端服务: 请在另一个终端运行 'cd frontend && npm run dev'
echo.
echo 💡 提示：
echo - 不要关闭这两个窗口
echo - 前端访问: http://localhost:5173
echo - 停止服务: 关闭这两个窗口即可
echo.
pause
