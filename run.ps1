cd $PSScriptRoot
& .\venv\Scripts\Activate.ps1
Add-Type @"
	using System;
	using System.Runtime.InteropServices;
	public class WinAp {
		[DllImport("user32.dll")]
		[return: MarshalAs(UnmanagedType.Bool)]
		public static extern bool SetForegroundWindow(IntPtr hWnd);

		[DllImport("user32.dll")]
		[return: MarshalAs(UnmanagedType.Bool)]
		public static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);
	}
"@

Start-Job -ScriptBlock {
	$WEBPAGE = "http://localhost:8000"
	While ($true) {
		Start-Sleep -Seconds 2
		try {
			Invoke-WebRequest -Uri $WEBPAGE
			break
		}
		catch {
			continue
		}
	}

	Start-Sleep -Seconds 30
	Start-Process -FilePath "C:\Program Files\Google\Chrome\Application\chrome.exe" -ArgumentList "--kiosk", "$WEBPAGE"

	While ($true) {
		Start-Sleep -Seconds 5
		$p = Get-Process | Where-Object { $_.mainWindowTitle -and $_.Name -like "chrome" }
		if ($p) {
			$handle = $p.MainWindowHandle
			[void] [WinAp]::SetForegroundWindow($handle)
			[void] [WinAp]::ShowWindow($handle, 3)
		}
	}
}
uvicorn app.main:app
deactivate