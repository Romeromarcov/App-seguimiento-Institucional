# 🏢 Módulo del Taller - Lubrikca

## Descripción General

El módulo del Taller es la aplicación que permite a los talleres mecánicos (workshops) gestionar citas de servicio, asignar mecánicos, y registrar servicios completados con sus costos y duraciones.

## Funcionalidades Principales

### 1. **Autenticación**
- Login con selección de taller
- Dos talleres de prueba disponibles:
  - Taller Lubrikca Premium (taller-001)
  - Auto Servicio Total (taller-002)

### 2. **Dashboard**
- Resumen de estado del taller
- 4 estadísticas principales:
  - Citas pendientes
  - Servicios en progreso
  - Servicios completados hoy
  - Capacidad disponible

### 3. **Gestión de Citas**

#### Citas Pendientes
- Ver todas las citas sin confirmar
- Información del cliente y vehículo
- Seleccionar mecánico y confirmar
- Ver detalles completos de la cita

#### Citas Confirmadas
- Listar citas confirmadas y en progreso
- Iniciar servicio (cambiar estado a "en progreso")
- Completar servicio con:
  - Duración en minutos
  - Costo final
  - Notas del mecánico

### 4. **Gestión de Mecánicos**
- Ver lista de mecánicos disponibles
- Información: nombre, especialidad, experiencia, calificación
- Agregar nuevos mecánicos

### 5. **Historial de Servicios**
- Ver servicios completados
- Información: cliente, vehículo, tipo de servicio, fecha, duración, costo
- Calificación del cliente

## Endpoints de API

### Talleres
```
GET    /api/taller/listar              - Listar todos los talleres
GET    /api/taller/{taller_id}         - Obtener datos del taller
GET    /api/taller/{taller_id}/resumen - Obtener resumen del estado
```

### Citas
```
GET    /api/taller/{taller_id}/citas/pendientes    - Citas sin confirmar
GET    /api/taller/{taller_id}/citas/confirmadas   - Citas confirmadas/en progreso
GET    /api/taller/{taller_id}/citas/fecha         - Citas por fecha (YYYY-MM-DD)
GET    /api/taller/{taller_id}/citas/{servicio_id} - Detalles de una cita

POST   /api/taller/{taller_id}/citas/{servicio_id}/confirmar    - Confirmar cita
POST   /api/taller/{taller_id}/citas/{servicio_id}/iniciar      - Iniciar servicio
POST   /api/taller/{taller_id}/citas/{servicio_id}/completar    - Completar servicio
POST   /api/taller/{taller_id}/citas/{servicio_id}/calificar    - Actualizar calificación
```

### Mecánicos
```
GET    /api/taller/{taller_id}/mecanicos         - Listar mecánicos
POST   /api/taller/{taller_id}/mecanicos         - Agregar mecánico
```

### Historial
```
GET    /api/taller/{taller_id}/historial         - Ver servicios completados
```

## Flujo de Trabajo

### 1. Confirmar una Cita
```
1. El cliente solicita un servicio desde la app Cliente
2. Aparece en "Citas Pendientes"
3. El taller selecciona un mecánico
4. El estado cambia a "Confirmado"
```

### 2. Realizar el Servicio
```
1. El mecánico ve la cita en "Citas Confirmadas"
2. Hace clic en "Iniciar" para comenzar el trabajo
3. El estado cambia a "En Progreso"
```

### 3. Completar el Servicio
```
1. El mecánico ingresa:
   - Duración real del servicio (minutos)
   - Costo final del servicio ($)
   - Notas sobre lo realizado
2. El servicio se marca como "Completado"
3. Se agrega al historial
```

### 4. Evaluación
```
1. El cliente recibe una notificación
2. El cliente califica el servicio (1-5 estrellas)
3. La calificación se registra y afecta el promedio del taller
```

## Datos de Prueba

### Taller 1 - Lubrikca Premium
- **ID:** taller-001
- **Mecánicos:** Carlos López, Pedro Martínez, Luis González
- **Calificación:** 4.8 ⭐
- **Capacidad:** 5 servicios simultáneos

### Taller 2 - Auto Servicio Total
- **ID:** taller-002
- **Mecánicos:** Roberto Fernández, Miguel Rodríguez
- **Calificación:** 4.6 ⭐
- **Capacidad:** 3 servicios simultáneos

### Citas de Prueba
- **srv-001:** Cambio de aceite - Confirmado
- **srv-002:** Diagnóstico - Pendiente

## Estados de un Servicio

| Estado | Descripción |
|--------|-------------|
| `pendiente` | Cita solicitada, sin confirmar |
| `confirmado` | Mecánico asignado |
| `en_progreso` | El mecánico está trabajando |
| `completado` | Servicio finalizado |
| `cancelado` | Cita cancelada |

## Interfaz de Usuario

### Vista Mobile (< 600px)
- Diseño responsive con una columna
- Navegación por pestañas simplificada
- Botones grandes y fáciles de tocar

### Vista Tablet (600px - 1024px)
- Grid de 2 columnas para estadísticas
- Tabs horizontales completos

### Vista Desktop (> 1024px)
- Grid completo de estadísticas
- Mejor distribución de espacios
- Tablas para historial

## Colores y Estilos

- **Primario:** Gradiente #667eea → #764ba2 (Púrpura)
- **Estados:**
  - Pendiente: Amarillo (#fff3cd)
  - Confirmado: Azul claro (#d1ecf1)
  - En Progreso: Azul (#cfe2ff)
  - Completado: Verde (#d1e7dd)

## Próximas Mejoras

- [ ] Sistema de notificaciones en tiempo real
- [ ] Integración con GPS para ubicación de clientes
- [ ] Reportes de rendimiento del taller
- [ ] Sistema de disponibilidad de mecánicos
- [ ] Chat con clientes
- [ ] Facturación integrada
- [ ] Integración con Odoo 18

## Iniciar Servidor

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Luego accede a:
- **App del Cliente:** http://localhost:8000/
- **App del Taller:** http://localhost:8000/taller
- **API Docs:** http://localhost:8000/docs

## Archivos Principales

- `backend/models/taller.py` - Modelos Pydantic
- `backend/services/taller_service.py` - Lógica de negocio
- `backend/routers/taller.py` - Endpoints API
- `frontend/taller.html` - Interfaz web
