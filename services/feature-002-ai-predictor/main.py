#!/usr/bin/env python3
"""
E-Football Fetcher - RapidAPI integration for feature-002
"""
import os
import json
import requests
from typing import Optional, Dict, Any


class EFootballFetcher:
    """Fetch e-football fixtures from RapidAPI."""
    
    BASE_URL = "https://api-football-v1.p.rapidapi.com/v3"
    HOST = "api-football-v1.p.rapidapi.com"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize fetcher with RapidAPI key from env or argument."""
        self.api_key = api_key or os.environ.get("RAPIDAPI_KEY")
        if not self.api_key:
            raise ValueError("RAPIDAPI_KEY not set in environment or argument")
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.HOST,
        }
    
    def fetch_fixtures(self, league: int = 39, season: int = 2025, **kwargs) -> Dict[str, Any]:
        """
        Fetch fixtures for a given league and season.
        
        Args:
            league: League ID (default 39 = Premier League)
            season: Season year (default 2025)
            **kwargs: Additional query params
        
        Returns:
            JSON response dict
        """
        params = {"league": league, "season": season}
        params.update(kwargs)
        
        url = f"{self.BASE_URL}/fixtures"
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def fetch_standings(self, league: int = 39, season: int = 2025) -> Dict[str, Any]:
        """Fetch league standings."""
        params = {"league": league, "season": season}
        url = f"{self.BASE_URL}/standings"
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    
    def fetch_statistics(self, fixture_id: int) -> Dict[str, Any]:
        """Fetch fixture statistics."""
        params = {"fixture": fixture_id}
        url = f"{self.BASE_URL}/fixtures/statistics"
        response = requests.get(url, headers=self.headers, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
