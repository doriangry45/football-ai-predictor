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

# Prompt version control
PROMPT_VERSION = os.getenv("PROMPT_VERSION", "v2")


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
    # Allow running with stubbed google.generativeai in test/dev environments
    
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
    
    # Gather additional context (standings, team stats, player availability)
    def gather_additional_context(fixtures_list, league=39, season=2025):
        team_stats = {}
        players_status = {}
        standings = []
        try:
            fetcher = EFootballFetcher(RAPIDAPI_KEYS[0] if RAPIDAPI_KEYS else None)
            # Standings
            try:
                standings_resp = fetcher.fetch_standings(league=league, season=season)
                standings = standings_resp.get('response', [])
            except Exception:
                standings = []

            # For each team in fixtures, try to get team stats and players (limited)
            team_ids = set()
            for fx in fixtures_list:
                try:
                    h_id = fx.get('teams', {}).get('home', {}).get('id')
                    a_id = fx.get('teams', {}).get('away', {}).get('id')
                    if h_id: team_ids.add(h_id)
                    if a_id: team_ids.add(a_id)
                except Exception:
                    continue

            for tid in list(team_ids)[:8]:
                try:
                    stats = fetcher.fetch_team_stats(team=tid, season=season)
                    team_stats[tid] = stats.get('response', {})
                except Exception:
                    team_stats[tid] = {}
                try:
                    players = fetcher.fetch_players(team=tid, season=season)
                    players_status[tid] = players.get('response', [])
                except Exception:
                    players_status[tid] = []
        except Exception as e:
            logging.warning(f"Gathering context failed: {e}")
        return team_stats, players_status, standings

    team_stats, players_status, standings = gather_additional_context(fixtures, league=39, season=2025)

    # Load prompt template based on PROMPT_VERSION
    prompt_template = None
    try:
        if PROMPT_VERSION == 'v1':
            with open(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'prompts', 'prompt_v1_over_under.md'), 'r', encoding='utf-8') as f:
                prompt_template = f.read()
        else:
            with open(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'prompts', 'prompt_v2_over_under.md'), 'r', encoding='utf-8') as f:
                prompt_template = f.read()
    except Exception:
        # fallback to inline prompt if files missing
        prompt_template = None

    prompt = None
    if prompt_template:
        prompt = prompt_template.replace('{fixtures_json}', json.dumps(fixture_summary, indent=2))
        prompt = prompt.replace('{team_stats_json}', json.dumps({k: v for k, v in list(team_stats.items())[:5]}, indent=2))
        prompt = prompt.replace('{players_status_json}', json.dumps({k: v[:4] for k, v in list(players_status.items())[:5]}, indent=2))
        prompt = prompt.replace('{standings_json}', json.dumps(standings[:8], indent=2))
    else:
        # inline fallback
        prompt = f"Analyze these upcoming football fixtures for \"{query}\" predictions:\n{json.dumps(fixture_summary, indent=2)}\nReturn JSON."
    
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
                prompt_version = os.getenv('PROMPT_VERSION', PROMPT_VERSION)
                # store limited player snapshot to avoid very large payloads
                for match in prediction.get("matches", []):
                    player_snapshot = {}
                    try:
                        # look up available players for home and away if present
                        # match may include team ids in fixture_summary; attempt to include small snapshot
                        player_snapshot = {
                            'home_players': [p.get('player', {}).get('name') for p in players_status.get(match.get('home'), [])][:6] if isinstance(players_status, dict) else [],
                            'away_players': [p.get('player', {}).get('name') for p in players_status.get(match.get('away'), [])][:6] if isinstance(players_status, dict) else []
                        }
                    except Exception:
                        player_snapshot = {}

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
                        "prompt_version": prompt_version,
                        "player_snapshot": json.dumps(player_snapshot),
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


@app.route("/api/fixtures", methods=["GET"])
def api_fixtures():
    league = int(request.args.get("league", 39))
    season = int(request.args.get("season", 2025))
    try:
        data = get_fixtures(league=league, season=season)
        return jsonify(data)
    except Exception as e:
        logging.error(f"/api/fixtures error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/players", methods=["GET"])
def api_players():
    team = request.args.get("team")
    season = int(request.args.get("season", 2025))
    if not team:
        return jsonify({"error": "team param required"}), 400
    try:
        fetcher = EFootballFetcher(RAPIDAPI_KEYS[0] if RAPIDAPI_KEYS else None)
        data = fetcher.fetch_players(team=int(team), season=season)
        return jsonify(data)
    except Exception as e:
        logging.error(f"/api/players error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/standings", methods=["GET"])
def api_standings():
    league = int(request.args.get("league", 39))
    season = int(request.args.get("season", 2025))
    try:
        fetcher = EFootballFetcher(RAPIDAPI_KEYS[0] if RAPIDAPI_KEYS else None)
        data = fetcher.fetch_standings(league=league, season=season)
        return jsonify(data)
    except Exception as e:
        logging.error(f"/api/standings error: {e}")
        return jsonify({"error": str(e)}), 500

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