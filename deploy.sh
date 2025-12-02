#!/bin/bash

# Script para construir y ejecutar el contenedor Docker en Linux

echo "======================================================================"
echo "  DOCKER - LSM PREDICTOR - DEPLOY SCRIPT"
echo "======================================================================"

# Verificar si Docker está instalado
echo -e "\n[1/5] Verificando Docker..."
if command -v docker &> /dev/null; then
    echo "  ✓ Docker encontrado"
    docker --version
else
    echo "  ✗ Docker no está instalado"
    echo "  Instala Docker con: sudo apt install docker.io docker-compose"
    exit 1
fi

# Verificar archivos necesarios
echo -e "\n[2/5] Verificando archivos necesarios..."
archivos=(
    "Dockerfile"
    "docker-compose.yml"
    "servidor.py"
    "predictor_lsm.py"
    "mejor_modelo.pkl"
    "scaler.pkl"
    "label_encoder.pkl"
    "templates/index.html"
)

faltantes=0
for archivo in "${archivos[@]}"; do
    if [ -f "$archivo" ]; then
        echo "  ✓ $archivo"
    else
        echo "  ✗ $archivo"
        faltantes=$((faltantes + 1))
    fi
done

if [ $faltantes -gt 0 ]; then
    echo -e "\n  Archivos faltantes. Abortando..."
    exit 1
fi

# Detener contenedor si existe
echo -e "\n[3/5] Limpiando contenedores previos..."
docker-compose down 2>/dev/null
echo "  ✓ Limpieza completada"

# Construir imagen
echo -e "\n[4/5] Construyendo imagen Docker..."
docker-compose build
if [ $? -eq 0 ]; then
    echo "  ✓ Imagen construida exitosamente"
else
    echo "  ✗ Error al construir imagen"
    exit 1
fi

# Ejecutar contenedor
echo -e "\n[5/5] Iniciando contenedor..."
docker-compose up -d
if [ $? -eq 0 ]; then
    echo "  ✓ Contenedor iniciado exitosamente"
else
    echo "  ✗ Error al iniciar contenedor"
    exit 1
fi

# Esperar a que el servidor esté listo
echo -e "\n⏳ Esperando que el servidor esté listo..."
sleep 5

# Verificar estado
echo -e "\n======================================================================"
echo "  ✓ SERVIDOR DESPLEGADO EXITOSAMENTE"
echo "======================================================================"

# Obtener IP local
ip=$(hostname -I | awk '{print $1}')

echo -e "\n📍 URLs de acceso:"
echo "  • Local:      http://localhost:3000"
if [ ! -z "$ip" ]; then
    echo "  • Red local:  http://$ip:3000"
fi

echo -e "\n📊 Comandos útiles:"
echo "  • Ver logs:      docker-compose logs -f"
echo "  • Detener:       docker-compose down"
echo "  • Reiniciar:     docker-compose restart"
echo "  • Ver estado:    docker-compose ps"

echo -e "\n🌐 Para exponer a internet:"
echo "  1. Instalar ngrok: https://ngrok.com/download"
echo "  2. Ejecutar:       ngrok http 3000"

echo -e "\n🔥 Para acceso en producción:"
echo "  • Abrir puerto:    sudo ufw allow 3000"
echo "  • Ver firewall:    sudo ufw status"

echo -e "\n======================================================================"
echo ""
echo "✓ Script completado"
echo ""
echo "Accede a: http://localhost:3000"
