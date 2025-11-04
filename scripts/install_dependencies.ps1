Write-Host \"🚀 Установка зависимостей NeuroPartner...\" -ForegroundColor Cyan

# Проверяем Python
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host \"❌ Python не установлен\" -ForegroundColor Red
    exit 1
}

Write-Host \"✅ $pythonVersion\" -ForegroundColor Green

Write-Host \"Установка pip пакетов...\" -ForegroundColor Yellow

$packages = @(
    \"python-telegram-bot==20.7\",
    \"google-generativeai==0.3.2\", 
    \"python-dotenv==1.0.0\",
    \"requests==2.31.0\",
    \"aiohttp==3.9.1\"
)

foreach ($package in $packages) {
    Write-Host \"Установка: $package\" -ForegroundColor Gray
    pip install $package --user
    if ($LASTEXITCODE -ne 0) {
        Write-Host \"⚠️  Проблема с: $package\" -ForegroundColor Yellow
    }
}

Write-Host \"✅ Основные зависимости установлены!\" -ForegroundColor Green
