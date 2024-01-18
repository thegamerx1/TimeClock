cd $PSScriptRoot
& .\venv\Scripts\Activate.ps1
uvicorn app.main:app
deactivate