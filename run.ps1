cd $PSScriptRoot
& .\venv\Scripts\Activate.ps1
Start-Job -ScriptBlock {
	$WEBPAGE = "http://localhost:8000"
	While($true) {
		Start-Sleep -Seconds 2
		try {
			Invoke-WebRequest -Uri $WEBPAGE
			break
		} catch {
			continue
		}
	}
	& "C:\Program Files\Google\Chrome\Application\chrome.exe" --kiosk $WEBPAGE
}
uvicorn app.main:app
deactivate