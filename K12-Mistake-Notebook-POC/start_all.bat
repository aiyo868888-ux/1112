@echo off
chcp 65001 > nul
echo ============================================================
echo K12错题本 - 完整服务启动 (AI自动检测版)
echo ============================================================
echo.

echo [1/4] 启动OCR服务 (百度OCR)...
cd /d "%~dp0ocr_service"
start "百度OCR服务" python baidu_ocr_app.py
timeout /t 2 /nobreak > nul

echo [2/4] 启动AI分析服务...
cd /d "%~dp0ai_service"
start "AI分析服务" python simple_app.py
timeout /t 2 /nobreak > nul

echo [3/4] 启动题目检测服务 (AI自动检测)...
cd /d "%~dp0detection_service"
start "题目检测服务" python simple_app.py
timeout /t 2 /nobreak > nul

echo [4/4] 启动前端应用...
cd /d "%~dp0frontend"
start "前端应用" npm run dev
timeout /t 3 /nobreak > nul

echo.
echo ============================================================
echo 所有服务已启动！
echo ============================================================
echo.
echo 服务地址:
echo   - 前端应用:     http://localhost:5173
echo   - OCR服务:      http://localhost:8001 (百度OCR)
echo   - AI分析服务:   http://localhost:8002
echo   - 题目检测服务: http://localhost:8003 (AI自动检测)
echo.
echo 新功能:
echo   - AI自动检测题目区域
echo   - 支持手动调整框选
echo   - 一页多题批量识别
echo.
echo 免费额度:
echo   - 百度OCR: 1000次/月 (个人认证)
echo   - 重置时间: 每月1日
echo.
echo 按任意键打开浏览器...
pause > nul

echo 正在打开浏览器...
start http://localhost:5173

echo.
echo ============================================================
echo 启动完成！现在可以测试AI自动检测功能了。
echo ============================================================
echo.
echo 测试步骤:
echo   1. 上传一张试卷图片
echo   2. 等待AI自动检测题目区域 (1-3秒)
echo   3. 查看自动框选结果
echo   4. 调整框选区域 (可选)
echo   5. 点击"完成"进入识别流程
echo.
pause
