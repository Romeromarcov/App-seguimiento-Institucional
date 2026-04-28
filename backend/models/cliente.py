from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class TipoLubricante(str, Enum):
    SINTETICO = "sintético"
    SEMISINTETICO = "semisintético"
    MINERAL = "mineral"

class Vehiculo(BaseModel):
    id: Optional[str] = None
    marca: str
    modelo: str
    año: int
    placa: str
    tipo_lubricante: TipoLubricante
    litros_capacidad: float
    kilometraje_inicial: int
    fecha_registro: Optional[datetime] = None

class RegistroKilometraje(BaseModel):
    id: Optional[str] = None
    vehiculo_id: str
    kilometraje: int
    fecha: Optional[datetime] = None

class DatosPersonales(BaseModel):
    nombre: str
    cedula: str
    correo: str
    telefono: str
    direccion: str
    empresa: str

class UsuarioCliente(BaseModel):
    id: Optional[str] = None
    datos_personales: DatosPersonales
    vehiculos: List[Vehiculo] = []
    gps_activo: bool = True
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    fecha_registro: Optional[datetime] = None
    activo: bool = True

class EstadoCita(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    EN_PROCESO = "en_proceso"
    COMPLETADA = "completada"
    CANCELADA = "cancelada"

class Taller(BaseModel):
    id: str
    nombre: str
    direccion: str
    latitud: float
    longitud: float
    calificacion_promedio: float = 4.5

class ServicioCita(BaseModel):
    id: Optional[str] = None
    usuario_id: str
    vehiculo_id: str
    taller_id: str
    fecha_hora: datetime
    tipo_servicio: str
    estado: EstadoCita = EstadoCita.PENDIENTE
    costo_estimado: float
    descuento_credito_50pct: float = 0
    qr_code: Optional[str] = None
    calificacion_taller: Optional[int] = None
    comentario: Optional[str] = None
    fecha_creacion: Optional[datetime] = None

class RecomendacionMantenimiento(BaseModel):
    id: Optional[str] = None
    vehiculo_id: str
    tipo: str
    componente: str
    kilometraje_recomendado: int
    kilometraje_actual: int
    estado: str
    urgencia: str

class CreditoBeneficio(BaseModel):
    id: Optional[str] = None
    usuario_id: str
    cita_id: str
    monto_lubricante: float
    porcentaje_descuento: float = 50
    monto_credito: float
    fecha_otorgado: Optional[datetime] = None
    aplicado: bool = False
