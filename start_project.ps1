
$projectPath = "D:\Projects\generic-data-ingestion"

# Start the FastAPI backend
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$projectPath'; .\venv\Scripts\Activate.ps1; uvicorn app:app --reload"
)

# Give the backend a moment to start
Start-Sleep -Seconds 3

# Start the frontend server
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "Set-Location '$projectPath'; python -m http.server 5500"
)

# Open the frontend in your browser
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:5500/frontend/"