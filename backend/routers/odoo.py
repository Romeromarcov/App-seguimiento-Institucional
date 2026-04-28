from fastapi import APIRouter, HTTPException
import requests
from datetime import datetime
from config import ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_TOKEN

router = APIRouter(prefix="/api/odoo", tags=["odoo"])

def call_odoo_api(endpoint: str, method: str = "POST", data: dict = None):
    """Llamar a la API JSON-RPC de Odoo"""
    url = f"{ODOO_URL}/api/v1/{endpoint}" if "/api/" not in endpoint else f"{ODOO_URL}{endpoint}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ODOO_API_TOKEN}"
    }

    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            response = requests.get(url, headers=headers, timeout=10)

        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error llamando Odoo API: {str(e)}")

@router.get("/test-connection")
def test_connection():
    """Probar conexión con Odoo"""
    try:
        result = call_odoo_api("/res.partner", "GET")
        return {
            "status": "conectado",
            "url": ODOO_URL,
            "user": ODOO_USER,
            "database": ODOO_DB
        }
    except HTTPException as e:
        return {
            "status": "error",
            "detail": str(e.detail),
            "url": ODOO_URL
        }

@router.get("/partners")
def get_partners():
    """Obtener todos los partners (talleres) que sean proveedores"""
    try:
        # Hacer petición GET a Odoo API REST
        url = f"{ODOO_URL}/api/v1/res.partner"
        headers = {
            "Authorization": f"Bearer {ODOO_API_TOKEN}",
            "Content-Type": "application/json"
        }

        # En Odoo, filtramos por supplier_rank > 0
        params = {
            "fields": ["id", "name", "email", "phone", "supplier_rank"],
            "domain": [["supplier_rank", ">", 0]]
        }

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        partners = response.json().get("records", [])

        return {
            "partners": partners,
            "count": len(partners),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo partners: {str(e)}")

@router.post("/create-sales-order")
def create_sales_order(order_data: dict):
    """Crear sales.order en Odoo desde un pedido"""
    try:
        # Datos esperados: partner_id, description, amount
        partner_id = order_data.get("partner_id")
        description = order_data.get("description", "Pedido desde App")
        amount = order_data.get("amount", 0)

        url = f"{ODOO_URL}/api/v1/sale.order"
        headers = {
            "Authorization": f"Bearer {ODOO_API_TOKEN}",
            "Content-Type": "application/json"
        }

        # Estructura de sales.order en Odoo
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "sale.order",
                "method": "create",
                "args": [{
                    "partner_id": partner_id,
                    "order_line": [(0, 0, {
                        "name": description,
                        "product_qty": 1,
                        "price_unit": amount
                    })]
                }]
            }
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        order_id = result.get("result", {}).get("id")

        return {
            "status": "creado",
            "order_id": order_id,
            "description": description,
            "amount": amount,
            "url": f"{ODOO_URL}/web#id={order_id}&model=sale.order"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando sales.order: {str(e)}")

@router.post("/create-payment")
def create_payment(payment_data: dict):
    """Crear account.payment en Odoo (crédito a taller)"""
    try:
        partner_id = payment_data.get("partner_id")
        amount = payment_data.get("amount", 0)
        reference = payment_data.get("reference", "")

        url = f"{ODOO_URL}/api/v1/account.payment"
        headers = {
            "Authorization": f"Bearer {ODOO_API_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "model": "account.payment",
                "method": "create",
                "args": [{
                    "partner_id": partner_id,
                    "amount": amount,
                    "payment_type": "outbound",
                    "partner_type": "supplier",
                    "memo": f"Credito CxC - {reference}"
                }]
            }
        }

        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        payment_id = result.get("result", {}).get("id")

        return {
            "status": "creado",
            "payment_id": payment_id,
            "amount": amount,
            "reference": reference,
            "url": f"{ODOO_URL}/web#id={payment_id}&model=account.payment"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando payment: {str(e)}")

@router.get("/sales-orders")
def get_sales_orders(partner_id: int = None):
    """Obtener sales.orders de Odoo"""
    try:
        url = f"{ODOO_URL}/api/v1/sale.order"
        headers = {
            "Authorization": f"Bearer {ODOO_API_TOKEN}",
            "Content-Type": "application/json"
        }

        params = {
            "fields": ["id", "name", "partner_id", "date_order", "amount_total", "state"]
        }

        if partner_id:
            params["domain"] = [["partner_id", "=", partner_id]]

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        orders = response.json().get("records", [])

        return {
            "orders": orders,
            "count": len(orders),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo sales.orders: {str(e)}")

@router.get("/payments")
def get_payments(partner_id: int = None):
    """Obtener account.payments de Odoo"""
    try:
        url = f"{ODOO_URL}/api/v1/account.payment"
        headers = {
            "Authorization": f"Bearer {ODOO_API_TOKEN}",
            "Content-Type": "application/json"
        }

        params = {
            "fields": ["id", "name", "partner_id", "date", "amount", "state"]
        }

        if partner_id:
            params["domain"] = [["partner_id", "=", partner_id], ["partner_type", "=", "supplier"]]

        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        payments = response.json().get("records", [])

        return {
            "payments": payments,
            "count": len(payments),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error obteniendo payments: {str(e)}")
