# ⚡ Inicio Rápido - App del Taller

## 1️⃣ Iniciar el Servidor

```bash
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 2️⃣ Acceder a la App

Abre tu navegador en:
```
http://localhost:8000/taller
```

## 3️⃣ Hacer Login

1. Selecciona un taller de la lista:
   - ✅ Taller Lubrikca Premium (recomendado)
   - ✅ Auto Servicio Total
2. Haz clic en "Ingresar"

## 4️⃣ Ver tu Dashboard

Verás:
- **📊 Estadísticas:** Citas pendientes, en progreso, completadas, capacidad
- **📋 4 Pestañas:** Citas Pendientes, Confirmadas, Mecánicos, Historial

## 5️⃣ Flujo Principal

### Confirmar una Cita
```
1. Abre "Citas Pendientes"
2. Selecciona una cita
3. Elige un mecánico
4. Haz clic en "Confirmar"
```

### Realizar un Servicio
```
1. Abre "Citas Confirmadas"
2. Haz clic en "Iniciar" cuando el mecánico empiece
3. Cuando termines, haz clic en "Completar"
4. Ingresa:
   - Duración real (minutos)
   - Costo final ($)
   - Notas del mecánico
```

### Agregar un Mecánico
```
1. Abre la pestaña "Mecánicos"
2. Haz clic en "+ Agregar Mecánico"
3. Completa los datos
4. Guarda
```

## 📊 Datos de Prueba

| Taller | ID | Mecánicos |
|--------|-----|-----------|
| **Lubrikca Premium** | taller-001 | 3 disponibles |
| **Auto Servicio** | taller-002 | 2 disponibles |

**Servicios para probar:**
- `srv-001` - Cambio de aceite (confirmado)
- `srv-002` - Diagnóstico (pendiente)

## 🧪 Probar API Directamente

```bash
# Ver todos los talleres
curl http://localhost:8000/api/taller/listar

# Ver resumen de un taller
curl http://localhost:8000/api/taller/taller-001/resumen

# Ver citas pendientes
curl http://localhost:8000/api/taller/taller-001/citas/pendientes

# Ver mecánicos
curl http://localhost:8000/api/taller/taller-001/mecanicos
```

## 📱 Caractéristicas

✅ Responsive (mobile, tablet, desktop)  
✅ Estados de citas en tiempo real  
✅ Cálculo automático de métricas  
✅ Sistema de calificaciones  
✅ Historial de servicios  
✅ Gestión de mecánicos  

## 🚀 Próximos Pasos

- [ ] Probar flujo completo de confirmación y completar servicio
- [ ] Revisar historial de servicios
- [ ] Agregar nuevos mecánicos
- [ ] Conectar con la app del Cliente
- [ ] Desplegar en Railway

¡Listo! 🎉 Ya puedes empezar a usar el panel del taller.
