"""Vercel entry point: exposes the FastAPI app as a serverless function.

index.html and /img are served by Vercel as static files; every /api/* request comes here.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Vercel's file system is read-only except /tmp
os.environ.setdefault("CHROMA_DIR", "/tmp/chroma_data")
os.environ.setdefault("HOME", "/tmp")

from backend.main import app  # noqa: E402,F401
