#!/bin/bash

# Ejemplos de uso de la API del Taller
# Estos comandos pueden ejecutarse en terminal/bash

BASE_URL="http://localhost:8000"
TALLER_ID="taller-001"
SERVICIO_ID="srv-001"
MECANICO_ID="mec-001"

echo "=========================================="
echo "API DEL TALLER - EJEMPLOS DE USO"
echo "=========================================="

# 1. Listar todos los talleres
echo -e "\n1. Listar todos los talleres:"
curl -s "$BASE_URL/api/taller/listar" | python -m json.tool | head -20

# 2. Obtener datos de un taller específico
echo -e "\n\n2. Obtener datos de un taller específico:"
curl -s "$BASE_URL/api/taller/$TALLER_ID" | python -m json.tool | head -25

# 3. Obtener resumen del taller
echo -e "\n\n3. Obtener resumen del estado del taller:"
curl -s "$BASE_URL/api/taller/$TALLER_ID/resumen" | python -m json.tool

# 4. Obtener citas pendientes
echo -e "\n\n4. Obtener citas pendientes:"
curl -s "$BASE_URL/api/taller/$TALLER_ID/citas/pendientes" | python -m json.tool | head -30

# 5. Obtener citas confirmadas
echo -e "\n\n5. Obtener citas confirmadas/en progreso:"
curl -s "$BASE_URL/api/taller/$TALLER_ID/citas/confirmadas" | python -m json.tool | head -30

# 6. Obtener citas por fecha
echo -e "\n\n6. Obtener citas programadas para una fecha:"
FECHA=$(date +%Y-%m-%d)
curl -s "$BASE_URL/api/taller/$TALLER_ID/citas/fecha?fecha=$FECHA" | python -m json.tool | head -30

# 7. Ver detalles de una cita
echo -e "\n\n7. Ver detalles de una cita:"
curl -s "$BASE_URL/api/taller/$TALLER_ID/citas/$SERVICIO_ID" | python -m json.tool | head -40

# 8. Listar mecánicos del taller
echo -e "\n\n8. Listar mecánicos del taller:"
curl -s "$BASE_URL/api/taller/$TALLER_ID/mecanicos" | python -m json.tool

# 9. Confirmar una cita con un mecánico
echo -e "\n\n9. Confirmar una cita (asignar mecánico):"
curl -s -X POST "$BASE_URL/api/taller/$TALLER_ID/citas/$SERVICIO_ID/confirmar?mecanico_id=$MECANICO_ID" | python -m json.tool | head -30

# 10. Iniciar servicio
echo -e "\n\n10. Iniciar un servicio (cambiar a 'en progreso'):"
curl -s -X POST "$BASE_URL/api/taller/$TALLER_ID/citas/$SERVICIO_ID/iniciar" | python -m json.tool | head -30

# 11. Completar servicio
echo -e "\n\n11. Completar un servicio:"
curl -s -X POST "$BASE_URL/api/taller/$TALLER_ID/citas/$SERVICIO_ID/completar?duracion_minutos=35&costo_final=50.00&notas=Cambio%20completado%20sin%20problemas" | python -m json.tool | head -30

# 12. Agregar nuevo mecánico
echo -e "\n\n12. Agregar un nuevo mecánico:"
curl -s -X POST "$BASE_URL/api/taller/$TALLER_ID/mecanicos" \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Juan Pérez",
    "especialidad": "Electricista automotriz",
    "experiencia_años": 7
  }' | python -m json.tool

# 13. Obtener historial de servicios completados
echo -e "\n\n13. Obtener historial de servicios completados:"
curl -s "$BASE_URL/api/taller/$TALLER_ID/historial" | python -m json.tool | head -40

# 14. Calificar un servicio (como cliente)
echo -e "\n\n14. Actualizar calificación de un servicio:"
curl -s -X POST "$BASE_URL/api/taller/$TALLER_ID/citas/$SERVICIO_ID/calificar?calificacion=5&comentario=Excelente%20trabajo" | python -m json.tool | head -30

echo -e "\n\n=========================================="
echo "Fin de ejemplos"
echo "=========================================="
