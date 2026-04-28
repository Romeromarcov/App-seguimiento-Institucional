#!/bin/bash

# EJEMPLOS DE USO - API Cliente Lubrikca
# ====================================
# Ejecuta estos comandos para probar la API

BASE_URL="http://localhost:8000/api/cliente"
USER_DEMO="user-001"
VEH_DEMO="veh-001"
TALLER_DEMO="taller-001"

echo "🚀 EJEMPLOS DE API - MVP CLIENTE LUBRIKCA"
echo "=========================================="
echo ""
echo "Base URL: $BASE_URL"
echo ""

# ============================================================================
# 1. AUTENTICACIÓN & USUARIOS
# ============================================================================

echo "📝 1. REGISTRO DE NUEVO USUARIO"
echo "==============================="
echo ""
echo "Comando:"
echo 'curl -X POST '$BASE_URL'/registro \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{
  "nombre": "Carlos López",
  "cedula": "98765432",
  "correo": "carlos@example.com",
  "telefono": "+58-412-5551234",
  "direccion": "Calle 5 Apto 10, Caracas",
  "empresa": "Seguros Xyz"
}'"'"

echo ""
echo "Respuesta esperada:"
echo '{"id": "user-xxx...", "datos_personales": {...}, "vehiculos": [], ...}'
echo ""
echo ""

# ============================================================================
# 2. USUARIOS EXISTENTES
# ============================================================================

echo "👤 2. OBTENER PERFIL DE USUARIO"
echo "================================"
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/perfil/$USER_DEMO"
echo ""
echo "Respuesta esperada: Datos completos del usuario, vehículos, GPS, etc."
echo ""
echo ""

echo "📊 3. OBTENER RESUMEN DEL USUARIO"
echo "=================================="
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/resumen/$USER_DEMO"
echo ""
echo "Respuesta esperada:"
echo '{
  "usuario_id": "user-001",
  "nombre": "Juan García",
  "total_vehiculos": 1,
  "total_citas": 0,
  "citas_activas": 0,
  "total_credito_disponible": 0,
  "gps_activo": true
}'
echo ""
echo ""

echo "📍 4. ACTUALIZAR UBICACIÓN GPS"
echo "=============================="
echo ""
echo "Comando:"
echo 'curl -X PUT '$BASE_URL'/ubicacion/'$USER_DEMO'?latitud=10.4806&longitud=-66.9036'
echo ""
echo "Respuesta esperada: {status: success, coordenadas: {lat, lng}}"
echo ""
echo ""

# ============================================================================
# 3. VEHÍCULOS
# ============================================================================

echo "🚗 5. REGISTRAR NUEVO VEHÍCULO"
echo "=============================="
echo ""
echo "Comando:"
echo 'curl -X POST '$BASE_URL'/vehiculos/'$USER_DEMO' \'
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{
  "marca": "Honda",
  "modelo": "Civic",
  "año": 2019,
  "placa": "DEF-456",
  "tipo_lubricante": "semisintético",
  "litros_capacidad": 3.7,
  "kilometraje_inicial": 45000
}'"'"

echo ""
echo "Respuesta: Nuevo vehículo con ID generado"
echo ""
echo ""

echo "🚗 6. LISTAR VEHÍCULOS DEL USUARIO"
echo "=================================="
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/vehiculos/$USER_DEMO"
echo ""
echo "Respuesta: Array de todos los vehículos"
echo ""
echo ""

echo "🚗 7. OBTENER DETALLES DE UN VEHÍCULO"
echo "====================================="
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/vehiculo/$VEH_DEMO"
echo ""
echo "Respuesta: Detalles completos del vehículo"
echo ""
echo ""

# ============================================================================
# 4. KILOMETRAJE & MANTENIMIENTO
# ============================================================================

echo "⛽ 8. REGISTRAR KILOMETRAJE"
echo "=========================="
echo ""
echo "Comando:"
echo 'curl -X POST '$BASE_URL'/kilometraje/'$USER_DEMO'/'$VEH_DEMO'?kilometraje=62500'
echo ""
echo "Respuesta: {status: success, registro_id: xxx, kilometraje: 62500}"
echo ""
echo "⚠️  Nota: Genera automáticamente recomendaciones si km > recomendado"
echo ""
echo ""

echo "📋 9. VER HISTORIAL DE KILOMETRAJE"
echo "=================================="
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/historial-kilometraje/$VEH_DEMO"
echo ""
echo "Respuesta: {vehiculo_id: xxx, registros: [...], total_registros: N}"
echo ""
echo ""

echo "🔧 10. VER RECOMENDACIONES DE MANTENIMIENTO"
echo "=========================================="
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/recomendaciones/$VEH_DEMO"
echo ""
echo "Respuesta: Array de recomendaciones con componentes, urgencia, etc."
echo ""
echo "Ejemplo:"
echo '[
  {
    "id": "rec-xxx",
    "vehiculo_id": "veh-001",
    "tipo": "mantenimiento_preventivo",
    "componente": "cambio_aceite",
    "kilometraje_recomendado": 10000,
    "kilometraje_actual": 12500,
    "estado": "vencido",
    "urgencia": "crítica"
  }
]'
echo ""
echo ""

# ============================================================================
# 5. LUBRICANTES & TALLERES
# ============================================================================

echo "🛢️  11. OBTENER LUBRICANTES DISPONIBLES"
echo "========================================"
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/lubricantes"
echo ""
echo "Respuesta:"
echo '{
  "sintetico_5w30": {
    "nombre": "Castrol Edge 5W30",
    "precio_litro": 150000,
    "tipo": "sintético"
  },
  ...
}'
echo ""
echo ""

echo "🏪 12. OBTENER TALLERES DISPONIBLES"
echo "===================================="
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/talleres"
echo ""
echo "Respuesta:"
echo '[
  {
    "id": "taller-001",
    "nombre": "Lubrikca Centro",
    "direccion": "Centro Plaza, Caracas",
    "calificacion": 4.8,
    "coordenadas": {"lat": 10.4806, "lng": -66.9036}
  },
  ...
]'
echo ""
echo ""

# ============================================================================
# 6. SERVICIOS & CITAS
# ============================================================================

echo "📅 13. SOLICITAR SERVICIO (CREAR CITA)"
echo "======================================"
echo ""
echo "Comando:"
echo 'curl -X POST '$BASE_URL'/solicitar-servicio/'$USER_DEMO' \'
echo '  -G \\'
echo '  --data-urlencode "vehiculo_id='$VEH_DEMO'" \'
echo '  --data-urlencode "taller_id='$TALLER_DEMO'" \'
echo '  --data-urlencode "fecha_hora=2026-05-01T14:00:00" \'
echo '  --data-urlencode "tipo_servicio=cambio_aceite"'
echo ""
echo "Respuesta:"
echo '{
  "status": "success",
  "cita_id": "cita-abcd1234",
  "qr_code": "QR-cita-abcd1234-xyz789",
  "costo_estimado": 200000,
  "descuento_credito_50pct": 210000,
  "monto_final": -10000
}'
echo ""
echo ""

echo "📋 14. LISTAR MIS CITAS"
echo "======================"
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/mis-citas/$USER_DEMO"
echo ""
echo "Respuesta:"
echo '{
  "usuario_id": "user-001",
  "citas": [...],
  "total_citas": 2,
  "citas_pendientes": 1,
  "citas_confirmadas": 1
}'
echo ""
echo ""

echo "📄 15. OBTENER DETALLE DE CITA"
echo "=============================="
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/cita/cita-abcd1234"
echo ""
echo "Respuesta: Detalle completo de la cita con QR, costos, estado, etc."
echo ""
echo ""

echo "✅ 16. CONFIRMAR SERVICIO EN TALLER (ESCANEAR QR)"
echo "=================================================="
echo ""
echo "Comando:"
echo "curl -X POST $BASE_URL/confirmar-en-taller/cita-abcd1234"
echo ""
echo "Respuesta:"
echo '{
  "status": "success",
  "cita_id": "cita-abcd1234",
  "estado": "en_proceso",
  "mensaje": "Servicio iniciado. Recibiendo beneficio de crédito del 50%"
}'
echo ""
echo "✨ EN ESTE MOMENTO SE ACTIVA EL CRÉDITO DEL 50%"
echo ""
echo ""

echo "🏁 17. COMPLETAR SERVICIO & CALIFICAR"
echo "====================================="
echo ""
echo "Comando:"
echo 'curl -X POST '$BASE_URL'/completar-servicio/cita-abcd1234 \'
echo '  -G \\'
echo '  --data-urlencode "calificacion=5" \'
echo '  --data-urlencode "comentario=Excelente servicio, muy profesionales"'
echo ""
echo "Respuesta:"
echo '{
  "status": "success",
  "cita_id": "cita-abcd1234",
  "estado": "completada",
  "calificacion": 5,
  "credito_otorgado": 210000,
  "mensaje": "Servicio completado. Crédito de \$210.000 otorgado"
}'
echo ""
echo "💳 EN ESTE MOMENTO SE GENERA EL CRÉDITO AUTOMÁTICAMENTE"
echo ""
echo ""

echo "❌ 18. CANCELAR CITA"
echo "==================="
echo ""
echo "Comando:"
echo "curl -X POST $BASE_URL/cancelar-cita/cita-abcd1234"
echo ""
echo "Respuesta:"
echo '{
  "status": "success",
  "cita_id": "cita-abcd1234",
  "estado": "cancelada"
}'
echo ""
echo "⚠️  Solo se pueden cancelar citas en estado PENDIENTE"
echo ""
echo ""

# ============================================================================
# 7. CRÉDITOS
# ============================================================================

echo "💳 19. VER MIS CRÉDITOS DISPONIBLES"
echo "===================================="
echo ""
echo "Comando:"
echo "curl -X GET $BASE_URL/mis-creditos/$USER_DEMO"
echo ""
echo "Respuesta: Array de créditos"
echo '[
  {
    "id": "cred-xxx",
    "usuario_id": "user-001",
    "cita_id": "cita-abcd1234",
    "monto_lubricante": 210000,
    "monto_credito": 210000,
    "fecha_otorgado": "2026-04-28T14:30:00",
    "aplicado": false
  }
]'
echo ""
echo ""

# ============================================================================
# BASH UTILITIES
# ============================================================================

echo "🔧 FUNCIONES ÚTILES BASH"
echo "========================"
echo ""
echo "# Función para registrar usuario y capturar ID:"
echo "register_user() {"
echo '  RESPONSE=$(curl -s -X POST '$BASE_URL'/registro \'
echo '    -H "Content-Type: application/json" \'
echo '    -d '"'"'{
  "nombre": "$1",
  "cedula": "$2",
  "correo": "$3",
  "telefono": "$4",
  "direccion": "$5",
  "empresa": "$6"
}'"'"')'
echo '  echo "$RESPONSE" | jq -r ".id"'
echo "}"
echo ""
echo "# Uso: USER_ID=\$(register_user 'Juan' '123' 'juan@test.com' '+58...' 'Calle 1' 'Corp')"
echo ""
echo ""

echo "# Función para hacer request GET con JSON bonito:"
echo "api_get() {"
echo "  curl -s -X GET \"\$1\" | jq '.'"
echo "}"
echo ""
echo "# Uso: api_get '$BASE_URL/perfil/user-001'"
echo ""
echo ""

echo "════════════════════════════════════════════════════"
echo "FIN DE EJEMPLOS"
echo "════════════════════════════════════════════════════"
echo ""
echo "📖 Documentación completa en: MVP_CLIENTE_README.md"
echo "🔄 Flujos detallados en: FLUJO_USUARIO.md"
echo "🚀 Inicio rápido en: QUICK_START.md"
