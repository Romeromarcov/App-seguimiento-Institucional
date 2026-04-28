# Lubrikca MVP - Módulo Cliente/Usuario

## 📱 Descripción

MVP funcional del módulo **Cliente/Usuario** de la plataforma Lubrikca. Sistema de gestión de mantenimiento vehicular con:

✅ **Funcionalidades Implementadas:**
- Registro y perfil de usuario
- Registro de vehículos (marca, modelo, año, placa, lubricante, capacidad)
- Historial de kilometraje (updates cada 15 días)
- Recomendaciones automáticas de mantenimiento preventivo
- Solicitud de servicios en talleres
- Agendamiento de citas
- Escaneo de QR en taller
- Confirmación de servicios completados
- Sistema de créditos (50% en lubricante)
- Calificación de talleres
- Dashboard con resumen de estado

### 🔧 Stack Técnico
- **Backend:** FastAPI (Python)
- **Frontend:** HTML5 + Vanilla JavaScript
- **Storage:** En memoria (sin BD para esta fase MVP)
- **Despliegue:** Railway (listo)

---

## 🚀 Inicio Rápido Local

### Requisitos
- Python 3.9+
- pip

### 1. Clonar e instalar dependencias
```bash
git clone <tu-repo>
cd GestionCxC
pip install -r requirements.txt
```

### 2. Ejecutar servidor
```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. Abrir en navegador
- **Dashboard de administración:** http://localhost:8000/
- **App del cliente:** http://localhost:8000/cliente

---

## 📲 Uso de la App Cliente

### Usuario Demo
Para pruebas rápidas, usa el usuario predefinido:
- **ID:** `user-001`
- Vehículo asociado: Toyota Corolla 2020 (ABC-123)

### Flujo Principal del Usuario

#### 1️⃣ **Registro**
```
Login → Registrarse → Completar datos personales
```
- Nombre, cédula, email, teléfono, dirección, empresa
- Se genera automáticamente un ID de usuario único

#### 2️⃣ **Registrar Vehículos**
```
Dashboard → Vehículos → Agregar Vehículo
```
- Marca, modelo, año, placa
- Tipo de lubricante (sintético, semisintético, mineral)
- Capacidad en litros
- Kilometraje inicial

#### 3️⃣ **Historial de Kilometraje**
```
Dashboard → Vehículos → Detalles → Registrar Kilometraje
```
- Sistema solicita kilometraje cada 15 días (manuales en MVP)
- Genera automáticamente recomendaciones basadas en:
  - Ficha técnica del vehículo (marca/modelo)
  - Manual de fabricante
  - Componentes a mantener

#### 4️⃣ **Solicitar Servicio**
```
Dashboard → Citas → Solicitar Servicio
```
- Seleccionar vehículo
- Elegir tipo de servicio (cambio aceite, revisión, etc)
- Seleccionar fecha y hora
- Elegir taller más cercano
- Sistema calcula:
  - Costo estimado
  - Descuento del 50% en lubricante

#### 5️⃣ **En el Taller**
```
Cita activa → Escanear QR → Confirmar servicio
```
- Usuario escanea código QR en taller
- Sistema confirma inicio del servicio
- **Beneficio automático:** Crédito del 50% en lubricante se activa

#### 6️⃣ **Completar Servicio**
```
Servicio realizado → Calificar (1-5 estrellas)
```
- Confirmar que servicio fue recibido
- Calificación del taller (requerida)
- Comentarios opcionales
- **Crédito generado automáticamente** (visible en pestaña Créditos)

---

## 📊 Endpoints de API

### Usuarios
```
POST   /api/cliente/registro                 → Registrar usuario
GET    /api/cliente/perfil/{usuario_id}     → Obtener perfil completo
PUT    /api/cliente/ubicacion/{usuario_id}  → Actualizar GPS
GET    /api/cliente/resumen/{usuario_id}    → Resumen del estado
```

### Vehículos
```
POST   /api/cliente/vehiculos/{usuario_id}           → Registrar vehículo
GET    /api/cliente/vehiculos/{usuario_id}           → Listar vehículos
GET    /api/cliente/vehiculo/{vehiculo_id}           → Detalles vehículo
POST   /api/cliente/kilometraje/{usuario_id}/{veh_id} → Registrar KM
GET    /api/cliente/historial-kilometraje/{veh_id}   → Historial KM
```

### Recomendaciones
```
GET    /api/cliente/recomendaciones/{vehiculo_id}   → Obtener recomendaciones
```

### Servicios y Talleres
```
GET    /api/cliente/lubricantes          → Lubricantes disponibles
GET    /api/cliente/talleres             → Talleres disponibles
POST   /api/cliente/solicitar-servicio/{usuario_id}  → Solicitar servicio
GET    /api/cliente/mis-citas/{usuario_id}           → Listar citas
GET    /api/cliente/cita/{cita_id}                   → Detalles cita
POST   /api/cliente/confirmar-en-taller/{cita_id}   → Escanear QR
POST   /api/cliente/completar-servicio/{cita_id}    → Completar + calificar
POST   /api/cliente/cancelar-cita/{cita_id}         → Cancelar cita
```

### Créditos
```
GET    /api/cliente/mis-creditos/{usuario_id}  → Créditos disponibles
```

---

## 🗂️ Estructura del Proyecto

```
GestionCxC/
├── backend/
│   ├── main.py                          # Punto de entrada FastAPI
│   ├── models/
│   │   └── cliente.py                   # Modelos Pydantic (NEW)
│   ├── routers/
│   │   └── cliente.py                   # Endpoints API (NEW)
│   ├── services/
│   │   └── cliente_service.py           # Lógica de negocio (NEW)
│   └── requirements.txt
├── frontend/
│   ├── cliente.html                     # App del cliente (NEW)
│   ├── index.html                       # Dashboard admin
│   └── mobile.html                      # Vista móvil
├── MVP_CLIENTE_README.md                # Este archivo (NEW)
├── railway.json                         # Config para Railway
├── requirements.txt
├── run.sh                               # Script de arranque
└── .env.example
```

---

## 🌐 Datos Mockup

### Usuario Demo Incluido
- **ID:** user-001
- **Nombre:** Juan García
- **Empresa:** Tech Corp
- **Vehículo:** Toyota Corolla 2020

### Talleres Disponibles
1. Lubrikca Centro (Caracas)
2. Lubrikca Las Mercedes
3. Lubrikca Chacao

### Lubricantes Disponibles
- Castrol Edge 5W30 (Sintético) - $150.000/lt
- Mobil 1 0W20 (Sintético) - $160.000/lt
- Shell Helix 10W40 (Semisintético) - $100.000/lt
- Pennzoil 20W50 (Mineral) - $70.000/lt

### Planes de Mantenimiento
**Por marca (Toyota, Chevrolet, Ford):**
- Cambio de aceite: 10.000 km
- Cambio de filtro: 10.000 km
- Rotación de llantas: 15.000 km
- Inspección de frenos: 30.000 km
- Cambio de refrigerante: 80.000 km

---

## 🚀 Despliegue en Railway

### 1. Preparar repositorio
```bash
git add .
git commit -m "MVP Cliente/Usuario - Listo para Railway"
git push origin main
```

### 2. Conectar a Railway
1. Ir a https://railway.app
2. Crear nuevo proyecto
3. Conectar repositorio GitHub
4. Railway detectará automáticamente:
   - `requirements.txt`
   - `railway.json`
   - Comando de inicio

### 3. Variables de entorno (si necesarias)
```
# No requiere .env para el MVP
# Los datos son en memoria
```

### 4. El servidor estará en vivo en
```
https://tu-proyecto.railway.app/cliente
```

---

## 📝 Notas de Implementación

### ✅ Lo que funciona completamente:
- Flujos de usuario end-to-end
- Validaciones básicas
- Recomendaciones automáticas
- Generación de créditos
- Dashboard responsivo
- Sistema de ratings

### 🔄 Próximas Fases (No incluidas):
- Base de datos real (SQLite/PostgreSQL)
- Integración con Odoo 18
- Notificaciones por email/SMS
- Integración con Google Maps API
- Sistema de pagos
- Módulos: Taller, Empresa, Admin

### 💾 Datos Persistentes:
En el MVP actual, todos los datos están **en memoria**. Si reinicia el servidor, se pierden.
Para fase de producción, necesitará:
- Base de datos
- Sesiones persistentes
- Sistema de tokens JWT

---

## 🧪 Testing Manual

### Caso de Uso Completo:
1. Login con `user-001`
2. Ver dashboard → Estadísticas
3. Ir a "Vehículos" → Ver Toyota Corolla
4. Registrar kilometraje → Ver recomendaciones
5. "Solicitar Servicio" → Agendar cita
6. "Escanear QR" → Confirmar en taller
7. "Completar Servicio" → Calificar
8. Ver crédito otorgado en "Créditos"

### Caso: Registrar Nuevo Usuario
1. Click "Registrarse" en login
2. Completar formulario
3. Sistema genera ID automático
4. Agregar vehículos
5. Solicitar servicios

---

## 📞 Soporte

Para dudas sobre el MVP:
- Revisar modelos en `backend/models/cliente.py`
- API docs en `http://localhost:8000/docs` (Swagger)
- Frontend en `frontend/cliente.html`

---

## 📄 Licencia

Proyecto interno Lubrikca - 2026
