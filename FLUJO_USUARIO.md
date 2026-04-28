# 🔄 Flujo Completo del Usuario - MVP Cliente Lubrikca

## Diagrama de Flujos

```
┌─────────────────────────────────────────────────────────────────┐
│                    INICIO SESIÓN / REGISTRO                      │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────┴─────────┐
                    ↓                   ↓
            [LOGIN EXISTENTE]    [REGISTRO NUEVO]
                    │                   │
                    └─────────┬─────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                         DASHBOARD                                 │
│  ├─ 📊 Resumen (Vehículos, Citas, Créditos)                    │
│  ├─ 🚗 Vehículos (Ver, Agregar)                                │
│  ├─ 📅 Citas (Ver, Crear)                                      │
│  └─ 💳 Créditos (Ver disponibles)                              │
└─────────────────────────────────────────────────────────────────┘
                              ↓
            ┌─────────────────┼─────────────────┐
            ↓                 ↓                 ↓
      [VEHÍCULOS]       [SERVICIOS]        [CRÉDITOS]
            │                 │                 │
            ↓                 ↓                 ↓
       Registrar KM    Solicitar Servicio   Ver Balance


────────────────────────────────────────────────────────────────────
```

## 1️⃣ FLUJO: GESTIÓN DE VEHÍCULOS

```
┌─ Dashboard → Vehículos
│
├─ [Ver Vehículos Registrados]
│  │
│  ├─ Detalles del vehículo
│  │  ├─ Marca, Modelo, Año, Placa
│  │  ├─ Tipo Lubricante, Capacidad
│  │  ├─ KM Inicial registrado
│  │  │
│  │  └─ [Registrar Kilometraje] → Sistema valida KM > KM Inicial
│  │                               ↓
│  │                     Genera automáticamente
│  │                     Recomendaciones de Mantenimiento
│  │                               ↓
│  │                     [Mostrar Recomendaciones]
│  │                     ├─ Cambio Aceite
│  │                     ├─ Cambio Filtro
│  │                     ├─ Rotación Llantas
│  │                     ├─ Inspección Frenos
│  │                     └─ Cambio Refrigerante
│  │
│  └─ [Agregar Nuevo Vehículo]
│     │
│     └─ Formulario completo
│        ├─ Marca (Toyota, Chevrolet, Ford...)
│        ├─ Modelo
│        ├─ Año (validado 1990-2025)
│        ├─ Placa (formato libre)
│        ├─ Tipo Lubricante (sintético/semisintético/mineral)
│        ├─ Capacidad en litros
│        ├─ Kilometraje actual
│        └─ [Guardar] → Nuevo vehículo disponible
│
└─ (Repetible para N vehículos)

DATOS PERSISTIDOS EN MEMORIA:
  usuario.vehiculos = [Vehículo1, Vehículo2, ...]
  
RECOMENDACIONES AUTOMÁTICAS:
  - Base: Marca + Modelo
  - Planes predefinidos (Toyota, Chevrolet, Ford)
  - Se generan cuando KM actual > KM recomendado
  - Urgencia: "crítica" si KM > Recomendado * 1.2
```

---

## 2️⃣ FLUJO: SOLICITAR SERVICIO & CITA

```
┌─ Dashboard → Citas → [Solicitar Servicio]
│
├─ [1. Seleccionar Vehículo]
│  └─ Dropdown con todos los vehículos del usuario
│     └─ Muestra: Marca, Modelo, Placa, Lubricante
│
├─ [2. Seleccionar Tipo de Servicio]
│  └─ Opciones:
│     ├─ Cambio de Aceite (costo base: $200k)
│     ├─ Revisión General (costo base: $150k)
│     └─ Cambio de Filtro (costo base: $150k)
│
├─ [3. Seleccionar Fecha & Hora]
│  ├─ Date picker (mín. hoy)
│  └─ Time picker
│
├─ [4. Elegir Taller]
│  └─ Lista de talleres disponibles
│     ├─ Lubrikca Centro (Caracas)
│     ├─ Lubrikca Las Mercedes
│     └─ Lubrikca Chacao
│     └─ Cada taller muestra:
│        ├─ Dirección
│        └─ Calificación promedio (⭐⭐⭐⭐⭐)
│
├─ [5. Cálculo Automático]
│  ├─ Costo Base: $200.000 (ej: cambio aceite)
│  ├─ Descuento Lubricante 50%: -$21.000 (ej: 4.2 lts * $100k * 50%)
│  └─ TOTAL A PAGAR: $179.000
│
├─ [CONFIRMAR SOLICITUD]
│  └─ API: POST /solicitar-servicio
│     └─ Respuesta:
│        ├─ Cita ID generado
│        ├─ QR Code
│        ├─ Costo final
│        └─ Estado: PENDIENTE
│
└─ Cita guardada en sistema
   ├─ usuario.citas.add(ServicioCita)
   └─ Visible en "Mis Citas"

CÁLCULO DE CRÉDITO:
  Crédito 50% = (Litros vehículo × Precio lubricante base) × 0.5
  Ejemplo: 4.2 lt × $100.000 × 0.5 = $210.000 crédito potencial
```

---

## 3️⃣ FLUJO: EJECUCIÓN DEL SERVICIO EN TALLER

```
USUARIO LLEGA AL TALLER:

┌─ Cita en estado: PENDIENTE
│
├─ [Dashboard → Citas → Mi Cita]
│  └─ Ver QR Code (cadena única)
│     └─ Ejemplo: QR-cita-abc123-def456
│
├─ [ESCANEAR QR EN TALLER]
│  └─ Usuario hace click en "Escanear QR"
│     └─ Modal muestra el código
│     └─ Usuario valida con personal del taller
│
├─ [HE ESCANEADO EL QR]
│  └─ API: POST /confirmar-en-taller/{cita_id}
│     └─ Cambio de estado: PENDIENTE → EN_PROCESO
│     └─ ✅ CRÉDITO SE ACTIVA AUTOMÁTICAMENTE
│        (Usuario recibe 50% de descuento en lubricante)
│
├─ [SERVICIO EN PROCESO]
│  ├─ Personal del taller realiza el servicio
│  ├─ Aplica lubricante seleccionado
│  └─ Ejecuta otros servicios solicitados
│
├─ [SERVICIO COMPLETADO]
│  ├─ Usuario confirma que recibió el servicio
│  │  └─ API: POST /completar-servicio/{cita_id}
│  │
│  └─ Generación AUTOMÁTICA de Crédito
│     ├─ Sistema crea CreditoBeneficio
│     ├─ Monto = 50% del lubricante usado
│     ├─ Estado: DISPONIBLE
│     └─ Visible en pestaña "Créditos"
│
└─ Cita en estado: COMPLETADA

FLUJO DE CALIFICACIÓN (Obligatorio):
  Después de completar servicio
  ├─ Modal: "¿Cómo fue tu experiencia?"
  ├─ Rating 1-5 estrellas
  ├─ Comentarios opcionales
  └─ [Enviar Calificación]
     ├─ Se guarda en la cita
     └─ Afecta calificación promedio del taller
```

---

## 4️⃣ FLUJO: CRÉDITOS & BENEFICIOS

```
┌─ Dashboard → Créditos
│
├─ [CRÉDITOS DISPONIBLES]
│  └─ Listado de créditos no utilizados
│     ├─ Monto: $210.000 (ej)
│     ├─ Fecha Otorgado: 2026-04-28
│     └─ Estado: DISPONIBLE (verde)
│
├─ [CRÉDITOS UTILIZADOS]
│  └─ Listado de créditos ya aplicados
│     ├─ Monto: $150.000
│     └─ Estado: APLICADO (gris)
│
├─ GENERACIÓN AUTOMÁTICA:
│  └─ Se crean cuando servicio → COMPLETADA
│     └─ Monto = 50% de lubricante
│     └─ Asociado a Cita ID
│     └─ Vinculado a Usuario
│
└─ APLICACIÓN (Futura fase):
   ├─ Cuando usuario solicita próximo servicio
   ├─ Sistema detecta créditos disponibles
   └─ Descuenta automáticamente del total a pagar

BALANCE TOTAL:
  ┌─────────────────────────┐
  │ Total Crédito Disponible │ = Sum(Créditos donde aplicado = false)
  │                         │
  │  Ejemplo: $210k + $150k │
  │         = $360k         │
  └─────────────────────────┘
```

---

## 5️⃣ DIAGRAMA DE ESTADOS DE CITA

```
         ┌─────────────────────────────────────────┐
         │      CREACIÓN DE SOLICITUD              │
         │    (usuario solicita servicio)          │
         └──────────────────┬──────────────────────┘
                            │
                            ↓
                      ┌──────────────┐
                      │   PENDIENTE  │  ← Esperando confirmación usuario
                      └──┬───────┬───┘
                         │       │
              ┌──────────┘       └──────────┐
              ↓                             ↓
         [CANCELAR]                   [ESCANEAR QR]
              │                             │
              ↓                             ↓
         ┌──────────────┐            ┌──────────────┐
         │  CANCELADA   │            │ EN_PROCESO   │  ← Usuario en taller
         │ (sin crédito)│            │ (✅ crédito  │
         └──────────────┘            │    activo)   │
                                     └──┬───────────┘
                                        │
                                        ↓
                                 [COMPLETAR SERVICIO +
                                  CALIFICAR]
                                        │
                                        ↓
                                 ┌──────────────┐
                                 │ COMPLETADA   │  ← Servicio entregado
                                 │ ✅ Crédito   │
                                 │   generado   │
                                 └──────────────┘
```

---

## 📊 DATOS EJEMPLARES EN TRÁNSITO

### Ejemplo: Solicitud de Servicio
```json
{
  "usuario_id": "user-001",
  "vehiculo_id": "veh-001",
  "taller_id": "taller-001",
  "fecha_hora": "2026-05-01T14:00:00",
  "tipo_servicio": "cambio_aceite"
}
```

### Respuesta del Sistema
```json
{
  "status": "success",
  "cita_id": "cita-a1b2c3d4",
  "qr_code": "QR-cita-a1b2c3d4-xyz789",
  "costo_estimado": 200000,
  "descuento_credito_50pct": 210000,
  "monto_final": -10000
}
```

### Completar Servicio & Generar Crédito
```json
{
  "status": "success",
  "cita_id": "cita-a1b2c3d4",
  "estado": "completada",
  "calificacion": 5,
  "credito_otorgado": 210000,
  "mensaje": "Servicio completado. Crédito de $210.000 otorgado"
}
```

---

## 🔐 Validaciones en Flujos

| Flujo | Validación | Acción si Falla |
|-------|-----------|-----------------|
| Registrar KM | KM > KM_inicial | Error, rechaza |
| Solicitar Servicio | Todos campos completos | Error, no permite submit |
| Solicitar Servicio | Taller seleccionado | Error, destaca taller |
| Calificar | Rating 1-5 | Error, requiere calificación |
| Fecha/Hora | Mínimo hoy | Input desactiva fechas pasadas |

---

## 📱 Vista Responsive

- **Móvil (< 600px):** Layout single column, botones a ancho completo
- **Tablet:** Mismo layout, máx 500px de ancho
- **Desktop:** Centro de pantalla, máx 500px

---

Flujos diseñados para ser intuitivos y minimizar pasos del usuario. 🚀
