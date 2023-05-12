#### Get current user
$user = whoami
$user = $user.split("\")[1]
#### Change location to current user Desktop
Set-Location -Path C:\Users\$user\Desktop\
#### Stop and Delete the inventory application
Stop-Process -Name InventorySystem
#### Clone the git repo
$gitrepo = "https://github.com/SaiPrabhathK/StemCenterInventoryManagement.git"
C:\"Program Files"\Git\bin\git clone $gitrepo InventoryRepo
#### Change location to the cloned git repo
#Set-Location .\InventoryRepo
#### check and install necessary modules
$modules = "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib"
if ( !($modules) )
{
    $modules
}
$pyinstaller = "pip install pyinstaller"
if ( !($pyinstaller) )
{
    $pyinstaller
}
#### Start and run update script in the git repo to build the application from python scripts.
Start-Process -FilePath "powershell" -ArgumentList ".\InventoryRepo\update.ps1"
