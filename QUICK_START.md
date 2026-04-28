# 🚀 Quick Start - MVP Cliente Lubrikca

## 60 segundos para empezar

### 1. Instalar
```bash
pip install -r requirements.txt
```

### 2. Ejecutar
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Abrir
- **App del Cliente:** http://localhost:8000/cliente
- **API Docs:** http://localhost:8000/docs
- **Admin:** http://localhost:8000/

---

## 🎮 Demo Inmediata

### Usuario Predefinido
```
ID: user-001
(Sin contraseña necesaria en MVP)
```

### Qué Puedes Hacer:
1. ✅ Ver vehículo registrado (Toyota Corolla)
2. ✅ Registrar kilometraje
3. ✅ Ver recomendaciones automáticas
4. ✅ Solicitar servicio en taller
5. ✅ Agendar cita
6. ✅ Escanear QR ficticio
7. ✅ Calificar servicio
8. ✅ Ganar crédito (50% en lubricante)
9. ✅ Ver créditos disponibles

---

## 📁 Archivos Nuevos

```
backend/
├── models/cliente.py          ← Modelos de datos
├── routers/cliente.py         ← Endpoints API  
└── services/cliente_service.py ← Lógica negocio

frontend/
└── cliente.html               ← App completa (UI+JS)
```

---

## 🔌 API Principal

```bash
# Registrar usuario
curl -X POST http://localhost:8000/api/cliente/registro \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Test","cedula":"123","correo":"test@test.com","telefono":"+58","direccion":"Calle 1","empresa":"Corp"}'

# Obtener perfil
curl http://localhost:8000/api/cliente/perfil/user-001

# Listar vehículos
curl http://localhost:8000/api/cliente/vehiculos/user-001

# Obtener talleres
curl http://localhost:8000/api/cliente/talleres

# Solicitar servicio
curl -X POST http://localhost:8000/api/cliente/solicitar-servicio/user-001 \
  -G --data-urlencode 'vehiculo_id=veh-001' \
  --data-urlencode 'taller_id=taller-001' \
  --data-urlencode 'fecha_hora=2026-05-01T14:00:00' \
  --data-urlencode 'tipo_servicio=cambio_aceite'
```

---

## 🌐 Deploy en Railway

### Opción 1: Desde CLI (recomendado)
```bash
npm install -g @railway/cli
railway login
railway up
```

### Opción 2: Desde Dashboard
1. https://railway.app → New Project
2. Deploy from GitHub → Conectar repo
3. Listo ✓

### URL en vivo
```
https://tu-proyecto.railway.app/cliente
```

---

## 🔄 Próximos Pasos

Para pasar a producción:
- [ ] Conectar base de datos real (PostgreSQL)
- [ ] Implementar autenticación JWT
- [ ] Integrar con Odoo 18
- [ ] Módulos: Taller, Empresa, Admin
- [ ] Notificaciones (email/SMS)
- [ ] Google Maps API

---

## ⚠️ Limitaciones MVP

- Datos **en memoria** (se pierden al reiniciar)
- Sin persistencia de sesiones
- Talleres, lubricantes, recomendaciones hardcodeados
- Sin autenticación real
- Sin integración Odoo

---

Más detalles: Ver `MVP_CLIENTE_README.md`
