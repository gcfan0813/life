@echo off
echo 正在启动无限人生：AI编年史...
echo.

echo 步骤1: 启动后端服务...
cd backend
start python main.py
timeout /t 5 >nul
echo.

echo 步骤2: 启动前端服务...
cd ..
start npm run dev
timeout /t 5 >nul
echo.

echo ========================================
echo 服务启动完成！
echo ========================================
echo.
echo 访问地址：
echo  前端: http://localhost:3002/
echo  后端: http://localhost:8000/
echo  API文档: http://localhost:8000/docs
echo.
echo 按任意键关闭此窗口...
pause >nul
