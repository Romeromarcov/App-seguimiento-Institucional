from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
from typing import List, Optional
from ..models.cliente import (
    UsuarioCliente, Vehiculo, DatosPersonales, ServicioCita,
    RecomendacionMantenimiento, CreditoBeneficio
)
from ..services.cliente_service import ClienteService

router = APIRouter(prefix="/api/cliente", tags=["cliente"])
service = ClienteService()

# Usuarios
@router.post("/registro", response_model=UsuarioCliente)
async def registrar_usuario(datos: DatosPersonales):
    """Registra un nuevo usuario cliente con sus datos personales"""
    return service.registrar_usuario(datos)

@router.get("/perfil/{usuario_id}", response_model=UsuarioCliente)
async def obtener_perfil(usuario_id: str):
    """Obtiene el perfil completo del usuario"""
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.put("/ubicacion/{usuario_id}")
async def actualizar_ubicacion(usuario_id: str, latitud: float, longitud: float):
    """Actualiza la ubicación GPS del usuario"""
    usuario = service.actualizar_ubicacion(usuario_id, latitud, longitud)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"status": "success", "usuario_id": usuario_id, "coordenadas": {"lat": latitud, "lng": longitud}}

# Vehículos
@router.post("/vehiculos/{usuario_id}", response_model=Vehiculo)
async def registrar_vehiculo(usuario_id: str, vehiculo: Vehiculo):
    """Registra un nuevo vehículo para el usuario"""
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return service.registrar_vehiculo(usuario_id, vehiculo)

@router.get("/vehiculos/{usuario_id}", response_model=List[Vehiculo])
async def obtener_vehiculos(usuario_id: str):
    """Obtiene los vehículos del usuario"""
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return service.obtener_vehiculos(usuario_id)

@router.get("/vehiculo/{vehiculo_id}", response_model=Vehiculo)
async def obtener_vehiculo(vehiculo_id: str):
    """Obtiene los detalles de un vehículo específico"""
    vehiculo = service.obtener_vehiculo(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo

# Kilometraje
@router.post("/kilometraje/{usuario_id}/{vehiculo_id}")
async def registrar_kilometraje(usuario_id: str, vehiculo_id: str, kilometraje: int):
    """Registra el kilometraje actual del vehículo"""
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    vehiculo = service.obtener_vehiculo(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    if kilometraje < vehiculo.kilometraje_inicial:
        raise HTTPException(status_code=400, detail="El kilometraje no puede ser menor al inicial")

    registro = service.registrar_kilometraje(usuario_id, vehiculo_id, kilometraje)
    return {"status": "success", "registro_id": registro.id, "kilometraje": kilometraje}

@router.get("/historial-kilometraje/{vehiculo_id}")
async def obtener_historial_kilometraje(vehiculo_id: str):
    """Obtiene el historial de kilometraje de un vehículo"""
    vehiculo = service.obtener_vehiculo(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    registros = service.obtener_historial_kilometraje(vehiculo_id)
    return {"vehiculo_id": vehiculo_id, "registros": registros, "total_registros": len(registros)}

# Recomendaciones de mantenimiento
@router.get("/recomendaciones/{vehiculo_id}", response_model=List[RecomendacionMantenimiento])
async def obtener_recomendaciones(vehiculo_id: str):
    """Obtiene las recomendaciones de mantenimiento para un vehículo"""
    vehiculo = service.obtener_vehiculo(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return service.obtener_recomendaciones(vehiculo_id)

# Lubricantes
@router.get("/lubricantes")
async def obtener_lubricantes():
    """Obtiene la lista de lubricantes disponibles"""
    return service.obtener_lubricantes()

# Talleres
@router.get("/talleres")
async def obtener_talleres():
    """Obtiene los talleres disponibles con su ubicación"""
    return service.obtener_talleres()

# Citas y Servicios
@router.post("/solicitar-servicio/{usuario_id}")
async def solicitar_servicio(usuario_id: str, vehiculo_id: str,
                            taller_id: str, fecha_hora: str,
                            tipo_servicio: str = "cambio_aceite"):
    """Solicita un servicio en un taller específico"""
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    vehiculo = service.obtener_vehiculo(vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")

    try:
        fecha_dt = datetime.fromisoformat(fecha_hora)
    except ValueError:
        raise HTTPException(status_code=400, detail="Formato de fecha inválido (ISO 8601)")

    cita = service.solicitar_servicio(usuario_id, vehiculo_id, taller_id, fecha_dt, tipo_servicio)
    return {
        "status": "success",
        "cita_id": cita.id,
        "qr_code": cita.qr_code,
        "costo_estimado": cita.costo_estimado,
        "descuento_credito_50pct": cita.descuento_credito_50pct,
        "monto_final": cita.costo_estimado - cita.descuento_credito_50pct
    }

@router.get("/mis-citas/{usuario_id}")
async def obtener_mis_citas(usuario_id: str):
    """Obtiene todas las citas del usuario"""
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    citas = service.obtener_citas_usuario(usuario_id)
    return {
        "usuario_id": usuario_id,
        "citas": citas,
        "total_citas": len(citas),
        "citas_pendientes": len([c for c in citas if c.estado == "pendiente"]),
        "citas_confirmadas": len([c for c in citas if c.estado == "confirmada"])
    }

@router.get("/cita/{cita_id}", response_model=ServicioCita)
async def obtener_cita(cita_id: str):
    """Obtiene los detalles de una cita específica"""
    cita = service.obtener_cita(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    return cita

@router.post("/confirmar-en-taller/{cita_id}")
async def confirmar_servicio_en_taller(cita_id: str):
    """Confirma que el servicio comienza (usuario escanea QR en taller)"""
    cita = service.obtener_cita(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    cita_actualizada = service.confirmar_servicio_en_taller(cita_id)
    return {
        "status": "success",
        "cita_id": cita_id,
        "estado": cita_actualizada.estado,
        "mensaje": "Servicio iniciado. Recibiendo beneficio de crédito del 50% en lubricante"
    }

@router.post("/completar-servicio/{cita_id}")
async def completar_servicio(cita_id: str, calificacion: int = 5, comentario: str = ""):
    """Completa el servicio y genera el crédito automáticamente"""
    if not 1 <= calificacion <= 5:
        raise HTTPException(status_code=400, detail="La calificación debe estar entre 1 y 5")

    cita = service.obtener_cita(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    cita_actualizada = service.completar_servicio(cita_id, calificacion, comentario)
    return {
        "status": "success",
        "cita_id": cita_id,
        "estado": cita_actualizada.estado,
        "calificacion": calificacion,
        "credito_otorgado": cita_actualizada.descuento_credito_50pct,
        "mensaje": f"Servicio completado. Crédito de ${cita_actualizada.descuento_credito_50pct:,} otorgado"
    }

@router.post("/cancelar-cita/{cita_id}")
async def cancelar_cita(cita_id: str):
    """Cancela una cita pendiente"""
    cita = service.obtener_cita(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")

    if cita.estado != "pendiente":
        raise HTTPException(status_code=400, detail="Solo se pueden cancelar citas pendientes")

    cita_actualizada = service.cancelar_cita(cita_id)
    return {
        "status": "success",
        "cita_id": cita_id,
        "estado": cita_actualizada.estado
    }

# Créditos
@router.get("/mis-creditos/{usuario_id}", response_model=List[CreditoBeneficio])
async def obtener_mis_creditos(usuario_id: str):
    """Obtiene todos los créditos disponibles del usuario"""
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    creditos = service.obtener_creditos(usuario_id)
    total_credito = sum(c.monto_credito for c in creditos if not c.aplicado)
    return creditos

@router.get("/resumen/{usuario_id}")
async def obtener_resumen(usuario_id: str):
    """Obtiene un resumen del estado del usuario"""
    usuario = service.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    vehiculos = service.obtener_vehiculos(usuario_id)
    citas = service.obtener_citas_usuario(usuario_id)
    creditos = service.obtener_creditos(usuario_id)
    total_credito_disponible = sum(c.monto_credito for c in creditos if not c.aplicado)

    return {
        "usuario_id": usuario_id,
        "nombre": usuario.datos_personales.nombre,
        "empresa": usuario.datos_personales.empresa,
        "total_vehiculos": len(vehiculos),
        "total_citas": len(citas),
        "citas_activas": len([c for c in citas if c.estado in ["pendiente", "confirmada", "en_proceso"]]),
        "total_credito_disponible": total_credito_disponible,
        "gps_activo": usuario.gps_activo
    }
