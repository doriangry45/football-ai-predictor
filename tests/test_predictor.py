import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "services" / "feature-002-ai-predictor"))

import pytest

def test_import_app():
    """Test that app imports successfully."""
    try:
        from services.feature_002_ai_predictor.app import app
        assert app is not None
    except ImportError:
        # Try direct import
        os.chdir(project_root / "services" / "feature-002-ai-predictor")
        from app import app
        assert app is not None

def test_api_health():
    """Test health endpoint."""
    try:
        from services.feature_002_ai_predictor.app import app
    except ImportError:
        os.chdir(project_root / "services" / "feature-002-ai-predictor")
        from app import app
    
    client = app.test_client()
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert "status" in data
    assert data["status"] == "healthy"

def test_api_leagues():
    """Test leagues endpoint."""
    try:
        from services.feature_002_ai_predictor.app import app
    except ImportError:
        os.chdir(project_root / "services" / "feature-002-ai-predictor")
        from app import app
    
    client = app.test_client()
    response = client.get("/api/leagues")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0