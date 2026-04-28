import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routers import cliente

app = FastAPI(
    title='App Seguimiento Institucional',
    description='MVP - Módulo Cliente/Usuario para gestión de mantenimiento vehicular',
    version='1.0.0-MVP',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Registrar routers
app.include_router(cliente.router)

# Frontend estático
frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'frontend')
if os.path.isdir(frontend_dir):
    app.mount('/static', StaticFiles(directory=frontend_dir), name='static')

    @app.get('/', include_in_schema=False)
    def index():
        return FileResponse(os.path.join(frontend_dir, 'cliente.html'))

    @app.get('/cliente', include_in_schema=False)
    @app.get('/cliente.html', include_in_schema=False)
    def cliente_page():
        return FileResponse(os.path.join(frontend_dir, 'cliente.html'))

    @app.get('/app', include_in_schema=False)
    def app_redirect():
        return FileResponse(os.path.join(frontend_dir, 'cliente.html'))
