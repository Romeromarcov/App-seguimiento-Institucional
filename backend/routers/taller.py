from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from typing import List, Optional
from models.taller import (
    Taller, TallerRegistro, ServicioTaller, Mecanico, ResumenTaller,
    HistorialServicio
)
from services.taller_service import TallerService

router = APIRouter(prefix="/api/taller", tags=["taller"])
service = TallerService()


# ==================== TALLERES ====================
@router.post("/registro", response_model=Taller)
async def registrar_taller(datos: TallerRegistro):
    """Registra un nuevo taller"""
    return service.registrar_taller(datos)


@router.get("/listar", response_model=List[Taller])
async def listar_talleres():
    """Lista todos los talleres disponibles"""
    return service.listar_talleres()


@router.get("/{taller_id}", response_model=Taller)
async def obtener_taller(taller_id: str):
    """Obtiene los datos de un taller específico"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return taller


@router.get("/{taller_id}/resumen", response_model=ResumenTaller)
async def obtener_resumen(taller_id: str):
    """Obtiene el resumen del estado del taller"""
    resumen = service.obtener_resumen(taller_id)
    if not resumen:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return resumen


# ==================== CITAS ====================
@router.get("/{taller_id}/citas/pendientes", response_model=List[ServicioTaller])
async def obtener_citas_pendientes(taller_id: str):
    """Obtiene todas las citas pendientes del taller"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return service.obtener_citas_pendientes(taller_id)


@router.get("/{taller_id}/citas/confirmadas", response_model=List[ServicioTaller])
async def obtener_citas_confirmadas(taller_id: str):
    """Obtiene todas las citas confirmadas del taller"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return service.obtener_citas_confirmadas(taller_id)


@router.get("/{taller_id}/citas/fecha", response_model=List[ServicioTaller])
async def obtener_citas_por_fecha(taller_id: str, fecha: str = Query(...)):
    """Obtiene las citas programadas para una fecha específica (YYYY-MM-DD)"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return service.obtener_servicios_por_fecha(taller_id, fecha)


@router.post("/{taller_id}/citas/{servicio_id}/confirmar", response_model=ServicioTaller)
async def confirmar_cita(taller_id: str, servicio_id: str, mecanico_id: str = Query(...)):
    """Confirma una cita y asigna un mecánico"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")

    resultado = service.confirmar_cita(servicio_id, mecanico_id)
    if not resultado:
        raise HTTPException(status_code=400, detail="No se pudo confirmar la cita")
    return resultado


@router.post("/{taller_id}/citas/{servicio_id}/iniciar", response_model=ServicioTaller)
async def iniciar_servicio(taller_id: str, servicio_id: str):
    """Inicia el servicio (mecánico comienza a trabajar)"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")

    resultado = service.iniciar_servicio(servicio_id)
    if not resultado:
        raise HTTPException(status_code=400, detail="No se pudo iniciar el servicio")
    return resultado


@router.post("/{taller_id}/citas/{servicio_id}/completar", response_model=ServicioTaller)
async def completar_servicio(
    taller_id: str,
    servicio_id: str,
    duracion_minutos: int = Query(...),
    costo_final: float = Query(...),
    notas: Optional[str] = None
):
    """Marca un servicio como completado"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")

    resultado = service.completar_servicio(
        servicio_id,
        duracion_minutos,
        costo_final,
        notas
    )
    if not resultado:
        raise HTTPException(status_code=400, detail="No se pudo completar el servicio")
    return resultado


@router.get("/{taller_id}/citas/{servicio_id}", response_model=ServicioTaller)
async def obtener_detalle_cita(taller_id: str, servicio_id: str):
    """Obtiene los detalles de una cita específica"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")

    servicio = service.obtener_servicio(servicio_id)
    if not servicio or servicio.taller_id != taller_id:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


# ==================== MECÁNICOS ====================
@router.get("/{taller_id}/mecanicos", response_model=List[Mecanico])
async def obtener_mecanicos(taller_id: str):
    """Obtiene la lista de mecánicos del taller"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return service.obtener_mecanicos(taller_id)


@router.post("/{taller_id}/mecanicos", response_model=Mecanico)
async def agregar_mecanico(taller_id: str, mecanico: Mecanico):
    """Agrega un nuevo mecánico al taller"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")

    resultado = service.agregar_mecanico(taller_id, mecanico)
    if not resultado:
        raise HTTPException(status_code=400, detail="No se pudo agregar el mecánico")
    return resultado


# ==================== HISTORIAL ====================
@router.get("/{taller_id}/historial", response_model=List[HistorialServicio])
async def obtener_historial(taller_id: str):
    """Obtiene el historial de servicios completados"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")
    return service.obtener_historial(taller_id)


# ==================== CALIFICACIONES ====================
@router.post("/{taller_id}/citas/{servicio_id}/calificar", response_model=ServicioTaller)
async def calificar_servicio(
    taller_id: str,
    servicio_id: str,
    calificacion: float = Query(...),
    comentario: Optional[str] = None
):
    """Actualiza la calificación de un servicio completado"""
    taller = service.obtener_taller(taller_id)
    if not taller:
        raise HTTPException(status_code=404, detail="Taller no encontrado")

    if calificacion < 1 or calificacion > 5:
        raise HTTPException(status_code=400, detail="Calificación debe estar entre 1 y 5")

    resultado = service.actualizar_calificacion(servicio_id, calificacion, comentario)
    if not resultado:
        raise HTTPException(status_code=400, detail="No se pudo actualizar la calificación")
    return resultado
