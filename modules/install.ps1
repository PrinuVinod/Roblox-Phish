$arch = (Get-WmiObject Win32_Processor).Architecture
if ($arch -like '*arm*' -or $arch -like '*Android*') {
    Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-arm.zip' -OutFile 'cloudflared-windows-arm.zip'
    Expand-Archive -Path 'cloudflared-windows-arm.zip' -DestinationPath 'server'
    Rename-Item -Path 'server/cloudflared-windows-arm.exe' -NewName 'server/cloudflared.exe'
} elseif ($arch -like '*64*') {
    Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.zip' -OutFile 'cloudflared-windows-amd64.zip'
    Expand-Archive -Path 'cloudflared-windows-amd64.zip' -DestinationPath 'server'
    Rename-Item -Path 'server/cloudflared-windows-amd64.exe' -NewName 'server/cloudflared.exe'
} else {
    Invoke-WebRequest -Uri 'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-386.zip' -OutFile 'cloudflared-windows-386.zip'
    Expand-Archive -Path 'cloudflared-windows-386.zip' -DestinationPath 'server'
    Rename-Item -Path 'server/cloudflared-windows-386.exe' -NewName 'server/cloudflared.exe'
}
