# AI Studio Prompts for Football Match Predictions

## 📋 Index

1. [Over/Under 2.5 Goals Prediction](#1-overunder-25-goals-prediction)
2. [Both Teams to Score (BTTS) Analysis](#2-both-teams-to-score-btts-analysis)
3. [Result Prediction (1X2)](#3-result-prediction-1x2)
4. [Advanced Statistical Analysis](#4-advanced-statistical-analysis)
5. [Team Form Analysis](#5-team-form-analysis)
6. [Head-to-Head Analysis](#6-head-to-head-analysis)

---

## 1. Over/Under 2.5 Goals Prediction

### Purpose
Analyze if match will have more than 2.5 goals (3 or more) or less than 2.5 goals (0-2).

### Prompt

```
Analyze this upcoming football match and predict if it will be Over 2.5 Goals (3+ goals) or Under 2.5 Goals (0-2 goals).

Match Data:
{
  "match": {
    "date": "{fixture_date}",
    "homeTeam": "{home_team}",
    "awayTeam": "{away_team}",
    "league": "{league_name}",
    "season": "{season}"
  },
  "homeTeamStats": {
    "goalsFor": "{avg_goals_scored}",
    "goalsAgainst": "{avg_goals_conceded}",
    "form": "{recent_results}",
    "totalMatches": "{total_matches}"
  },
  "awayTeamStats": {
    "goalsFor": "{avg_goals_scored}",
    "goalsAgainst": "{avg_goals_conceded}",
    "form": "{recent_results}",
    "totalMatches": "{total_matches}"
  }
}

Consider:
1. Historical Over/Under 2.5 performance
2. Average goals per match for both teams
3. Home/Away advantage impact
4. Recent form (last 5-10 matches)
5. Head-to-head history
6. League scoring patterns
7. Team injuries/absences (if known)

Provide:
{
  "prediction": "OVER/UNDER",
  "probability": 65,
  "confidence": "HIGH/MEDIUM/LOW",
  "reasoning": "Detailed analysis...",
  "keyFactors": ["Factor 1", "Factor 2", "Factor 3"],
  "alternativeScenario": "What could change this prediction",
  "tweet": "Turkish prediction summary in 280 chars"
}
```

### Example Response

```json
{
  "prediction": "OVER",
  "probability": 72,
  "confidence": "HIGH",
  "reasoning": "Home team averages 2.3 goals at home, away team averages 1.8 goals. Recent forms show attacking momentum. Head-to-head history: 60% Over 2.5.",
  "keyFactors": [
    "Home team scored 3+ in last 4 matches",
    "Away team defensive struggles (2.1 goals conceded/match)",
    "League average 2.9 goals (above 2.5)"
  ],
  "alternativeScenario": "Defensive parking could lower score if away team prioritizes not conceding",
  "tweet": "🎯 MAÇ TAHMİNİ: Over 2.5 (%72) - Her iki takım da ofensif oynuyor, istatistikler Over lehine 📊⚽"
}
```

---

## 2. Both Teams to Score (BTTS) Analysis

### Purpose
Predict if both teams will score in the match (BTTS: Yes/No).

### Prompt

```
Analyze this football match for Both Teams to Score (BTTS) prediction.

Match Data:
{
  "homeTeam": "{team_name}",
  "awayTeam": "{team_name}",
  "homeTeamDefense": {
    "cleanSheets": "{percentage}",
    "goalsAgainst": "{avg_per_match}",
    "defensiveRating": "{rating}"
  },
  "awayTeamDefense": {
    "cleanSheets": "{percentage}",
    "goalsAgainst": "{avg_per_match}",
    "defensiveRating": "{rating}"
  }
}

Key Analysis Points:
1. Defense strength (clean sheets %)
2. Attacking capability of both teams
3. Recent BTTS history
4. Home/Away scoring patterns
5. Tactical setup (attacking vs defensive)

Provide:
{
  "btts": "YES/NO",
  "probability": 65,
  "homeTeamToScore": 85,
  "awayTeamToScore": 72,
  "reasoning": "...",
  "tweet": "Turkish BTTS prediction"
}
```

---

## 3. Result Prediction (1X2)

### Purpose
Predict match winner or draw (1=Home Win, X=Draw, 2=Away Win).

### Prompt

```
Predict the final result of this football match (1X2 format: Home Win / Draw / Away Win).

Current Statistics:
{
  "homeTeam": "{name}",
  "awayTeam": "{name}",
  "homeForm": "{recent_results_with_scores}",
  "awayForm": "{recent_results_with_scores}",
  "headToHead": {
    "homeWins": "{count}",
    "draws": "{count}",
    "awayWins": "{count}",
    "averageScore": "{avg_goals}"
  },
  "standings": {
    "homePosition": "{position}",
    "awayPosition": "{position}",
    "homePoints": "{points}",
    "awayPoints": "{points}"
  }
}

Factors to Consider:
1. Current league position and points
2. Recent form (W/D/L record)
3. Head-to-head history
4. Home/Away performance
5. Team quality/rating
6. Motivation (title race, relegation battle, etc.)

Provide:
{
  "prediction": "1/X/2",
  "homeWinProbability": 45,
  "drawProbability": 25,
  "awayWinProbability": 30,
  "reasoning": "...",
  "mostLikelyScore": "2-1",
  "tweet": "Turkish result prediction"
}
```

---

## 4. Advanced Statistical Analysis

### Purpose
Deep statistical analysis for professional predictions.

### Prompt

```
Perform advanced statistical analysis for this football match prediction.

Team Statistics:
{
  "teams": [
    {
      "name": "{team_name}",
      "xG": "{expected_goals}",
      "xGA": "{expected_goals_against}",
      "possession": "{average_percentage}",
      "shotsOnTarget": "{average_per_match}",
      "pressureSuccess": "{percentage}",
      "passingAccuracy": "{percentage}"
    }
  ]
}

Calculate:
1. Elo Rating difference
2. Expected Goals (xG) advantage
3. Possession-based advantage
4. Pressing effectiveness
5. Historical performance index
6. Injury impact (if available)

Provide:
{
  "eloAdvantage": "Home +15",
  "xGPrediction": "Home 1.8 vs Away 1.2",
  "possessionAdvantage": "Home 52%",
  "overallAdvantage": "Home MODERATE",
  "probabilityDistribution": {
    "under1.5": "18%",
    "1.5to2.5": "35%",
    "over2.5": "47%"
  },
  "tweet": "İstatistikler ev sahibi takımı destekliyor 📈"
}
```

---

## 5. Team Form Analysis

### Purpose
Analyze current team form and momentum.

### Prompt

```
Analyze team form and momentum for this upcoming match.

Last 10 Matches Data:
{
  "homeTeam": {
    "results": ["W3-1", "W2-0", "D1-1", "L0-2", "W2-1", "D0-0", "W1-0", "L1-2", "W3-0", "W2-0"],
    "points": 19,
    "goalsFor": 16,
    "goalsAgainst": 7
  },
  "awayTeam": {
    "results": ["D1-1", "W2-1", "L1-3", "D0-0", "W2-0", "L0-1", "D1-1", "W1-0", "L2-3", "W3-1"],
    "points": 14,
    "goalsFor": 12,
    "goalsAgainst": 10
  }
}

Analyze:
1. Win/Draw/Loss ratio
2. Scoring trends
3. Recent momentum (up/down/stable)
4. Streak (current winning/losing streak)
5. Consistency

Provide:
{
  "homeMomentum": "STRONG (W-W-W trend)",
  "awayMomentum": "MIXED (alternating results)",
  "homeFormRating": "8.5/10",
  "awayFormRating": "5.5/10",
  "formAdvantage": "HOME +3.0",
  "tweet": "Ev sahibi takım 3 maç üst üste kazanıyor, formda üstün 💪"
}
```

---

## 6. Head-to-Head Analysis

### Purpose
Analyze historical matchups between teams.

### Prompt

```
Analyze head-to-head history between these teams.

Historical Data (Last 10 Meetings):
{
  "homeTeam": "{name}",
  "awayTeam": "{name}",
  "meetings": [
    {"date": "2024-01-15", "result": "2-1", "winner": "home"},
    {"date": "2023-12-28", "result": "1-1", "winner": "draw"},
    ...
  ],
  "allTimeStats": {
    "homeWins": 12,
    "draws": 8,
    "awayWins": 7,
    "totalGoals": 68,
    "homeGoals": 37,
    "awayGoals": 31
  }
}

Analyze:
1. Dominance (who wins more often)
2. Average goals in H2H
3. Recent H2H results
4. Home/Away split
5. Psychological factor

Provide:
{
  "historicalDominance": "Home team leads (12W-8D-7L)",
  "h2hAverageGoals": 2.27,
  "recentTrend": "Home won last 2",
  "h2hAdvantage": "HOME",
  "psychologicalEdge": "SLIGHT (Home team confident)",
  "tweet": "H2H'de ev sahibi takım tarihsel üstünlüğe sahip 📊"
}
```

---

## 📊 Response Format Standards

All predictions should return JSON in this format:

```json
{
  "prediction": "OVER/UNDER/YES/NO/1/X/2",
  "probability": 65,
  "confidence": "HIGH/MEDIUM/LOW",
  "reasoning": "Detailed analysis with key points",
  "keyFactors": [
    "Factor 1 with evidence",
    "Factor 2 with evidence",
    "Factor 3 with evidence"
  ],
  "alternativeScenario": "What could change this prediction",
  "tweet": "Turkish prediction (max 280 chars) with emojis"
}
```

---

## 🎯 Usage in Application

### Python Integration

```python
import google.generativeai as genai

def ai_predict(fixtures_data, query="over 2.5"):
    """Send fixture data to AI with appropriate prompt."""
    
    # Select appropriate prompt based on query
    prompts = {
        "over 2.5": OVER_UNDER_PROMPT,
        "btts": BTTS_PROMPT,
        "1x2": RESULT_PROMPT,
    }
    
    prompt = prompts.get(query.lower(), OVER_UNDER_PROMPT)
    
    # Inject fixture data into prompt
    full_prompt = prompt.format(**fixtures_data)
    
    # Get AI response
    response = model.generate_content(full_prompt)
    
    # Parse and return
    return json.loads(response.text)
```

### API Endpoint

```bash
POST /api/predict
{
  "league": 39,
  "season": 2025,
  "query": "over 2.5"  # or "btts", "1x2", "form"
}

Response:
{
  "matches": [
    {
      "home": "Manchester United",
      "away": "Liverpool",
      "prediction": "OVER",
      "probability": 72,
      "reasoning": "...",
      "tweet": "..."
    }
  ]
}
```

---

## 💡 Tips for Better Predictions

1. **Use Current Data** - Always fetch latest statistics
2. **Consider Context** - Season stage, motivation, injuries
3. **Triangulate** - Use multiple prediction methods
4. **Validate** - Track prediction accuracy over time
5. **Adjust Weights** - Different leagues have different patterns
6. **Include Uncertainty** - Provide confidence levels

---

**Last Updated**: 2025-11-13  
**Version**: 1.0  
**Maintained By**: AI Predictions Team
