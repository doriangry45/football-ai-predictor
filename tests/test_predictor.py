import pytest
from services.feature-002_ai_predictor.app import app, check_limit

def test_rate_limit():
    assert check_limit("test") == True
    # 1000 kez artır, sonra False