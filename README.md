# 🚗 App Seguimiento Institucional

**MVP - Módulo Cliente/Usuario**  
Plataforma de gestión de mantenimiento vehicular con sistema de créditos automáticos

---

## 📋 Descripción

MVP funcional de la aplicación **"App Seguimiento Institucional"** con enfoque en:

- 👤 **Usuarios/Clientes:** Registro, perfil, vehículos
- 🚗 **Vehículos:** Registrar múltiples, especificaciones técnicas
- 📊 **Mantenimiento Preventivo:** Recomendaciones automáticas por marca/modelo
- 📅 **Servicios:** Solicitar en talleres, agendar citas
- 🏪 **Talleres:** Seleccionar, calificar
- 💳 **Créditos:** Generación automática (50% en lubricante)
- ⭐ **Calificaciones:** Rating 1-5 estrellas

---

## 🚀 Inicio Rápido

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Ejecutar servidor
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Abrir en navegador
```
http://localhost:8000/cliente
```

**Usuario demo:** `user-001` (sin contraseña)

---

## 📁 Estructura del Proyecto

```
App seguimiento Institucional/
├── README.md                        ← Este archivo
├── QUICK_START.md                   ← Guía rápida
├── MVP_CLIENTE_README.md            ← Documentación completa
├── FLUJO_USUARIO.md                 ← Diagramas y flujos
├── EJEMPLOS_API.sh                  ← Ejemplos curl
├── DEPLOYMENT_CHECKLIST.md          ← Checklist deploy
│
├── requirements.txt                 ← Dependencias Python
├── railway.json                     ← Config Railway
├── .env.example                     ← Variables ejemplo
│
├── backend/
│   ├── main.py                      ← App FastAPI
│   ├── models/
│   │   └── cliente.py               ← Modelos Pydantic
│   ├── services/
│   │   └── cliente_service.py       ← Lógica negocio
│   └── routers/
│       └── cliente.py               ← 24 endpoints API
│
└── frontend/
    └── cliente.html                 ← App HTML5+JS (1500 líneas)
```

---

## 🔌 API REST (24 Endpoints)

### Usuarios (4)
- `POST /api/cliente/registro` - Registrar usuario
- `GET /api/cliente/perfil/{usuario_id}` - Obtener perfil
- `PUT /api/cliente/ubicacion/{usuario_id}` - Actualizar GPS
- `GET /api/cliente/resumen/{usuario_id}` - Resumen estado

### Vehículos (4)
- `POST /api/cliente/vehiculos/{usuario_id}` - Registrar vehículo
- `GET /api/cliente/vehiculos/{usuario_id}` - Listar vehículos
- `GET /api/cliente/vehiculo/{vehiculo_id}` - Detalles vehículo
- `POST /api/cliente/kilometraje/{usuario_id}/{veh_id}` - Registrar KM

### Mantenimiento (2)
- `GET /api/cliente/historial-kilometraje/{veh_id}` - Historial KM
- `GET /api/cliente/recomendaciones/{vehiculo_id}` - Recomendaciones

### Catálogos (2)
- `GET /api/cliente/lubricantes` - Lubricantes disponibles
- `GET /api/cliente/talleres` - Talleres disponibles

### Servicios & Citas (8)
- `POST /api/cliente/solicitar-servicio/{usuario_id}` - Solicitar servicio
- `GET /api/cliente/mis-citas/{usuario_id}` - Listar citas
- `GET /api/cliente/cita/{cita_id}` - Detalle cita
- `POST /api/cliente/confirmar-en-taller/{cita_id}` - Escanear QR
- `POST /api/cliente/completar-servicio/{cita_id}` - Completar + calificar
- `POST /api/cliente/cancelar-cita/{cita_id}` - Cancelar cita
- `GET /api/cliente/mis-creditos/{usuario_id}` - Ver créditos

---

## 🎨 Características de UI

✅ Responsive (móvil, tablet, desktop)  
✅ 4 tabs: Resumen, Vehículos, Citas, Créditos  
✅ Validación de formularios  
✅ Sistema de alertas  
✅ Animaciones suaves  
✅ Modales interactivos  
✅ Navegación intuitiva  
✅ Touch-friendly  

---

## 📊 Datos Mockup Incluidos

**Usuario Demo:**
- Nombre: Juan García
- Empresa: Tech Corp
- Vehículo: Toyota Corolla 2020

**Talleres:** 3 disponibles
- Lubrikca Centro
- Lubrikca Las Mercedes
- Lubrikca Chacao

**Lubricantes:** 4 tipos
- Castrol Edge 5W30
- Mobil 1 0W20
- Shell Helix 10W40
- Pennzoil 20W50

---

## 🚀 Desplegar en Railway

### Opción 1: CLI
```bash
npm install -g @railway/cli
railway login
cd "/c/Users/PC/Proyectos/App seguimiento Institucional"
railway up
```

### Opción 2: Dashboard
1. railway.app → New Project
2. Deploy from GitHub
3. Conectar repositorio
4. Listo en ~2 minutos

**URL en vivo:**
```
https://tu-proyecto.railway.app/cliente
```

---

## 📝 Documentación

- **QUICK_START.md** - Inicio en 60 segundos
- **MVP_CLIENTE_README.md** - Guía completa (120+ líneas)
- **FLUJO_USUARIO.md** - Diagramas detallados
- **EJEMPLOS_API.sh** - 19 ejemplos curl
- **DEPLOYMENT_CHECKLIST.md** - Checklist deploy

---

## ⚙️ Stack Técnico

- **Backend:** FastAPI (Python 3.9+)
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Storage:** En memoria (mockup)
- **Deploy:** Railway compatible

---

## 📋 Próximos Pasos (Fase 2)

- [ ] PostgreSQL real
- [ ] JWT autenticación
- [ ] Odoo 18 integración
- [ ] Módulo Taller
- [ ] Módulo Empresa
- [ ] Módulo Admin
- [ ] Notificaciones
- [ ] Google Maps
- [ ] Sistema de pagos

---

## 📞 Notas

- Este es un **MVP sin persistencia de datos** (en memoria)
- Sin autenticación real (demo mode)
- Sin integración Odoo
- **Listo para demostración** y testing
- **Producción requiere:** BD + Auth + Odoo

---

**Versión:** 1.0.0-MVP  
**Estado:** 🟢 Listo para deploy  
**Fecha:** 2026-04-28
