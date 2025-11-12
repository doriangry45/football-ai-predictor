from flask import Flask, jsonify, request, render_template
import requests
import os
import redis
import json
import logging
from datetime import datetime, timedelta
import google.generativeai as genai
from supabase import create_client
from services.feature-001.main import EFootballFetcher

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# === ENV ===
load_dotenv()
KEYS = [os.getenv("RAPIDAPI_KEY1"), os.getenv("RAPIDAPI_KEY2")]
genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-pro')

r = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"))
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

# === RATE LIMIT ===
def check_limit(key_prefix):
    today = datetime.now().strftime("%Y-%m-%d")
    key = f"{key_prefix}:{today}"
    count = r.incr(key)
    if count == 1:
        r.expire(key, 86400)
    if count > 900:  # 1000 limit
        logging.warning(f"Rate limit near: {count}")
        return False
    return True

# === FETCH + CACHE ===
def get_fixtures(league=39, season=2025):
    cache_key = f"fixtures:{league}:{season}"
    cached = supabase.table('api_cache').select('value').eq('key', cache_key).execute()
    if cached.data:
        return cached.data[0]['value']

    for i, key in enumerate(KEYS):
        if not check_limit(f"rapidapi_key{i+1}"):
            continue
        fetcher = EFootballFetcher(key)
        try:
            data = fetcher.fetch_fixtures(league, season)
            supabase.table('api_cache').upsert({
                "key": cache_key,
                "value": data,
                "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
            }).execute()
            return data
        except:
            continue
    return cached.data[0]['value'] if cached.data else []

# === AI PREDICT ===
def ai_predict(fixtures, query="over 2.5"):
    prompt = f"""
    Analyze these fixtures for "{query}":
    {json.dumps(fixtures[:5])}
    
    Return JSON with predictions.
    """
    response = model.generate_content(prompt)
    try:
        return json.loads(response.text)
    except:
        return {"error": "AI parse failed", "raw": response.text}

# === ROUTES ===
@app.route("/")
def dashboard():
    return render_template("predict.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.json
    league = data.get("league", 39)
    season = data.get("season", 2025)
    query = data.get("query", "over 2.5")

    fixtures = get_fixtures(league, season)
    if not fixtures:
        return jsonify({"error": "No data"}), 500

    prediction = ai_predict(fixtures, query)

    # Save to Supabase
    for match in prediction.get("matches", []):
        supabase.table('predictions').insert({
            "fixture_id": 123,
            "home_team": match["home"],
            "away_team": match["away"],
            "prediction": match,
            "probability": match["probability"]
        }).execute()

    return jsonify(prediction)

if __name__ == "__main__":
    app.run(debug=True, port=5000)