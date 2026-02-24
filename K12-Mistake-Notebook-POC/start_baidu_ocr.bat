@echo off
chcp 65001 > nul
echo ============================================================
echo K12错题本 - 启动脚本 (百度OCR版)
echo ============================================================
echo.

echo [1/3] 启动OCR服务...
cd /d "%~dp0ocr_service"
start "百度OCR服务" python baidu_ocr_app.py
timeout /t 3 /nobreak > nul

echo [2/3] 启动AI分析服务...
cd /d "%~dp0ai_service"
start "AI分析服务" python simple_app.py
timeout /t 2 /nobreak > nul

echo [3/3] 启动前端应用...
cd /d "%~dp0frontend"
start "前端应用" npm run dev
timeout /t 3 /nobreak > nul

echo.
echo ============================================================
echo 所有服务已启动！
echo ============================================================
echo.
echo 服务地址:
echo   - 前端应用: http://localhost:5173
echo   - OCR服务:  http://localhost:8001
echo   - AI服务:   http://localhost:8002
echo.
echo 免费额度信息:
echo   - 百度OCR: 1000次/月 (个人认证)
echo   - 腾讯OCR: 1000次/月 (可选)
echo   - 重置时间: 每月1日
echo.
echo 按任意键打开浏览器...
pause > nul

echo 正在打开浏览器...
start http://localhost:5173

echo.
echo 启动完成！现在可以开始测试了。
echo.
echo 提示:
echo   1. 上传一张试卷图片
echo   2. 点击"重新识别"测试OCR
echo   3. 点击"AI分析"测试智能分析
echo.
pause
