import uuid
from datetime import datetime, timedelta
from typing import List, Optional, Dict
from models.taller import (
    Taller, ServicioTaller, TallerRegistro, Mecanico, DetalleServicio,
    ResumenTaller, HistorialServicio, EstadoServicio, TipoServicio
)


class TallerService:
    def __init__(self):
        self.talleres = {}
        self.servicios = {}
        self.mecanicos = {}
        self._init_datos_mockup()

    def _init_datos_mockup(self):
        """Inicializa datos de prueba"""
        # Taller 1
        taller1_id = "taller-001"
        mecanicos_t1 = [
            Mecanico(
                id="mec-001",
                nombre="Carlos López",
                especialidad="Cambios de aceite y filtros",
                experiencia_años=8,
                calificacion_promedio=4.8
            ),
            Mecanico(
                id="mec-002",
                nombre="Pedro Martínez",
                especialidad="Reparaciones mayores",
                experiencia_años=12,
                calificacion_promedio=4.9
            ),
            Mecanico(
                id="mec-003",
                nombre="Luis González",
                especialidad="Diagnóstico y alineación",
                experiencia_años=6,
                calificacion_promedio=4.6
            )
        ]

        for mecanico in mecanicos_t1:
            self.mecanicos[mecanico.id] = mecanico

        self.talleres[taller1_id] = Taller(
            id=taller1_id,
            nombre="Taller Lubrikca Premium",
            cedula_rif="J-29345678",
            correo="taller.premium@lubrikca.com",
            telefono="+58-212-1234567",
            direccion="Av. Francisco de Miranda, Edificio A, Piso 3",
            ciudad="Caracas",
            latitud=10.4920,
            longitud=-66.8552,
            horario_apertura="07:00",
            horario_cierre="18:00",
            capacidad_simultaneas=5,
            mecanicos=mecanicos_t1,
            calificacion_promedio=4.8,
            servicios_completados=127,
            fecha_registro=datetime.now() - timedelta(days=180),
            activo=True
        )

        # Taller 2
        taller2_id = "taller-002"
        mecanicos_t2 = [
            Mecanico(
                id="mec-004",
                nombre="Roberto Fernández",
                especialidad="Mantenimiento preventivo",
                experiencia_años=10,
                calificacion_promedio=4.7
            ),
            Mecanico(
                id="mec-005",
                nombre="Miguel Rodríguez",
                especialidad="Suspensión y frenos",
                experiencia_años=9,
                calificacion_promedio=4.5
            )
        ]

        for mecanico in mecanicos_t2:
            self.mecanicos[mecanico.id] = mecanico

        self.talleres[taller2_id] = Taller(
            id=taller2_id,
            nombre="Auto Servicio Total",
            cedula_rif="J-31456789",
            correo="info@autoservicio.com",
            telefono="+58-212-9876543",
            direccion="Calle Bolívar, Centro Comercial El Solar",
            ciudad="Caracas",
            latitud=10.5030,
            longitud=-66.9000,
            horario_apertura="08:00",
            horario_cierre="17:00",
            capacidad_simultaneas=3,
            mecanicos=mecanicos_t2,
            calificacion_promedio=4.6,
            servicios_completados=89,
            fecha_registro=datetime.now() - timedelta(days=240),
            activo=True
        )

        # Servicios de prueba
        self.servicios["srv-001"] = ServicioTaller(
            id="srv-001",
            usuario_id="user-001",
            usuario_nombre="Juan García",
            vehiculo_id="veh-001",
            vehiculo_info="Toyota Corolla 2020 - ABC-123",
            taller_id=taller1_id,
            mecanico_id="mec-001",
            mecanico_nombre="Carlos López",
            servicios=[
                DetalleServicio(
                    id="det-001",
                    tipo_servicio=TipoServicio.CAMBIO_ACEITE,
                    descripcion="Cambio de aceite sinténtico 5W-30",
                    precio_estimado=45.00,
                    tiempo_estimado_minutos=30,
                    fecha_creacion=datetime.now() - timedelta(days=1)
                )
            ],
            estado=EstadoServicio.CONFIRMADO,
            fecha_cita=datetime.now() + timedelta(days=2),
            hora_cita="09:00",
            fecha_confirmacion=datetime.now() - timedelta(hours=2),
            qr_code="QR-srv-001"
        )

        self.servicios["srv-002"] = ServicioTaller(
            id="srv-002",
            usuario_id="user-001",
            usuario_nombre="Juan García",
            vehiculo_id="veh-001",
            vehiculo_info="Toyota Corolla 2020 - ABC-123",
            taller_id=taller1_id,
            mecanico_id=None,
            mecanico_nombre=None,
            servicios=[
                DetalleServicio(
                    id="det-002",
                    tipo_servicio=TipoServicio.DIAGNOSTICO,
                    descripcion="Diagnóstico general del vehículo",
                    precio_estimado=30.00,
                    tiempo_estimado_minutos=45,
                    fecha_creacion=datetime.now()
                )
            ],
            estado=EstadoServicio.PENDIENTE,
            fecha_cita=datetime.now() + timedelta(days=3),
            hora_cita="14:00",
            qr_code="QR-srv-002"
        )

    def registrar_taller(self, datos: TallerRegistro) -> Taller:
        """Registra un nuevo taller"""
        taller_id = f"taller-{str(uuid.uuid4())[:8]}"
        taller = Taller(
            id=taller_id,
            nombre=datos.nombre,
            cedula_rif=datos.cedula_rif,
            correo=datos.correo,
            telefono=datos.telefono,
            direccion=datos.direccion,
            ciudad=datos.ciudad,
            latitud=0.0,
            longitud=0.0,
            horario_apertura=datos.horario_apertura,
            horario_cierre=datos.horario_cierre,
            capacidad_simultaneas=datos.capacidad_simultaneas,
            mecanicos=[],
            fecha_registro=datetime.now(),
            activo=True
        )
        self.talleres[taller_id] = taller
        return taller

    def obtener_taller(self, taller_id: str) -> Optional[Taller]:
        """Obtiene un taller por ID"""
        return self.talleres.get(taller_id)

    def listar_talleres(self) -> List[Taller]:
        """Lista todos los talleres activos"""
        return [t for t in self.talleres.values() if t.activo]

    def obtener_resumen(self, taller_id: str) -> Optional[ResumenTaller]:
        """Obtiene el resumen del estado del taller"""
        taller = self.obtener_taller(taller_id)
        if not taller:
            return None

        servicios_pendientes = sum(
            1 for s in self.servicios.values()
            if s.taller_id == taller_id and s.estado == EstadoServicio.PENDIENTE
        )
        servicios_en_progreso = sum(
            1 for s in self.servicios.values()
            if s.taller_id == taller_id and s.estado == EstadoServicio.EN_PROGRESO
        )
        servicios_completados_hoy = sum(
            1 for s in self.servicios.values()
            if s.taller_id == taller_id
            and s.estado == EstadoServicio.COMPLETADO
            and s.fecha_completacion
            and s.fecha_completacion.date() == datetime.now().date()
        )

        mecanicos_activos = sum(1 for m in taller.mecanicos if m.activo)

        return ResumenTaller(
            id=taller.id,
            nombre=taller.nombre,
            ciudad=taller.ciudad,
            servicios_pendientes=servicios_pendientes,
            servicios_en_progreso=servicios_en_progreso,
            servicios_completados_hoy=servicios_completados_hoy,
            servicios_completados_total=taller.servicios_completados,
            calificacion_promedio=taller.calificacion_promedio,
            capacidad_disponible=taller.capacidad_simultaneas - servicios_en_progreso,
            mecanicos_activos=mecanicos_activos
        )

    def obtener_citas_pendientes(self, taller_id: str) -> List[ServicioTaller]:
        """Obtiene todas las citas pendientes del taller"""
        return [
            s for s in self.servicios.values()
            if s.taller_id == taller_id and s.estado == EstadoServicio.PENDIENTE
        ]

    def obtener_citas_confirmadas(self, taller_id: str) -> List[ServicioTaller]:
        """Obtiene todas las citas confirmadas del taller"""
        return [
            s for s in self.servicios.values()
            if s.taller_id == taller_id
            and s.estado in [EstadoServicio.CONFIRMADO, EstadoServicio.EN_PROGRESO]
        ]

    def confirmar_cita(self, servicio_id: str, mecanico_id: str) -> Optional[ServicioTaller]:
        """Confirma una cita y asigna un mecánico"""
        servicio = self.servicios.get(servicio_id)
        if not servicio:
            return None

        mecanico = self.mecanicos.get(mecanico_id)
        if not mecanico:
            return None

        servicio.estado = EstadoServicio.CONFIRMADO
        servicio.mecanico_id = mecanico_id
        servicio.mecanico_nombre = mecanico.nombre
        servicio.fecha_confirmacion = datetime.now()
        self.servicios[servicio_id] = servicio
        return servicio

    def iniciar_servicio(self, servicio_id: str) -> Optional[ServicioTaller]:
        """Inicia el servicio (mecánico comienza a trabajar)"""
        servicio = self.servicios.get(servicio_id)
        if not servicio:
            return None

        servicio.estado = EstadoServicio.EN_PROGRESO
        servicio.fecha_inicio = datetime.now()
        self.servicios[servicio_id] = servicio
        return servicio

    def completar_servicio(
        self,
        servicio_id: str,
        duracion_minutos: int,
        costo_final: float,
        notas: Optional[str] = None
    ) -> Optional[ServicioTaller]:
        """Completa un servicio"""
        servicio = self.servicios.get(servicio_id)
        if not servicio:
            return None

        servicio.estado = EstadoServicio.COMPLETADO
        servicio.fecha_completacion = datetime.now()
        servicio.duracion_real_minutos = duracion_minutos
        servicio.costo_final = costo_final
        servicio.notas_mecanico = notas

        # Actualizar estadísticas del taller
        taller = self.talleres.get(servicio.taller_id)
        if taller:
            taller.servicios_completados += 1
            self.talleres[servicio.taller_id] = taller

        self.servicios[servicio_id] = servicio
        return servicio

    def obtener_historial(self, taller_id: str) -> List[HistorialServicio]:
        """Obtiene el historial de servicios completados"""
        historial = []
        for servicio in self.servicios.values():
            if (servicio.taller_id == taller_id
                and servicio.estado == EstadoServicio.COMPLETADO
                and servicio.fecha_completacion):

                servicio_info = servicio.servicios[0] if servicio.servicios else None
                historial.append(
                    HistorialServicio(
                        id=servicio.id,
                        usuario_nombre=servicio.usuario_nombre,
                        vehiculo_info=servicio.vehiculo_info,
                        tipo_servicio=servicio_info.tipo_servicio if servicio_info else TipoServicio.OTRO,
                        fecha_completacion=servicio.fecha_completacion,
                        duracion_minutos=servicio.duracion_real_minutos or 0,
                        costo=servicio.costo_final or 0,
                        calificacion=servicio.calificacion_cliente or 0,
                        comentario=servicio.comentario_cliente
                    )
                )
        return sorted(historial, key=lambda x: x.fecha_completacion, reverse=True)

    def agregar_mecanico(self, taller_id: str, mecanico: Mecanico) -> Optional[Mecanico]:
        """Agrega un mecánico a un taller"""
        taller = self.talleres.get(taller_id)
        if not taller:
            return None

        mecanico_id = f"mec-{str(uuid.uuid4())[:8]}"
        mecanico.id = mecanico_id
        self.mecanicos[mecanico_id] = mecanico
        taller.mecanicos.append(mecanico)
        self.talleres[taller_id] = taller
        return mecanico

    def obtener_mecanicos(self, taller_id: str) -> List[Mecanico]:
        """Obtiene los mecánicos de un taller"""
        taller = self.talleres.get(taller_id)
        return taller.mecanicos if taller else []

    def actualizar_calificacion(
        self,
        servicio_id: str,
        calificacion: float,
        comentario: Optional[str] = None
    ) -> Optional[ServicioTaller]:
        """Actualiza la calificación de un servicio"""
        servicio = self.servicios.get(servicio_id)
        if not servicio:
            return None

        servicio.calificacion_cliente = calificacion
        servicio.comentario_cliente = comentario

        # Actualizar calificación del taller
        taller = self.talleres.get(servicio.taller_id)
        if taller:
            servicios_completados = [
                s for s in self.servicios.values()
                if s.taller_id == servicio.taller_id
                and s.estado == EstadoServicio.COMPLETADO
                and s.calificacion_cliente
            ]
            if servicios_completados:
                promedio = sum(s.calificacion_cliente for s in servicios_completados) / len(servicios_completados)
                taller.calificacion_promedio = round(promedio, 1)
                self.talleres[servicio.taller_id] = taller

        self.servicios[servicio_id] = servicio
        return servicio

    def obtener_servicio(self, servicio_id: str) -> Optional[ServicioTaller]:
        """Obtiene un servicio por ID"""
        return self.servicios.get(servicio_id)

    def obtener_servicios_por_fecha(
        self,
        taller_id: str,
        fecha: str
    ) -> List[ServicioTaller]:
        """Obtiene servicios programados para una fecha específica"""
        try:
            fecha_target = datetime.fromisoformat(fecha).date()
            return [
                s for s in self.servicios.values()
                if s.taller_id == taller_id
                and s.fecha_cita.date() == fecha_target
                and s.estado != EstadoServicio.CANCELADO
            ]
        except:
            return []
