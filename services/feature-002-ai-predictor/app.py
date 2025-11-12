#!/usr/bin/env python3
"""
Flask Web UI for E-Football AI Predictor
Uses Gemini 2.5 Pro for match analysis with RapidAPI data
"""
import os
import json
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

# AI & Storage imports
import google.generativeai as genai
try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

try:
    from supabase import create_client
    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False

from main import EFootballFetcher

# === INIT ===
load_dotenv()
app = Flask(__name__, template_folder="../../../templates")
logging.basicConfig(level=logging.INFO)

# === CONFIG ===
RAPIDAPI_KEYS = [
    os.getenv("RAPIDAPI_KEY1"),
    os.getenv("RAPIDAPI_KEY2"),
    os.getenv("RAPIDAPI_KEY")  # fallback
]
RAPIDAPI_KEYS = [k for k in RAPIDAPI_KEYS if k]

genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY", ""))
model = genai.GenerativeModel('gemini-2.5-pro')

# Redis cache (optional)
r = None
if REDIS_AVAILABLE:
    try:
        r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
    except Exception as e:
        logging.warning(f"Redis connection failed: {e}")

# Supabase backup (optional)
supabase = None
if SUPABASE_AVAILABLE:
    try:
        supabase = create_client(
            os.getenv("SUPABASE_URL", ""),
            os.getenv("SUPABASE_KEY", "")
        )
    except Exception as e:
        logging.warning(f"Supabase connection failed: {e}")

# === RATE LIMIT (with Redis fallback) ===
current_key_index = 0

def check_limit(key_prefix):
    """Check and update rate limit using Redis."""
    if not r:
        return True  # No limit without Redis
    
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"{key_prefix}:{today}"
    try:
        count = r.incr(key)
        if count == 1:
            r.expire(key, 86400)
        if count > 900:  # 1000 limit
            logging.warning(f"Rate limit near: {count}/{key_prefix}")
            return False
        return True
    except Exception as e:
        logging.warning(f"Rate limit check failed: {e}")
        return True

def rotate_api_key():
    """Rotate to next API key."""
    global current_key_index
    current_key_index = (current_key_index + 1) % len(RAPIDAPI_KEYS)
    return RAPIDAPI_KEYS[current_key_index]

# === FETCH + CACHE ===
def get_fixtures(league=39, season=2025):
    """Fetch fixtures with cache fallback."""
    cache_key = f"fixtures:{league}:{season}"
    
    # Try Redis cache first
    if r:
        try:
            cached = r.get(cache_key)
            if cached:
                logging.info(f"Cache hit: {cache_key}")
                return json.loads(cached)
        except Exception as e:
            logging.warning(f"Redis cache miss: {e}")
    
    # Try Supabase cache
    if supabase:
        try:
            result = supabase.table('api_cache').select('value').eq('key', cache_key).execute()
            if result.data:
                logging.info(f"Supabase cache hit: {cache_key}")
                return result.data[0]['value']
        except Exception as e:
            logging.warning(f"Supabase cache miss: {e}")
    
    # Fetch from RapidAPI with key rotation
    fetched_data = None
    for attempt in range(len(RAPIDAPI_KEYS)):
        api_key = RAPIDAPI_KEYS[current_key_index]
        
        if not check_limit(f"rapidapi_key_{current_key_index}"):
            rotate_api_key()
            continue
        
        try:
            fetcher = EFootballFetcher(api_key)
            fetched_data = fetcher.fetch_fixtures(league, season)
            logging.info(f"Fetched {len(fetched_data.get('response', []))} fixtures from RapidAPI")
            
            # Cache in Redis
            if r:
                try:
                    r.setex(cache_key, 3600, json.dumps(fetched_data))
                except Exception as e:
                    logging.warning(f"Redis cache set failed: {e}")
            
            # Cache in Supabase
            if supabase:
                try:
                    supabase.table('api_cache').upsert({
                        "key": cache_key,
                        "value": fetched_data,
                        "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
                    }).execute()
                except Exception as e:
                    logging.warning(f"Supabase cache set failed: {e}")
            
            return fetched_data
        
        except Exception as e:
            logging.error(f"Fetch failed with key {current_key_index}: {e}")
            rotate_api_key()
    
    # Return empty if all attempts failed
    return {"response": [], "errors": "All API keys exhausted"}

# === AI PREDICT ===
def ai_predict(fixtures_data, query="over 2.5"):
    """Analyze fixtures with Gemini."""
    if not os.getenv("GOOGLE_AI_API_KEY"):
        return {"error": "GOOGLE_AI_API_KEY not configured"}
    
    fixtures = fixtures_data.get("response", [])[:10]
    
    if not fixtures:
        return {"matches": [], "error": "No fixtures available"}
    
    fixture_summary = []
    for f in fixtures:
        try:
            h = f.get("teams", {}).get("home", {})
            a = f.get("teams", {}).get("away", {})
            fixture_summary.append({
                "id": f.get("fixture", {}).get("id"),
                "home": h.get("name", "Unknown"),
                "away": a.get("name", "Unknown"),
                "date": f.get("fixture", {}).get("date", ""),
                "status": f.get("fixture", {}).get("status", {}).get("short", "")
            })
        except Exception as e:
            logging.warning(f"Parse fixture error: {e}")
    
    prompt = f"""
    Analyze these upcoming football fixtures for "{query}" predictions:
    {json.dumps(fixture_summary, indent=2)}
    
    For each fixture, provide:
    1. Over 2.5 probability (0-100)
    2. Key analysis reasoning
    3. A short tweet (Turkish)
    
    Return as JSON: {{"matches": [{{"home": "", "away": "", "prediction": "OVER/UNDER", "probability": 0, "reasoning": "", "tweet": ""}}]}}
    """
    
    try:
        response = model.generate_content(prompt)
        try:
            # Extract JSON from response
            text = response.text
            start = text.find("{")
            end = text.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = text[start:end]
                return json.loads(json_str)
        except json.JSONDecodeError:
            pass
        
        return {
            "matches": [
                {
                    "home": f["home"],
                    "away": f["away"],
                    "prediction": "ANALYZING",
                    "probability": 0,
                    "reasoning": "AI analysis in progress",
                    "tweet": response.text[:140]
                }
                for f in fixture_summary
            ]
        }
    
    except Exception as e:
        logging.error(f"AI prediction failed: {e}")
        return {"error": str(e), "matches": []}

# === ROUTES ===

@app.route("/")
def dashboard():
    """Main dashboard."""
    return render_template("predict.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    """AI prediction endpoint."""
    try:
        data = request.get_json() or {}
        league = data.get("league", 39)
        season = data.get("season", 2025)
        query = data.get("query", "over 2.5")
        
        # Get fixtures
        fixtures = get_fixtures(league, season)
        if "errors" in fixtures and not fixtures.get("response"):
            return jsonify({"error": "No fixtures available"}), 503
        
        # AI prediction
        prediction = ai_predict(fixtures, query)
        
        # Save predictions to Supabase (optional)
        if supabase and "matches" in prediction:
            try:
                for match in prediction.get("matches", []):
                    supabase.table('predictions').insert({
                        "league_id": league,
                        "season": season,
                        "home_team": match.get("home", ""),
                        "away_team": match.get("away", ""),
                        "prediction_type": query,
                        "prediction": match.get("prediction", ""),
                        "probability": match.get("probability", 0),
                        "reasoning": match.get("reasoning", ""),
                        "tweet": match.get("tweet", ""),
                        "created_at": datetime.now().isoformat()
                    }).execute()
            except Exception as e:
                logging.warning(f"Supabase insert failed: {e}")
        
        return jsonify(prediction)
    
    except Exception as e:
        logging.error(f"Predict endpoint error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health():
    """Health check."""
    return jsonify({
        "status": "healthy",
        "redis": bool(r),
        "supabase": bool(supabase),
        "google_ai": bool(os.getenv("GOOGLE_AI_API_KEY")),
        "api_keys": len(RAPIDAPI_KEYS)
    })

@app.route("/api/leagues", methods=["GET"])
def leagues():
    """Popular leagues."""
    return jsonify([
        {"id": 39, "name": "Premier League (England)"},
        {"id": 140, "name": "La Liga (Spain)"},
        {"id": 135, "name": "Serie A (Italy)"},
        {"id": 78, "name": "Bundesliga (Germany)"},
        {"id": 61, "name": "Ligue 1 (France)"},
    ])

@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    print("\n⚡ E-Football AI Predictor")
    print(f"✓ API Keys: {len(RAPIDAPI_KEYS)}")
    print(f"✓ Redis: {bool(r)}")
    print(f"✓ Supabase: {bool(supabase)}")
    print(f"✓ Google AI: {bool(os.getenv('GOOGLE_AI_API_KEY'))}")
    print("\n🚀 Running on http://localhost:5000")
    print("📊 Dashboard: http://localhost:5000")
    print("🔗 API: /api/predict (POST)")
    print("🏥 Health: /api/health (GET)\n")
    
    app.run(debug=True, host="0.0.0.0", port=5000)
    app.run(debug=True, port=5000)