Write-Host "🚀 Установка зависимостей NeuroPartner..." -ForegroundColor Cyan

# Проверяем Python
$pythonVersion = python --version
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python не установлен" -ForegroundColor Red
    exit 1
}

Write-Host "✅ $pythonVersion" -ForegroundColor Green

Write-Host "Установка pip пакетов..." -ForegroundColor Yellow

$packages = @(
    "google-generativeai==0.3.2",
    "python-dotenv==1.0.0", 
    "requests==2.31.0",
    "aiohttp==3.9.1"
)

foreach ($package in $packages) {
    Write-Host "Установка: $package" -ForegroundColor Gray
    pip install $package --user
}

Write-Host "✅ Основные зависимости установлены!" -ForegroundColor Green
