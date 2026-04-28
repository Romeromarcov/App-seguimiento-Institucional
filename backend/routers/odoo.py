from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime
from config import ODOO_URL, ODOO_DB, ODOO_USER, ODOO_API_TOKEN

router = APIRouter(prefix="/api/odoo", tags=["odoo"])

class PaymentData(BaseModel):
    partner_id: int
    amount: float
    reference: str = ""

class SalesOrderData(BaseModel):
    partner_id: int
    description: str
    amount: float

def call_odoo_jsonrpc(method: str, params: dict, endpoint: str = "/jsonrpc"):
    """Llamar a Odoo usando JSON-RPC"""
    url = f"{ODOO_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()

        if "error" in result and result["error"]:
            raise Exception(f"Odoo error: {result['error']}")

        return result.get("result", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

@router.get("/test-connection")
def test_connection():
    """Probar conexión con Odoo"""
    try:
        # Intentar obtener version de Odoo
        result = call_odoo_jsonrpc(
            "call",
            {
                "service": "common",
                "method": "version"
            }
        )

        return {
            "status": "conectado",
            "url": ODOO_URL,
            "user": ODOO_USER,
            "database": ODOO_DB,
            "version": result
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
        # Autenticar y obtener uid
        uid = call_odoo_jsonrpc(
            "call",
            {
                "service": "common",
                "method": "authenticate",
                "args": [ODOO_DB, ODOO_USER, ODOO_API_TOKEN, {}]
            }
        )

        if not uid:
            raise Exception("Autenticación fallida")

        # Obtener partners (supplier_rank > 0)
        partners = call_odoo_jsonrpc(
            "call",
            {
                "service": "object",
                "method": "execute",
                "args": [
                    ODOO_DB,
                    uid,
                    ODOO_API_TOKEN,
                    "res.partner",
                    "search_read",
                    [["supplier_rank", ">", 0]],
                    ["id", "name", "email", "phone", "supplier_rank"]
                ]
            }
        )

        return {
            "partners": partners,
            "count": len(partners),
            "status": "success"
        }
    except Exception as e:
        # En caso de error, devolver lista vacía pero sin fallar
        return {
            "partners": [],
            "count": 0,
            "status": "error",
            "detail": str(e)
        }

@router.post("/create-sales-order")
def create_sales_order(order_data: SalesOrderData):
    """Crear sales.order en Odoo desde un pedido"""
    try:
        # Autenticar
        uid = call_odoo_jsonrpc(
            "call",
            {
                "service": "common",
                "method": "authenticate",
                "args": [ODOO_DB, ODOO_USER, ODOO_API_TOKEN, {}]
            }
        )

        if not uid:
            raise Exception("Autenticación fallida")

        # Crear sales.order
        order_vals = {
            "partner_id": order_data.partner_id,
            "order_line": [(0, 0, {
                "name": order_data.description,
                "product_qty": 1,
                "price_unit": order_data.amount
            })]
        }

        order_id = call_odoo_jsonrpc(
            "call",
            {
                "service": "object",
                "method": "execute",
                "args": [
                    ODOO_DB,
                    uid,
                    ODOO_API_TOKEN,
                    "sale.order",
                    "create",
                    [order_vals]
                ]
            }
        )

        return {
            "status": "creado",
            "order_id": order_id,
            "description": order_data.description,
            "amount": order_data.amount,
            "partner_id": order_data.partner_id,
            "url": f"{ODOO_URL}/web#id={order_id}&model=sale.order&view_type=form"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando sales.order: {str(e)}")

@router.post("/create-payment")
def create_payment(payment_data: PaymentData):
    """Crear account.payment en Odoo (crédito a taller)"""
    try:
        # Autenticar
        uid = call_odoo_jsonrpc(
            "call",
            {
                "service": "common",
                "method": "authenticate",
                "args": [ODOO_DB, ODOO_USER, ODOO_API_TOKEN, {}]
            }
        )

        if not uid:
            raise Exception("Autenticación fallida")

        # Crear payment
        payment_vals = {
            "partner_id": payment_data.partner_id,
            "amount": payment_data.amount,
            "payment_type": "outbound",
            "partner_type": "supplier",
            "memo": f"Credito CxC - {payment_data.reference}"
        }

        payment_id = call_odoo_jsonrpc(
            "call",
            {
                "service": "object",
                "method": "execute",
                "args": [
                    ODOO_DB,
                    uid,
                    ODOO_API_TOKEN,
                    "account.payment",
                    "create",
                    [payment_vals]
                ]
            }
        )

        return {
            "status": "creado",
            "payment_id": payment_id,
            "amount": payment_data.amount,
            "reference": payment_data.reference,
            "partner_id": payment_data.partner_id,
            "url": f"{ODOO_URL}/web#id={payment_id}&model=account.payment&view_type=form"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creando payment: {str(e)}")

@router.get("/sales-orders")
def get_sales_orders(partner_id: int = None):
    """Obtener sales.orders de Odoo"""
    try:
        # Autenticar
        uid = call_odoo_jsonrpc(
            "call",
            {
                "service": "common",
                "method": "authenticate",
                "args": [ODOO_DB, ODOO_USER, ODOO_API_TOKEN, {}]
            }
        )

        if not uid:
            raise Exception("Autenticación fallida")

        # Filtro
        domain = []
        if partner_id:
            domain = [["partner_id", "=", partner_id]]

        # Obtener órdenes
        orders = call_odoo_jsonrpc(
            "call",
            {
                "service": "object",
                "method": "execute",
                "args": [
                    ODOO_DB,
                    uid,
                    ODOO_API_TOKEN,
                    "sale.order",
                    "search_read",
                    domain,
                    ["id", "name", "partner_id", "date_order", "amount_total", "state"]
                ]
            }
        )

        return {
            "orders": orders,
            "count": len(orders),
            "status": "success"
        }
    except Exception as e:
        return {
            "orders": [],
            "count": 0,
            "status": "error",
            "detail": str(e)
        }

@router.get("/payments")
def get_payments(partner_id: int = None):
    """Obtener account.payments de Odoo"""
    try:
        # Autenticar
        uid = call_odoo_jsonrpc(
            "call",
            {
                "service": "common",
                "method": "authenticate",
                "args": [ODOO_DB, ODOO_USER, ODOO_API_TOKEN, {}]
            }
        )

        if not uid:
            raise Exception("Autenticación fallida")

        # Filtro
        domain = [["partner_type", "=", "supplier"]]
        if partner_id:
            domain.append(["partner_id", "=", partner_id])

        # Obtener pagos
        payments = call_odoo_jsonrpc(
            "call",
            {
                "service": "object",
                "method": "execute",
                "args": [
                    ODOO_DB,
                    uid,
                    ODOO_API_TOKEN,
                    "account.payment",
                    "search_read",
                    domain,
                    ["id", "name", "partner_id", "date", "amount", "state"]
                ]
            }
        )

        return {
            "payments": payments,
            "count": len(payments),
            "status": "success"
        }
    except Exception as e:
        return {
            "payments": [],
            "count": 0,
            "status": "error",
            "detail": str(e)
        }
