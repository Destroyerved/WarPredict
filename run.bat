@echo off
echo ========================================
echo War Prediction & Conflict Simulator
echo ========================================
echo.

REM Check if Docker is available
where docker >nul 2>&1
if %errorlevel%==0 (
    echo [1] Running with Docker (Recommended)
    echo [2] Running locally (Manual)
    echo.
    set /p choice="Choose option [1/2]: "
    
    if "%choice%"=="1" goto docker_run
    if "%choice%"=="2" goto local_run
    echo Invalid choice. Running with Docker...
    goto docker_run
) else (
    echo Docker not found. Running locally...
    goto local_run
)

:docker_run
echo.
echo Starting Docker containers...
docker-compose up --build
goto end

:local_run
echo.
echo [1] Start Backend only
echo [2] Start Frontend only
echo [3] Start Streamlit only
echo [4] Start all services
echo.
set /p choice="Choose option [1-4]: "

if "%choice%"=="1" goto backend_only
if "%choice%"=="2" goto frontend_only
if "%choice%"=="3" goto streamlit_only
if "%choice%"=="4" goto all_local

:backend_only
echo Starting FastAPI backend on port 8000...
start "Backend" cmd /k "pip install -r requirements.txt >nul 2>&1 && uvicorn backend.api.main:app --reload --port 8000"
goto end

:frontend_only
echo Starting React frontend on port 5173...
start "Frontend" cmd /k "cd frontend && npm install && npm run dev"
goto end

:streamlit_only
echo Starting Streamlit app on port 8501...
start "Streamlit" cmd /k "pip install -r requirements.txt >nul 2>&1 && streamlit run streamlit_app/app.py"
goto end

:all_local
echo Starting all services...
echo.
echo Starting Backend on port 8000...
start "Backend" cmd /k "pip install -r requirements.txt >nul 2>&1 && uvicorn backend.api.main:app --reload --port 8000"
timeout /t 2 /nobreak >nul
echo Starting Frontend on port 5173...
start "Frontend" cmd /k "cd frontend && npm install && npm run dev"
timeout /t 2 /nobreak >nul
echo Starting Streamlit on port 8501...
start "Streamlit" cmd /k "pip install -r requirements.txt >nul 2>&1 && streamlit run streamlit_app/app.py"
goto end

:end
echo.
echo ========================================
echo Services started!
echo ========================================
echo.
echo URLs:
echo   - Frontend:    http://localhost:5173
echo   - API:         http://localhost:8000
echo   - Streamlit:   http://localhost:8501
echo.
pause