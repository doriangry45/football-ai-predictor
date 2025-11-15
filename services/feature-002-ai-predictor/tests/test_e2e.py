import os
import time
import subprocess
import requests

BASE_DIR = os.path.dirname(__file__)
APP_DIR = os.path.abspath(os.path.join(BASE_DIR, '..'))


def start_app():
    env = os.environ.copy()
    env['DEMO_MODE'] = '1'
    # Start the app as a subprocess
    p = subprocess.Popen(['python', 'app.py'], cwd=APP_DIR, env=env)
    time.sleep(2)
    return p


def stop_app(p):
    p.terminate()
    try:
        p.wait(timeout=5)
    except Exception:
        p.kill()


def test_root_and_predict():
    p = start_app()
    try:
        r = requests.get('http://127.0.0.1:5000/', timeout=5)
        assert r.status_code == 200
        assert 'E-Football AI' in r.text or 'Tahmin' in r.text

        r2 = requests.post('http://127.0.0.1:5000/api/predict', json={}, timeout=10)
        assert r2.status_code == 200
        data = r2.json()
        assert 'matches' in data
        assert isinstance(data['matches'], list)
    finally:
        stop_app(p)
