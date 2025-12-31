import uvicorn
from api import app
import os

def run_server():
    """Run the FastAPI server with uvicorn"""
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "True").lower() == "true"

    uvicorn.run(
        app,
        host=host,
        port=port,
        reload=reload,
        debug=True,
        log_level="info",
        workers=1  # For development; in production you might want multiple workers
    )

if __name__ == "__main__":
    print("Starting FastAPI server...")
    print("API documentation available at: http://localhost:8000/docs")
    print("Alternative docs at: http://localhost:8000/redoc")
    print(f"Server running on http://{os.getenv('HOST', '0.0.0.0')}:{os.getenv('PORT', 8000)}")
    run_server()