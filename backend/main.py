from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os

from backend.routes import syllabus, generate

app = FastAPI(
    title="Conscious Commute API",
    description="FastAPI Backend for Mumbai Local Student Commute Study Planner.",
    version="1.0.0"
)

# CORS Configuration
allowed_origins_str = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_str:
    allowed_origins = [o.strip() for o in allowed_origins_str.split(",") if o.strip()]
else:
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:8080",
        "http://localhost:8080",
        "http://127.0.0.1:55704"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(syllabus.router, prefix="/api")
app.include_router(generate.router, prefix="/api")

# Static Files Mounting
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
frontend_dir = os.path.join(base_dir, "frontend")

if os.path.exists(frontend_dir):
    # Mount subfolders of frontend for static assets
    css_path = os.path.join(frontend_dir, "css")
    js_path = os.path.join(frontend_dir, "js")
    assets_path = os.path.join(frontend_dir, "assets")
    
    app.mount("/css", StaticFiles(directory=css_path), name="css")
    app.mount("/js", StaticFiles(directory=js_path), name="js")
    app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
    # Mount railway data directory statically
    app.mount("/railway-data", StaticFiles(directory=os.path.join(base_dir, "data", "railway")), name="railway-data")

    @app.get("/")
    def serve_frontend():
        index_file = os.path.join(frontend_dir, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return {"status": "Backend running. Frontend index.html not found."}
else:
    @app.get("/")
    def serve_status():
        return {"status": "Backend running. Frontend folder not found."}
