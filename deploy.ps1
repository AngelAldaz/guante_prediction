# Script para construir y ejecutar el contenedor Docker

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*69) -ForegroundColor Cyan
Write-Host "  DOCKER - LSM PREDICTOR - DEPLOY SCRIPT" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*69) -ForegroundColor Cyan

# Verificar si Docker está instalado
Write-Host "`n[1/5] Verificando Docker..." -ForegroundColor Cyan
if (Get-Command docker -ErrorAction SilentlyContinue) {
    Write-Host "  ✓ Docker encontrado" -ForegroundColor Green
    docker --version
} else {
    Write-Host "  ✗ Docker no está instalado" -ForegroundColor Red
    Write-Host "  Descarga Docker Desktop: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Verificar archivos necesarios
Write-Host "`n[2/5] Verificando archivos necesarios..." -ForegroundColor Cyan
$archivos = @(
    "Dockerfile",
    "docker-compose.yml",
    "servidor.py",
    "predictor_lsm.py",
    "mejor_modelo.pkl",
    "scaler.pkl",
    "label_encoder.pkl",
    "templates/index.html"
)

$faltantes = @()
foreach ($archivo in $archivos) {
    if (Test-Path $archivo) {
        Write-Host "  ✓ $archivo" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $archivo" -ForegroundColor Red
        $faltantes += $archivo
    }
}

if ($faltantes.Count -gt 0) {
    Write-Host "`n  Archivos faltantes. Abortando..." -ForegroundColor Red
    exit 1
}

# Detener contenedor si existe
Write-Host "`n[3/5] Limpiando contenedores previos..." -ForegroundColor Cyan
docker-compose down 2>$null
Write-Host "  ✓ Limpieza completada" -ForegroundColor Green

# Construir imagen
Write-Host "`n[4/5] Construyendo imagen Docker..." -ForegroundColor Cyan
docker-compose build
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Imagen construida exitosamente" -ForegroundColor Green
} else {
    Write-Host "  ✗ Error al construir imagen" -ForegroundColor Red
    exit 1
}

# Ejecutar contenedor
Write-Host "`n[5/5] Iniciando contenedor..." -ForegroundColor Cyan
docker-compose up -d
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Contenedor iniciado exitosamente" -ForegroundColor Green
} else {
    Write-Host "  ✗ Error al iniciar contenedor" -ForegroundColor Red
    exit 1
}

# Esperar a que el servidor esté listo
Write-Host "`n⏳ Esperando que el servidor esté listo..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Verificar estado
Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("="*69) -ForegroundColor Green
Write-Host "  ✓ SERVIDOR DESPLEGADO EXITOSAMENTE" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Green
Write-Host ("="*69) -ForegroundColor Green

# Obtener IP local
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*"} | Select-Object -First 1).IPAddress

Write-Host "`n📍 URLs de acceso:" -ForegroundColor Cyan
Write-Host "  • Local:      http://localhost:3000" -ForegroundColor White
if ($ip) {
    Write-Host "  • Red local:  http://$($ip):3000" -ForegroundColor White
}
Write-Host "`n📊 Comandos útiles:" -ForegroundColor Cyan
Write-Host "  • Ver logs:      docker-compose logs -f" -ForegroundColor White
Write-Host "  • Detener:       docker-compose down" -ForegroundColor White
Write-Host "  • Reiniciar:     docker-compose restart" -ForegroundColor White
Write-Host "  • Ver estado:    docker-compose ps" -ForegroundColor White

Write-Host "`n🌐 Para exponer a internet:" -ForegroundColor Cyan
Write-Host "  1. Instalar ngrok: https://ngrok.com/download" -ForegroundColor White
Write-Host "  2. Ejecutar:       ngrok http 3000" -ForegroundColor White

Write-Host "`n" -NoNewline
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("="*69) -ForegroundColor Cyan
Write-Host ""

# Abrir navegador (opcional)
$respuesta = Read-Host "`n¿Deseas abrir el navegador? (s/n)"
if ($respuesta -eq "s" -or $respuesta -eq "S") {
    Start-Process "http://localhost:3000"
}

Write-Host "`n✓ Script completado" -ForegroundColor Green
