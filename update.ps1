#### Get current user
$user = whoami
$user = $user.split("\")[1]
#### Change location to current user Desktop
Set-Location -Path C:\Users\$user\Desktop\
Remove-Item -Path .\InventorySystem.exe -Force
#### Change location to InventoryRepo
Set-Location -Path C:\Users\$user\Desktop\InventoryRepo
#### Create the application
python -m PyInstaller .\main.py -F --name InventorySystem --clean --add-data ".\callUpdate.ps1;.\" --add-data "S:\Documents\InventorySystemCredentials\credentials.json;.\" --distpath "..\"
Start-Process -FilePath "powershell" -ArgumentList $command -Wait
#### Change location to desktop and delete the git repo
Set-Location ..\
Remove-Item -Path .\InventoryRepo -Recurse -Force
#### Launch the new updated InventorySystem application
Start-Process -FilePath .\InventorySystem