from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class EstadoServicio(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADO = "confirmado"
    EN_PROGRESO = "en_progreso"
    COMPLETADO = "completado"
    CANCELADO = "cancelado"


class TipoServicio(str, Enum):
    CAMBIO_ACEITE = "cambio_aceite"
    CAMBIO_FILTRO = "cambio_filtro"
    ALINEACION = "alineacion"
    BALANCEO = "balanceo"
    MANTENIMIENTO_PREVENTIVO = "mantenimiento_preventivo"
    REPARACION = "reparacion"
    DIAGNOSTICO = "diagnostico"
    OTRO = "otro"


class Mecanico(BaseModel):
    id: str
    nombre: str
    especialidad: str
    experiencia_años: int
    calificacion_promedio: float = 4.5
    activo: bool = True


class TallerRegistro(BaseModel):
    nombre: str
    cedula_rif: str
    correo: str
    telefono: str
    direccion: str
    ciudad: str
    horario_apertura: str
    horario_cierre: str
    capacidad_simultaneas: int = 5


class Taller(BaseModel):
    id: str
    nombre: str
    cedula_rif: str
    correo: str
    telefono: str
    direccion: str
    ciudad: str
    latitud: float
    longitud: float
    horario_apertura: str
    horario_cierre: str
    capacidad_simultaneas: int
    mecanicos: List[Mecanico] = []
    calificacion_promedio: float = 4.5
    servicios_completados: int = 0
    fecha_registro: datetime
    activo: bool = True


class DetalleServicio(BaseModel):
    id: str
    tipo_servicio: TipoServicio
    descripcion: str
    precio_estimado: float
    tiempo_estimado_minutos: int
    fecha_creacion: datetime


class ServicioTaller(BaseModel):
    id: str
    usuario_id: str
    usuario_nombre: str
    vehiculo_id: str
    vehiculo_info: str
    taller_id: str
    mecanico_id: Optional[str] = None
    mecanico_nombre: Optional[str] = None
    servicios: List[DetalleServicio]
    estado: EstadoServicio = EstadoServicio.PENDIENTE
    fecha_cita: datetime
    hora_cita: str
    fecha_confirmacion: Optional[datetime] = None
    fecha_inicio: Optional[datetime] = None
    fecha_completacion: Optional[datetime] = None
    duracion_real_minutos: Optional[int] = None
    costo_final: Optional[float] = None
    notas_mecanico: Optional[str] = None
    calificacion_cliente: Optional[float] = None
    comentario_cliente: Optional[str] = None
    qr_code: Optional[str] = None


class ResumenTaller(BaseModel):
    id: str
    nombre: str
    ciudad: str
    servicios_pendientes: int
    servicios_en_progreso: int
    servicios_completados_hoy: int
    servicios_completados_total: int
    calificacion_promedio: float
    capacidad_disponible: int
    mecanicos_activos: int


class HistorialServicio(BaseModel):
    id: str
    usuario_nombre: str
    vehiculo_info: str
    tipo_servicio: TipoServicio
    fecha_completacion: datetime
    duracion_minutos: int
    costo: float
    calificacion: float
    comentario: Optional[str] = None
