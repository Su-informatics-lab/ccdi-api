#!/usr/bin/env python3
"""
Simple test script to start the CCDI API server.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    import uvicorn
    from app.main import app
    
    print("✅ CCDI API Starting...")
    print("📊 Server will be available at: http://localhost:8000")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("🔧 OpenAPI Schema: http://localhost:8000/openapi.json")
    print("⏹️  Press Ctrl+C to stop the server")
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    )
    
except KeyboardInterrupt:
    print("\n👋 Server stopped by user")
except Exception as e:
    print(f"❌ Error starting server: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
