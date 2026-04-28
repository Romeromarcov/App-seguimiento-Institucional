import uuid
from datetime import datetime, timedelta
from typing import List, Optional
from ..models.cliente import (
    UsuarioCliente, Vehiculo, RegistroKilometraje, ServicioCita,
    RecomendacionMantenimiento, CreditoBeneficio, Taller, DatosPersonales,
    EstadoCita, TipoLubricante
)

class ClienteService:
    def __init__(self):
        self.usuarios = {}
        self.vehiculos = {}
        self.registros_kilometraje = {}
        self.citas = {}
        self.recomendaciones = {}
        self.creditos = {}
        self._init_datos_mockup()

    def _init_datos_mockup(self):
        # Usuarios de prueba
        self.usuarios["user-001"] = UsuarioCliente(
            id="user-001",
            datos_personales=DatosPersonales(
                nombre="Juan García",
                cedula="12345678",
                correo="juan@example.com",
                telefono="+58-414-1234567",
                direccion="Av. Principal 123, Caracas",
                empresa="Tech Corp"
            ),
            vehiculos=[
                Vehiculo(
                    id="veh-001",
                    marca="Toyota",
                    modelo="Corolla",
                    año=2020,
                    placa="ABC-123",
                    tipo_lubricante=TipoLubricante.SINTETICO,
                    litros_capacidad=4.2,
                    kilometraje_inicial=50000,
                    fecha_registro=datetime.now() - timedelta(days=30)
                )
            ],
            gps_activo=True,
            latitud=10.4806,
            longitud=-66.9036,
            fecha_registro=datetime.now() - timedelta(days=60),
            activo=True
        )

        # Talleres de prueba
        self.talleres = [
            Taller(id="taller-001", nombre="Lubrikca Centro",
                  direccion="Centro Plaza", latitud=10.4806, longitud=-66.9036, calificacion_promedio=4.8),
            Taller(id="taller-002", nombre="Lubrikca Las Mercedes",
                  direccion="Las Mercedes", latitud=10.4900, longitud=-66.8900, calificacion_promedio=4.6),
            Taller(id="taller-003", nombre="Lubrikca Chacao",
                  direccion="Chacao", latitud=10.4950, longitud=-66.8750, calificacion_promedio=4.5),
        ]

        # Lubricantes disponibles
        self.lubricantes_disponibles = {
            "sintetico_5w30": {"nombre": "Castrol Edge 5W30", "precio_litro": 150000, "tipo": "sintético"},
            "sintetico_0w20": {"nombre": "Mobil 1 0W20", "precio_litro": 160000, "tipo": "sintético"},
            "semisintetico_10w40": {"nombre": "Shell Helix 10W40", "precio_litro": 100000, "tipo": "semisintético"},
            "mineral_20w50": {"nombre": "Pennzoil 20W50", "precio_litro": 70000, "tipo": "mineral"},
        }

        # Datos de mantenimiento preventivo por marca
        self.planes_mantenimiento = {
            "Toyota": {
                "cambio_aceite": 10000,
                "cambio_filtro": 10000,
                "rotacion_llantas": 15000,
                "inspeccion_frenos": 30000,
                "cambio_refrigerante": 80000,
            },
            "Chevrolet": {
                "cambio_aceite": 10000,
                "cambio_filtro": 10000,
                "rotacion_llantas": 16000,
                "inspeccion_frenos": 35000,
                "cambio_refrigerante": 100000,
            },
            "Ford": {
                "cambio_aceite": 12000,
                "cambio_filtro": 12000,
                "rotacion_llantas": 16000,
                "inspeccion_frenos": 30000,
                "cambio_refrigerante": 90000,
            },
        }

    # Usuario
    def registrar_usuario(self, datos_personales: DatosPersonales) -> UsuarioCliente:
        usuario_id = f"user-{uuid.uuid4().hex[:8]}"
        usuario = UsuarioCliente(
            id=usuario_id,
            datos_personales=datos_personales,
            fecha_registro=datetime.now()
        )
        self.usuarios[usuario_id] = usuario
        return usuario

    def obtener_usuario(self, usuario_id: str) -> Optional[UsuarioCliente]:
        return self.usuarios.get(usuario_id)

    def actualizar_ubicacion(self, usuario_id: str, latitud: float, longitud: float) -> UsuarioCliente:
        usuario = self.usuarios.get(usuario_id)
        if usuario:
            usuario.latitud = latitud
            usuario.longitud = longitud
        return usuario

    # Vehículo
    def registrar_vehiculo(self, usuario_id: str, vehiculo: Vehiculo) -> Vehiculo:
        vehiculo.id = f"veh-{uuid.uuid4().hex[:8]}"
        vehiculo.fecha_registro = datetime.now()

        usuario = self.usuarios.get(usuario_id)
        if usuario:
            usuario.vehiculos.append(vehiculo)
            self.vehiculos[vehiculo.id] = vehiculo

        return vehiculo

    def obtener_vehiculos(self, usuario_id: str) -> List[Vehiculo]:
        usuario = self.usuarios.get(usuario_id)
        return usuario.vehiculos if usuario else []

    def obtener_vehiculo(self, vehiculo_id: str) -> Optional[Vehiculo]:
        return self.vehiculos.get(vehiculo_id)

    # Kilometraje
    def registrar_kilometraje(self, usuario_id: str, vehiculo_id: str, kilometraje: int) -> RegistroKilometraje:
        registro_id = f"reg-{uuid.uuid4().hex[:8]}"
        registro = RegistroKilometraje(
            id=registro_id,
            vehiculo_id=vehiculo_id,
            kilometraje=kilometraje,
            fecha=datetime.now()
        )
        self.registros_kilometraje[registro_id] = registro

        vehiculo = self.obtener_vehiculo(vehiculo_id)
        if vehiculo and kilometraje > vehiculo.kilometraje_inicial:
            self._generar_recomendaciones(usuario_id, vehiculo_id, kilometraje)

        return registro

    def obtener_historial_kilometraje(self, vehiculo_id: str) -> List[RegistroKilometraje]:
        return [r for r in self.registros_kilometraje.values()
                if r.vehiculo_id == vehiculo_id]

    # Recomendaciones
    def _generar_recomendaciones(self, usuario_id: str, vehiculo_id: str, km_actual: int):
        vehiculo = self.obtener_vehiculo(vehiculo_id)
        if not vehiculo:
            return

        plan = self.planes_mantenimiento.get(vehiculo.marca, {})

        for componente, km_recomendado in plan.items():
            km_desde_inicio = km_actual - vehiculo.kilometraje_inicial

            if km_desde_inicio > 0 and km_desde_inicio >= km_recomendado:
                urgencia = "crítica" if km_desde_inicio > km_recomendado * 1.2 else "normal"
                estado = "vencido" if km_desde_inicio > km_recomendado else "próximo"

                rec_id = f"rec-{uuid.uuid4().hex[:8]}"
                recomendacion = RecomendacionMantenimiento(
                    id=rec_id,
                    vehiculo_id=vehiculo_id,
                    tipo="mantenimiento_preventivo",
                    componente=componente,
                    kilometraje_recomendado=km_recomendado,
                    kilometraje_actual=km_desde_inicio,
                    estado=estado,
                    urgencia=urgencia
                )
                self.recomendaciones[rec_id] = recomendacion

    def obtener_recomendaciones(self, vehiculo_id: str) -> List[RecomendacionMantenimiento]:
        return [r for r in self.recomendaciones.values()
                if r.vehiculo_id == vehiculo_id]

    # Citas y Servicios
    def obtener_talleres(self) -> List[dict]:
        return [
            {
                "id": t.id,
                "nombre": t.nombre,
                "direccion": t.direccion,
                "calificacion": t.calificacion_promedio,
                "coordenadas": {"lat": t.latitud, "lng": t.longitud}
            }
            for t in self.talleres
        ]

    def solicitar_servicio(self, usuario_id: str, vehiculo_id: str,
                          taller_id: str, fecha_hora: datetime,
                          tipo_servicio: str = "cambio_aceite") -> ServicioCita:
        cita_id = f"cita-{uuid.uuid4().hex[:8]}"

        # Calcular costo estimado basado en el tipo de lubricante
        vehiculo = self.obtener_vehiculo(vehiculo_id)
        costo_base = 200000 if tipo_servicio == "cambio_aceite" else 150000
        costo_estimado = costo_base

        # Calcular descuento del 50% en lubricante
        descuento_50pct = (vehiculo.litros_capacidad * 100000) * 0.5 if vehiculo else 0

        cita = ServicioCita(
            id=cita_id,
            usuario_id=usuario_id,
            vehiculo_id=vehiculo_id,
            taller_id=taller_id,
            fecha_hora=fecha_hora,
            tipo_servicio=tipo_servicio,
            estado=EstadoCita.PENDIENTE,
            costo_estimado=costo_estimado,
            descuento_credito_50pct=descuento_50pct,
            qr_code=self._generar_qr(cita_id),
            fecha_creacion=datetime.now()
        )

        self.citas[cita_id] = cita
        return cita

    def _generar_qr(self, cita_id: str) -> str:
        return f"QR-{cita_id}-{uuid.uuid4().hex[:6]}"

    def obtener_citas_usuario(self, usuario_id: str) -> List[ServicioCita]:
        return [c for c in self.citas.values() if c.usuario_id == usuario_id]

    def obtener_cita(self, cita_id: str) -> Optional[ServicioCita]:
        return self.citas.get(cita_id)

    def confirmar_servicio_en_taller(self, cita_id: str) -> ServicioCita:
        cita = self.citas.get(cita_id)
        if cita:
            cita.estado = EstadoCita.EN_PROCESO
        return cita

    def completar_servicio(self, cita_id: str, calificacion: int,
                          comentario: str = "") -> ServicioCita:
        cita = self.citas.get(cita_id)
        if cita:
            cita.estado = EstadoCita.COMPLETADA
            cita.calificacion_taller = calificacion
            cita.comentario = comentario

            # Generar crédito automáticamente
            credito_id = f"cred-{uuid.uuid4().hex[:8]}"
            credito = CreditoBeneficio(
                id=credito_id,
                usuario_id=cita.usuario_id,
                cita_id=cita_id,
                monto_lubricante=cita.descuento_credito_50pct,
                monto_credito=cita.descuento_credito_50pct,
                fecha_otorgado=datetime.now()
            )
            self.creditos[credito_id] = credito

        return cita

    def cancelar_cita(self, cita_id: str) -> ServicioCita:
        cita = self.citas.get(cita_id)
        if cita:
            cita.estado = EstadoCita.CANCELADA
        return cita

    def obtener_creditos(self, usuario_id: str) -> List[CreditoBeneficio]:
        return [c for c in self.creditos.values() if c.usuario_id == usuario_id]

    def obtener_lubricantes(self) -> dict:
        return self.lubricantes_disponibles
