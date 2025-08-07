# PCLagos - Sistema de Gestión de Servicios

Sistema web para gestión de servicios de reparación de computadoras con chat en tiempo real, códigos QR y seguimiento de estado.

## 🚀 Características

- ✅ **Gestión de servicios** con códigos únicos
- ✅ **Chat en tiempo real** entre cliente y técnico
- ✅ **Códigos QR** para acceso móvil
- ✅ **Notas de reparación** con fechas manuales
- ✅ **Seguimiento de estado** (Pendiente, En Progreso, Completado, Cancelado)
- ✅ **Interfaz responsive** con Bootstrap 5
- ✅ **Panel de administración** personalizado

## 🛠️ Instalación Local

### Requisitos
- Python 3.11+
- pip

### Pasos

1. **Clonar el repositorio:**
```bash
git clone https://github.com/TU_USUARIO/pclagos.git
cd pclagos
```

2. **Crear entorno virtual:**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

6. **Ejecutar servidor:**
```bash
python manage.py runserver
```

7. **Abrir en navegador:**
```
http://localhost:8000
```

## 🌐 Despliegue en Render (Gratis)

### Pasos:

1. **Subir a GitHub:**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Crear cuenta en [Render.com](https://render.com)**

3. **Conectar GitHub y crear Web Service**

4. **Configuración:**
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn pc_repair.wsgi:application`
   - **Plan**: Free

5. **Variables de entorno:**
   - `DEBUG`: `False`
   - `SITE_URL`: `https://tu-app.onrender.com`

## 📁 Estructura del Proyecto

```
pclagos/
├── contact/          # App principal de servicios
├── core/            # App de páginas principales
├── services/        # App de servicios ofrecidos
├── gallery/         # App de galería
├── templates/       # Templates HTML
├── static/          # Archivos estáticos
├── media/           # Archivos subidos
└── pc_repair/       # Configuración del proyecto
```

## 🔧 Comandos Útiles

```bash
# Limpiar servicios existentes
python manage.py clear_services --confirm

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Recolectar archivos estáticos
python manage.py collectstatic
```

## 📱 Funcionalidades

### Para Clientes:
- Solicitar servicios con formulario
- Recibir código único con QR
- Consultar estado del servicio
- Chat en tiempo real con técnico
- Ver notas de reparación

### Para Técnicos:
- Panel de administración
- Gestión de servicios
- Chat con clientes
- Agregar notas de reparación
- Cambiar estado de servicios

## 🎨 Tecnologías

- **Backend**: Django 5.2.4
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Base de datos**: SQLite (desarrollo) / PostgreSQL (producción)
- **Servidor**: Gunicorn
- **QR Codes**: qrcode + Pillow
- **Forms**: Django Crispy Forms

## 📄 Licencia

Este proyecto es de uso libre para fines educativos y comerciales.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📞 Contacto

Para soporte técnico o consultas:
- Email: tu-email@ejemplo.com
- WhatsApp: +54 9 3402 556984 