# 🐳 Docker - Guía de Despliegue

## 🚀 Inicio Rápido con Docker

### Opción 1: Docker Compose (Recomendado)

```bash
# Construir y levantar el contenedor
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener
docker-compose down
```

El servidor estará disponible en: **http://localhost:5000**

### Opción 2: Docker manual

```bash
# Construir imagen
docker build -t lsm-predictor .

# Ejecutar contenedor
docker run -d -p 5000:5000 --name lsm-predictor lsm-predictor

# Ver logs
docker logs -f lsm-predictor

# Detener
docker stop lsm-predictor

# Eliminar
docker rm lsm-predictor
```

## 📦 Archivos Docker

- **`Dockerfile`** - Definición de la imagen
- **`docker-compose.yml`** - Orquestación del contenedor
- **`.dockerignore`** - Archivos excluidos de la imagen

## 🌐 Exponer a Internet

### Opción A: Usando ngrok (Más fácil)

1. **Instalar ngrok:**

   - Descarga de: https://ngrok.com/download
   - O con chocolatey: `choco install ngrok`

2. **Exponer el puerto:**

   ```bash
   ngrok http 5000
   ```

3. **Obtendrás una URL pública:**
   ```
   Forwarding: https://xxxx-xx-xx-xx-xx.ngrok.io -> http://localhost:5000
   ```

### Opción B: Servidor en la nube

#### Con VPS (DigitalOcean, AWS, Azure, etc.)

1. **Instalar Docker en el servidor:**

   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

2. **Copiar archivos al servidor:**

   ```bash
   scp -r * usuario@tu-servidor:/home/usuario/lsm-predictor/
   ```

3. **Levantar el servicio:**

   ```bash
   ssh usuario@tu-servidor
   cd lsm-predictor
   docker-compose up -d
   ```

4. **Configurar firewall:**
   ```bash
   sudo ufw allow 5000
   ```

Tu servidor estará en: `http://tu-ip-publica:5000`

#### Con Railway.app (Gratis)

1. Crear cuenta en https://railway.app
2. Conectar tu repositorio de GitHub
3. Railway detectará automáticamente el Dockerfile
4. Se desplegará automáticamente
5. Obtendrás una URL pública

#### Con Render.com (Gratis)

1. Crear cuenta en https://render.com
2. New > Web Service
3. Conectar repositorio
4. Seleccionar "Docker"
5. Port: 5000
6. Deploy

#### Con Fly.io (Gratis)

```bash
# Instalar flyctl
powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"

# Login
flyctl auth login

# Lanzar app
flyctl launch

# Desplegar
flyctl deploy
```

## 🔐 Configurar HTTPS con Nginx

Si tienes un dominio, puedes usar Nginx como proxy reverso:

**docker-compose.yml actualizado:**

```yaml
version: "3.8"

services:
  lsm-predictor:
    build: .
    container_name: lsm-predictor
    restart: unless-stopped
    networks:
      - lsm-network

  nginx:
    image: nginx:alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - lsm-predictor
    networks:
      - lsm-network

networks:
  lsm-network:
    driver: bridge
```

**nginx.conf:**

```nginx
events {
    worker_connections 1024;
}

http {
    server {
        listen 80;
        server_name tu-dominio.com;

        location / {
            proxy_pass http://lsm-predictor:5000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

## 🔍 Comandos Útiles

```bash
# Ver contenedores activos
docker ps

# Ver logs en tiempo real
docker-compose logs -f

# Reiniciar servicio
docker-compose restart

# Ver uso de recursos
docker stats

# Entrar al contenedor
docker exec -it lsm-predictor bash

# Reconstruir imagen
docker-compose build --no-cache

# Limpiar todo
docker-compose down -v
docker system prune -a
```

## 📊 Variables de Entorno

Puedes crear un archivo `.env`:

```env
FLASK_ENV=production
PORT=5000
HOST=0.0.0.0
```

Y actualizar `docker-compose.yml`:

```yaml
services:
  lsm-predictor:
    env_file:
      - .env
```

## 🚨 Firewall en Windows

Si estás en Windows y otros dispositivos no pueden acceder:

```powershell
# Permitir puerto 5000 en firewall
New-NetFirewallRule -DisplayName "LSM Predictor" -Direction Inbound -LocalPort 5000 -Protocol TCP -Action Allow
```

## 🌍 Acceder desde red local

Una vez corriendo Docker, otros dispositivos en tu red pueden acceder con:

```
http://TU_IP_LOCAL:5000
```

Para obtener tu IP local:

```powershell
ipconfig
# Busca "IPv4 Address" en tu adaptador de red
```

## 📱 Acceso desde móvil

Si tu PC y móvil están en la misma red WiFi:

```
http://192.168.x.x:5000
```

## ⚙️ Producción con Gunicorn

Para mejor rendimiento en producción, modifica el **Dockerfile**:

```dockerfile
# Instalar gunicorn
RUN pip install gunicorn

# Cambiar CMD
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "servidor:app"]
```

Y actualiza **requirements.txt**:

```
gunicorn>=21.0.0
```

## 📈 Monitoreo

Agregar healthcheck en `docker-compose.yml`:

```yaml
services:
  lsm-predictor:
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/obtener_texto"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 🎯 Resumen Rápido

**Local:**

```bash
docker-compose up -d
# Acceder: http://localhost:5000
```

**Internet (ngrok):**

```bash
ngrok http 5000
# Te da URL pública
```

**Nube (Railway):**

1. Push a GitHub
2. Conectar en railway.app
3. Despliegue automático
4. URL pública gratis

---

**Puerto expuesto:** 5000
**Acceso local:** http://localhost:5000
**Logs:** `docker-compose logs -f`
